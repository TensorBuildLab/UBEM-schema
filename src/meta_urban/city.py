"""E8: city-scale integration in New York City with AI-built inputs (paper Section 7.3).

    python scripts/download_nyc.py      # once
    python -m meta_urban.city           # runs the model calls (cached) and writes tables and the map

Sources: LL84 energy benchmarking disclosures for calendar year 2023 (33,684 properties, 265 columns) and PLUTO
tax lots (858,284 lots). A small pipeline joins each benchmarked property to its tax lot through the BBL
identifier, converts floor area and energy to SI, and reports floor-area-weighted energy use intensity (EUI)
for each of the 59 community districts.

The language model does the two integration steps a person would otherwise do:
  1. Selection (mapping in the loop): for each concept the pipeline needs, choose the column of the dataset that
     holds it, given the concept as an identifier only (L0) or as a Meta-Urban concept card (L2).
  2. Normalization: for each selected column, give its unit, multiplier and missing codes from the column name,
     its description and a sample of its values, without (T3) or with (T3P) the LL84 dataset card.
The reference pipeline uses the publisher's columns and units. Everything the AI pipeline does differently is
caused by the AI-built selection and profiles. The profile checks of E7 (meta_urban.endtoend.profile_check,
frozen before these data were opened) are applied unchanged, as a held-out test.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache

import numpy as np
import pandas as pd
import yaml

from . import DATA_RAW, PAPER, SCHEMA_YAML
from .bench import parse_json
from .checks import check as check_v2
from .endtoend import profile_check
from .io import leaf_concepts
from .llm import ROLE, UNIT_CHOICES, _concept_block, complete, load_cache, t3_request

NYC = DATA_RAW / "nyc"
TAB, FIG = PAPER / "tables", PAPER / "figures"
MODELS = ["ollama:qwen3:8b", "ollama:llama3.1:8b"]
KBTU_TO_KWH, FT2_TO_M2 = 1 / 3.412141633, 0.09290304

# concepts the pipeline needs, the purpose shown to the model, and the columns that correctly hold each one
# The key role is described by the schema element that models shared keys: the JoinKey value parcel_id (dataset
# level), written before this case. A first run described it with the concept record_identifier, whose definition
# ("within the dataset") correctly led both models with full cards to the internal Property ID; that run is kept in
# paper/tables/city_v1_record_identifier/ and reported as a specification error of the authors.
ROLES = {
    "bbl": ("join:parcel_id", "join each benchmarked property to New York City tax-lot (PLUTO) data",
            {"nyc_borough_block_and_lot"}),
    "area": ("gross_floor_area", "compute annual energy use intensity per unit floor area",
             {"property_gfa_self_reported", "property_gfa_calculated", "property_gfa_calculated_1"}),
    "site": ("total_energy_consumption", "compute annual site energy use intensity",
             {"site_energy_use_kbtu"}),
    "elec": ("electricity_consumption", "compute annual electricity use intensity",
             {"electricity_use_grid_purchase", "electricity_use_grid_purchase_1",
              "electricity_use_grid_purchase_2", "electricity_use_grid_purchase_3"}),
    "gas": ("natural_gas_consumption", "compute annual natural gas use intensity",
            {"natural_gas_use_kbtu", "natural_gas_use_therms_"}),
}
PLUTO_ROLE = ("join:parcel_id", "join tax lots to benchmarked properties", {"bbl"})
REF_COLUMNS = {"bbl": "nyc_borough_block_and_lot", "area": "property_gfa_calculated_1",
               "site": "site_energy_use_kbtu", "elec": "electricity_use_grid_purchase_1",
               "gas": "natural_gas_use_kbtu"}
EUI_RANGE = (5.0, 3000.0)  # kWh/m2 per year; records outside are treated as data errors (same rule for every run)


# ------------------------------------------------------------------------------------------------ data
@lru_cache
def ll84() -> pd.DataFrame:
    return pd.read_csv(NYC / "ll84_2023.csv", low_memory=False, dtype=str)


@lru_cache
def pluto() -> pd.DataFrame:
    p = pd.read_csv(NYC / "pluto.csv", low_memory=False, usecols=["bbl", "cd", "borough"])
    p = p.dropna(subset=["bbl"])
    p["bbl"] = p.bbl.astype("int64").astype(str)
    return p


@lru_cache
def columns(name: str) -> pd.DataFrame:
    m = json.loads((NYC / f"{name}_columns.json").read_text(encoding="utf-8"))
    return pd.DataFrame([{"field": c["fieldName"], "name": c["name"], "description": c.get("description") or ""}
                         for c in m["columns"] if not c["fieldName"].startswith(":")])


# ------------------------------------------------------------------------------------------ model calls
def _join_key_block(level: str, key: str) -> str:
    """A JoinKey value, documented like a concept: identifier only (L0) or with its schema definition (L2)."""
    if level == "L0":
        return key
    with open(SCHEMA_YAML, encoding="utf-8") as fh:
        desc = yaml.safe_load(fh)["enums"]["JoinKey"]["permissible_values"][key]["description"]
    return f"{key}: {key.replace('_', ' ')}. {desc} [join key type: keys through which records can be linked to other datasets]"


def select_request(dataset: str, concept_id: str, purpose: str, level: str) -> dict:
    cols = columns(dataset)
    if concept_id.startswith("join:"):
        concept_text = _join_key_block(level, concept_id.split(":", 1)[1])
    else:
        concept_text = _concept_block(level, [next(c for c in leaf_concepts() if c["id"] == concept_id)])
    block = "\n".join(f"{r.field}: {r.name}" for r in cols.itertuples())
    system = (f"{ROLE}\n\nTask: a data pipeline needs the column of a dataset that holds a given concept. Choose the "
              "single best column, or \"none\" if no column holds it.\n\n"
              f"DATASET COLUMNS (field: display name)\n{block}\n\n"
              'Output: {"column": <field or "none">, "confidence": <0 to 1>}')
    user = f"CONCEPT\n{concept_text}\n\nPURPOSE\n{purpose}"
    schema = {"type": "object", "properties": {"column": {"type": "string", "enum": list(cols.field) + ["none"]},
                                               "confidence": {"type": "number"}},
              "required": ["column", "confidence"], "additionalProperties": False}
    return {"system": system, "user": user, "schema": schema}


def _value_summary(s: pd.Series, k: int = 5) -> tuple[str, float | None, float | None]:
    num = pd.to_numeric(s, errors="coerce")
    text = s[num.isna() & s.notna()].value_counts().head(k)
    parts = [f'"{v}" ({n:,} records)' for v, n in text.items()]
    lo, hi = (float(num.min()), float(num.max())) if num.notna().any() else (None, None)
    if lo is not None:
        parts.insert(0, f"numeric values from {lo:,.0f} to {hi:,.0f}")
    return "; ".join(parts) if parts else "(no values)", lo, hi


def norm_item(field: str) -> dict:
    cols = columns("ll84").set_index("field")
    desc = " ".join(cols.loc[field, "description"].split()[:40])
    summary, lo, hi = _value_summary(ll84()[field])
    return {"dataset": "nyc_ll84", "name": cols.loc[field, "name"], "label": f"{cols.loc[field, 'name']}. {desc}",
            "codes_raw": summary, "code_list": [], "value_min": lo, "value_max": hi}


def gold_profile(field: str) -> dict:
    name = columns("ll84").set_index("field").loc[field, "name"]
    unit, mult = "none", 0
    if "(kBtu)" in name:
        unit, mult = "unit:BTU_IT", 1000
    elif "(kWh)" in name:
        unit, mult = "unit:KiloW-HR", 1
    elif "(therms)" in name:
        unit, mult = "unit:BTU_IT", 100000
    elif "(ft" in name:
        unit, mult = "unit:FT2", 1
    miss = ["Not Available"] if (ll84()[field] == "Not Available").any() else []
    return {"is_weight": False, "unit": unit, "unit_multiplier": mult, "missing_codes": miss}


def _profile_from(js: dict) -> dict:
    return {"is_weight": bool(js.get("is_weight")), "unit": js.get("unit") or "none",
            "unit_multiplier": js.get("unit_multiplier") or 0,
            "missing_codes": [str(c) for c in (js.get("missing_codes") or [])]}


# ------------------------------------------------------------------------------------------------ pipeline
TO_KWH = {"unit:BTU_IT": 1 / 3412.141633, "unit:KiloW-HR": 1.0, "unit:KiloBTU_IT": 1 / 3.412141633,
          "unit:THM_US": 29.30710702}
# Post hoc variant (exploratory, written after seeing that both models write kBtu as kWh): the unit vocabulary also
# offers the publisher's own units, so that "kBtu" need not be decomposed into Btu and a multiplier.
UNITS_PUBLISHER = UNIT_CHOICES[:2] + ["unit:KiloBTU_IT", "unit:THM_US"] + UNIT_CHOICES[2:]


def t3_request_units(item: dict, card: bool, units: list[str] | None = None) -> dict:
    req = t3_request(item, profile=card)
    if units:
        req = {**req, "system": req["system"].replace(str(UNIT_CHOICES), str(units)),
               "schema": json.loads(json.dumps(req["schema"]))}
        req["schema"]["properties"]["unit"]["enum"] = list(units)
    return req


def to_si(unit: str, mult) -> float | None:
    """Factor from raw values to kWh (energy) or m² (area); None when the unit cannot be converted."""
    f = TO_KWH.get(unit, {"unit:FT2": FT2_TO_M2}.get(unit))
    return None if f is None else f * float(mult or 1)
TO_M2 = {"unit:FT2": FT2_TO_M2}


def _values(field: str, prof: dict, table: dict) -> pd.Series:
    s = ll84()[field]
    miss = {c for c in prof["missing_codes"] if c != ""}
    s = s.where(~s.isin(miss))
    x = pd.to_numeric(s, errors="coerce")  # anything still non-numeric cannot be used
    f = table.get(prof["unit"])
    m = float(prof["unit_multiplier"] or 1)
    return x * (f * m if f is not None else np.nan)


def split_bbl(s: str) -> str | None:
    """First tax lot of a property, as a 10-digit BBL (None when absent or malformed)."""
    if not isinstance(s, str):
        return None
    first = re.split(r"[;,]", s)[0].strip()
    m = re.fullmatch(r"(\d)-?(\d{5})-?(\d{4})", first)
    return "".join(m.groups()) if m else None


def run_pipeline(sel: dict, prof: dict) -> dict:
    """sel: role -> LL84 field (or 'none'); prof: field -> profile. Returns city totals and the district table."""
    d = ll84()
    out = {"records": len(d)}
    if any(sel.get(r, "none") == "none" for r in ("bbl", "area", "site")):
        return out | {"failed": True}
    key = d[sel["bbl"]].map(split_bbl)
    area = _values(sel["area"], prof[sel["area"]], TO_M2)
    energy = {r: _values(sel[r], prof[sel[r]], TO_KWH) if sel.get(r, "none") != "none" else pd.Series(np.nan, index=d.index)
              for r in ("site", "elec", "gas")}
    eui = energy["site"] / area
    ok = key.notna() & (area > 0) & eui.between(*EUI_RANGE)
    lots = pluto().drop_duplicates("bbl").set_index("bbl")
    cd = key.map(lots.cd)
    linked = ok & cd.notna()
    df = pd.DataFrame({"cd": cd, "area": area, **energy})[linked]
    g = df.groupby("cd")
    dist = pd.DataFrame({"records": g.size(), "area_m2": g.area.sum(), "site_kwh": g.site.sum(min_count=1),
                         "elec_kwh": g.elec.sum(min_count=1), "gas_kwh": g.gas.sum(min_count=1)})
    dist["eui"] = dist.site_kwh / dist.area_m2
    dist["elec_intensity"] = dist.elec_kwh / dist.area_m2
    dist["gas_intensity"] = dist.gas_kwh / dist.area_m2
    out |= {"failed": False, "key_parsed": int(key.notna().sum()), "usable": int(ok.sum()),
            "linked": int(linked.sum()), "eui_city": float(df.site.sum() / df.area.sum()),
            "elec_city": float(df.elec.sum() / df.area.sum()), "gas_city": float(df.gas.sum() / df.area.sum()),
            "area_m2": float(df.area.sum()), "districts": dist}
    return out


# ------------------------------------------------------------------------------------------------ experiment
def ai_runs() -> list[dict]:
    runs = []
    pl_cols = set(columns("pluto").field)
    for model in MODELS:
        cache = load_cache(model)
        for level in ("L0", "L2"):
            sel, conf = {}, {}
            for role, (cid, purpose, _) in ROLES.items():
                r = complete(model, select_request("ll84", cid, purpose, level),
                             {"task": "E8-select", "dataset": "nyc_ll84", "name": role, "level": level}, 0, cache)
                js = parse_json(r["response"]) or {}
                sel[role], conf[role] = js.get("column", "none"), js.get("confidence")
            r = complete(model, select_request("pluto", PLUTO_ROLE[0], PLUTO_ROLE[1], level),
                         {"task": "E8-select", "dataset": "nyc_pluto", "name": "bbl", "level": level}, 0, cache)
            pl = (parse_json(r["response"]) or {}).get("column", "none")
            for card in (False, True):
                prof = {}
                for role, field in sel.items():
                    if field == "none" or role == "bbl":
                        continue
                    req = t3_request(norm_item(field), profile=card)
                    r = complete(model, req, {"task": "E8-T3P" if card else "E8-T3", "dataset": "nyc_ll84",
                                              "name": field}, 0, cache)
                    prof[field] = _profile_from(parse_json(r["response"]) or {})
                runs.append({"model": model.split(":", 1)[1], "selection": level, "card": card, "sel": sel,
                             "conf": conf, "pluto_key": pl, "pluto_key_ok": pl in PLUTO_ROLE[2] and pl in pl_cols,
                             "prof": prof})
    return runs


def _city_errors(res: dict, ref: dict) -> dict:
    if res.get("failed", True):
        return {"failed": True}
    pct = lambda k: 100 * (res[k] - ref[k]) / ref[k]  # noqa: E731
    err = 100 * (res["districts"].eui.reindex(ref["districts"].index) - ref["districts"].eui) / ref["districts"].eui
    return {"failed": False, "linked": res["linked"], "eui_city_err_pct": pct("eui_city"),
            "elec_city_err_pct": pct("elec_city"), "gas_city_err_pct": pct("gas_city"),
            "median_abs_district_err_pct": float(err.abs().median())}


def decomposition(ref: dict) -> pd.DataFrame:
    """Separate the two AI steps: the model's column selection with gold profiles (selection only), and the
    reference columns with the model's profiles (normalization only)."""
    rows = []
    for model in MODELS:
        cache = load_cache(model)
        for run in (r for r in ai_runs() if r["model"] == model.split(":", 1)[1] and not r["card"]):
            sel = run["sel"]
            gold = {f: gold_profile(f) for r, f in sel.items() if r != "bbl" and f != "none"}
            res = run_pipeline(sel, gold) if run["pluto_key_ok"] else {"failed": True}
            rows.append({"model": run["model"], "variant": "selection only", "selection": run["selection"],
                         "card": None} | _city_errors(res, ref))
        for variant, units in (("normalization only", None),
                               ("normalization only, publisher units offered (post hoc)", UNITS_PUBLISHER)):
            for card in (False, True):
                prof = {}
                for role, field in REF_COLUMNS.items():
                    if role == "bbl":
                        continue
                    task = ("E8-T3P" if card else "E8-T3") + ("-units" if units else "")
                    r = complete(model, t3_request_units(norm_item(field), card, units),
                                 {"task": task, "dataset": "nyc_ll84", "name": field}, 0, cache)
                    prof[field] = _profile_from(parse_json(r["response"]) or {})
                rows.append({"model": model.split(":", 1)[1], "variant": variant, "selection": "reference",
                             "card": card} | _city_errors(run_pipeline(REF_COLUMNS, prof), ref)
                            | {"profiles": json.dumps(prof)})
    return pd.DataFrame(rows)


