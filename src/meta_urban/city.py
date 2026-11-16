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

from . import DATA_RAW, PAPER
from .bench import parse_json
from .endtoend import profile_check
from .io import leaf_concepts
from .llm import ROLE, _concept_block, complete, load_cache, t3_request

NYC = DATA_RAW / "nyc"
TAB, FIG = PAPER / "tables", PAPER / "figures"
MODELS = ["ollama:qwen3:8b", "ollama:llama3.1:8b"]
KBTU_TO_KWH, FT2_TO_M2 = 1 / 3.412141633, 0.09290304

# concepts the pipeline needs, the purpose shown to the model, and the columns that correctly hold each one
ROLES = {
    "bbl": ("record_identifier", "join each benchmarked property to New York City tax-lot (PLUTO) data",
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
PLUTO_ROLE = ("record_identifier", "join tax lots to benchmarked properties", {"bbl"})
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
def select_request(dataset: str, concept_id: str, purpose: str, level: str) -> dict:
    cols = columns(dataset)
    concept = next(c for c in leaf_concepts() if c["id"] == concept_id)
    block = "\n".join(f"{r.field}: {r.name}" for r in cols.itertuples())
    system = (f"{ROLE}\n\nTask: a data pipeline needs the column of a dataset that holds a given concept. Choose the "
              "single best column, or \"none\" if no column holds it.\n\n"
              f"DATASET COLUMNS (field: display name)\n{block}\n\n"
              'Output: {"column": <field or "none">, "confidence": <0 to 1>}')
    user = f"CONCEPT\n{_concept_block(level, [concept])}\n\nPURPOSE\n{purpose}"
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
TO_KWH = {"unit:BTU_IT": 1 / 3412.141633, "unit:KiloW-HR": 1.0}
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
            prof_rows.append(tag | {"column": field, "fields_wrong": "; ".join(wrong), "flags": "; ".join(flags),
                                    "profile": json.dumps(p)})
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
    pd.DataFrame(sel_rows).to_csv(TAB / "city_selection.csv", index=False)
    pd.DataFrame(prof_rows).to_csv(TAB / "city_profiles.csv", index=False)
    pd.DataFrame(dist_rows).to_csv(TAB / "city_district_errors.csv", index=False)
    summary.to_csv(TAB / "city_summary.csv", index=False)
    refrow = {k: ref[k] for k in ("records", "key_parsed", "usable", "linked", "eui_city", "elec_city", "gas_city",
                                  "area_m2")}
    pd.DataFrame([refrow]).to_csv(TAB / "city_reference.csv", index=False)
    rd.to_csv(TAB / "city_reference_districts.csv")
    pd.set_option("display.width", 220)
    print(pd.DataFrame([refrow]).round(1).to_string(index=False))
    print(pd.DataFrame(sel_rows).to_string(index=False))
    print(pd.DataFrame(prof_rows).drop(columns="profile").to_string(index=False))
    print(summary.round(2).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