def check_v2_without_ll84_terms(item: dict, prof: dict) -> list[str]:
    """Version 2 without the three terms that occur in LL84 but in neither survey ('Not Available', kBtu, ft²).
    Version 2 was committed together with the LL84 catalog conventions, after the LL84 column list had been read,
    so these terms may reflect knowledge of the city data; this ablation removes them."""
    from . import checks as C

    saved = (C.UNIT_WORDS, C.NON_SUBSTANTIVE, C.expected_multiplier)
    C.UNIT_WORDS = {k: tuple(w for w in v if w not in ("ft²", "ft2")) for k, v in saved[0].items()}
    C.NON_SUBSTANTIVE = tuple(w for w in saved[1] if w != "not available")
    C.expected_multiplier = lambda label, unit: saved[2](re.sub(r"\bkbtu\b", "btu", label, flags=re.I), unit)
    try:
        return C.check(item, prof)
    finally:
        C.UNIT_WORDS, C.NON_SUBSTANTIVE, C.expected_multiplier = saved


def checks_heldout(summary_profiles: pd.DataFrame, decomp: pd.DataFrame) -> pd.DataFrame:
    """Profile checks v1 (frozen after E7) and v2 (frozen before this case) on every distinct AI-built profile of
    the city case. A profile is an indicator-changing error when its conversion factor to SI differs from the gold
    one (unit or multiplier) or when it drops valid values (a numeric missing code that occurs in the data)."""
    profs = [("main", r.model, r.column, json.loads(r.profile)) for r in summary_profiles.itertuples()]
    for r in decomp.dropna(subset=["profiles"]).itertuples():
        src = "post hoc units" if "post hoc" in r.variant else "main"
        profs += [(src, r.model, f, p) for f, p in json.loads(r.profiles).items()]
    seen, rows = set(), []
    for src, model, field, p in profs:
        key = (src, model, field, json.dumps(p, sort_keys=True))
        if key in seen:
            continue
        seen.add(key)
        g, item = gold_profile(field), norm_item(field)
        gf, pf = to_si(g["unit"], g["unit_multiplier"]), to_si(p["unit"], p["unit_multiplier"])
        # a wrong conversion to SI, or a unit given to a column that has none in the vocabulary (an intensity)
        unit_wrong = (g["unit"] != "none" and (pf is None or abs(pf / gf - 1) > 1e-6)) or \
                     (g["unit"] == "none" and p["unit"] != "none")
        vals = set(ll84()[field].dropna().unique())
        drops = [c for c in p["missing_codes"] if c and c in vals and pd.notna(pd.to_numeric(c, errors="coerce"))]
        miss_extra = sorted(c for c in p["missing_codes"] if c) != sorted(g["missing_codes"])
        status = "error" if unit_wrong or drops else ("harmless deviation" if miss_extra else "exact")
        rows.append({"source": src, "model": model, "column": field, "unit": p["unit"],
                     "multiplier": p["unit_multiplier"], "missing_codes": "; ".join(p["missing_codes"]),
                     "unit_wrong": unit_wrong, "drops_valid_values": bool(drops), "status": status,
                     "flagged_v1": bool(profile_check(item, p)), "flagged_v2": bool(check_v2(item, p)),
                     "flagged_v2_without_ll84_terms": bool(check_v2_without_ll84_terms(item, p)),
                     "flags_v2": "; ".join(check_v2(item, p))})
    return pd.DataFrame(rows)


def _district_shapes() -> dict[float, list]:
    g = json.loads((NYC / "community_districts.geojson").read_text(encoding="utf-8"))
    out = {}
    for f in g["features"]:
        cd = float(f["properties"]["boro_cd"])
        geom = f["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        out[cd] = [np.asarray(p[0]) for p in polys]
    return out


def fig_city(ref_d: pd.DataFrame, panels: list[tuple[str, pd.Series]], path, min_records: int = 20) -> None:
    """(a) reference EUI by community district; (b...) relative error of AI pipelines by district."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    from matplotlib.colors import TwoSlopeNorm

    from .analytics import INK2, save_fig

    shapes = _district_shapes()
    keep = ref_d.index[ref_d.records >= min_records]
    n = 1 + len(panels)
    fig, axes = plt.subplots(1, n, figsize=(2.55 * n, 3.15), dpi=200)
    lon0 = np.cos(np.radians(40.7))

    def draw(ax, values, cmap, norm, title):
        polys, cols, base = [], [], []
        for cd, rings in shapes.items():
            for r in rings:
                xy = np.c_[r[:, 0] * lon0, r[:, 1]]
                if cd in keep and cd in values.index and np.isfinite(values[cd]):
                    polys.append(xy)
                    cols.append(values[cd])
                else:
                    base.append(xy)
        ax.add_collection(PolyCollection(base, facecolor="#ecebe6", edgecolor="#ffffff", linewidth=0.3))
        pc = PolyCollection(polys, array=np.asarray(cols), cmap=cmap, norm=norm, edgecolor="#ffffff", linewidth=0.3)
        ax.add_collection(pc)
        ax.autoscale_view()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=7.2, color=INK2, loc="left")
        return pc

    pc = draw(axes[0], ref_d.eui, "Blues", plt.Normalize(ref_d.eui[keep].quantile(0.05), ref_d.eui[keep].quantile(0.95)),
              "(a) Reference site EUI")
    cb = fig.colorbar(pc, ax=axes[0], orientation="horizontal", fraction=0.05, pad=0.02)
    cb.set_label("kWh/(m²·yr)", fontsize=6.5)
    cb.ax.tick_params(labelsize=6)
    lim = max(5.0, max(float(np.nanmax(np.abs(v[keep.intersection(v.index)]))) for _, v in panels) if panels else 5.0)
    lim = min(np.ceil(lim / 5) * 5, 100.0)
    for k, (title, err) in enumerate(panels, 1):
        pc = draw(axes[k], err.clip(-lim, lim), "RdBu_r", TwoSlopeNorm(0, -lim, lim), f"({chr(97 + k)}) {title}")
        cb = fig.colorbar(pc, ax=axes[k], orientation="horizontal", fraction=0.05, pad=0.02)
        cb.set_label("Error in district EUI (%)", fontsize=6.5)
        cb.ax.tick_params(labelsize=6)
    fig.tight_layout()
    save_fig(fig, path)
    plt.close(fig)


def main() -> int:
    ref_prof = {f: gold_profile(f) for f in REF_COLUMNS.values() if f != "nyc_borough_block_and_lot"}
    ref = run_pipeline(REF_COLUMNS, ref_prof)
    rd = ref["districts"]
    rows, sel_rows, prof_rows, dist_rows = [], [], [], []
    for run in ai_runs():
        tag = {"model": run["model"], "selection": run["selection"], "card": run["card"]}
        for role, field in run["sel"].items():
            sel_rows.append(tag | {"role": role, "column": field, "correct": field in ROLES[role][2],
                                   "confidence": run["conf"][role]})
        sel_rows.append(tag | {"role": "pluto_bbl", "column": run["pluto_key"], "correct": run["pluto_key_ok"]})
        # profiles: compare with the gold profile of the selected column, and apply the frozen E7 rules
        for field, p in run["prof"].items():
            g = gold_profile(field)
            wrong = [f for f in ("unit",) if p[f] != g[f]]
            if g["unit"] != "none" and float(p["unit_multiplier"] or 1) != float(g["unit_multiplier"] or 1):
                wrong.append("unit_multiplier")
            if sorted(c for c in p["missing_codes"] if c) != sorted(c for c in g["missing_codes"] if c):
                wrong.append("missing_codes")
            flags = profile_check(norm_item(field), p)
            flags2 = check_v2(norm_item(field), p)
            prof_rows.append(tag | {"column": field, "fields_wrong": "; ".join(wrong), "flags_v1": "; ".join(flags),
                                    "flags_v2": "; ".join(flags2), "profile": json.dumps(p)})
        if not run["pluto_key_ok"]:
            res = {"failed": True}
        else:
            prof = {**run["prof"]}
            res = run_pipeline(run["sel"], prof)
        r = tag | {"failed": res.get("failed", True)}
        if not r["failed"]:
            dd = res["districts"].reindex(rd.index)
            err = 100 * (dd.eui - rd.eui) / rd.eui
            r |= {"linked": res["linked"], "linked_vs_ref_pct": 100 * (res["linked"] - ref["linked"]) / ref["linked"],
                  "eui_city": res["eui_city"], "eui_city_err_pct": 100 * (res["eui_city"] - ref["eui_city"]) / ref["eui_city"],
                  "elec_city_err_pct": 100 * (res["elec_city"] - ref["elec_city"]) / ref["elec_city"],
                  "gas_city_err_pct": 100 * (res["gas_city"] - ref["gas_city"]) / ref["gas_city"],
                  "districts_off_by_5pct": int((err.abs() > 5).sum()), "median_abs_district_err_pct": float(err.abs().median()),
                  "max_abs_district_err_pct": float(err.abs().max())}
            for cdv, e in err.items():
                dist_rows.append(tag | {"cd": cdv, "eui_ref": rd.eui[cdv], "eui_ai": dd.eui[cdv], "err_pct": e})
        rows.append(r)
    summary = pd.DataFrame(rows)
    decomp = decomposition(ref)
    decomp.to_csv(TAB / "city_decomposition.csv", index=False)
    checks_heldout(pd.DataFrame(prof_rows), decomp).to_csv(TAB / "city_checks_heldout.csv", index=False)
    pd.DataFrame(sel_rows).to_csv(TAB / "city_selection.csv", index=False)
    pd.DataFrame(prof_rows).to_csv(TAB / "city_profiles.csv", index=False)
    pd.DataFrame(dist_rows).to_csv(TAB / "city_district_errors.csv", index=False)
    summary.to_csv(TAB / "city_summary.csv", index=False)
    refrow = {k: ref[k] for k in ("records", "key_parsed", "usable", "linked", "eui_city", "elec_city", "gas_city",
                                  "area_m2")}
    pd.DataFrame([refrow]).to_csv(TAB / "city_reference.csv", index=False)
    rd.to_csv(TAB / "city_reference_districts.csv")
    # Map: the error caused by the models' column selection with full concept cards (gold profiles). Both models
    # chose the same floor-area column (with parking); the normalization errors are near-uniform factors (Table 9).
    panels, sel_dist = [], []
    for run in ai_runs():
        if run["selection"] != "L2" or run["card"] or not run["pluto_key_ok"]:
            continue
        sel = run["sel"]
        res = run_pipeline(sel, {f: gold_profile(f) for r, f in sel.items() if r != "bbl" and f != "none"})
        if res.get("failed", True):
            continue
        err = 100 * (res["districts"].eui.reindex(rd.index) - rd.eui) / rd.eui
        sel_dist.append(pd.DataFrame({"model": run["model"], "cd": err.index, "err_pct": err.values,
                                      "area_column": sel["area"]}))
    if sel_dist:
        sd = pd.concat(sel_dist)
        sd.to_csv(TAB / "city_district_errors_selection.csv", index=False)
        same = sd.groupby("cd").err_pct.nunique().max() == 1
        first = sd[sd.model == sd.model.iloc[0]].set_index("cd").err_pct
        panels.append(("Error from models' column choice" if same else "Error from Qwen3's column choice", first))
    fig_city(rd, panels, FIG / "fig_city_map.png")
    pd.set_option("display.width", 220)
    print(pd.DataFrame([refrow]).round(1).to_string(index=False))
    print(pd.DataFrame(sel_rows).to_string(index=False))
    print(pd.DataFrame(prof_rows).drop(columns="profile").to_string(index=False))
    print(summary.round(2).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
