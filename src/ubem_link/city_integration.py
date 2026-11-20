"""E8b: four-source integration in New York City with the ubem-link tool (paper Section 7.4).

    python scripts/download_nyc.py && python scripts/download_nyc.py --only footprints,weather
    python scripts/download_nyc.py --geometry
    python -m ubem_link.city_integration

Sources, one per data category of the UBEM-Link taxonomy:
    LL84 2023 benchmarking (microscopic energy; 33,684 properties)        key: BBL (tax lot), BIN (building)
    PLUTO tax lots (building characteristics; 858,284 lots)               key: BBL; coordinates
    NYC building footprints (building stock geometry; 1,082,933 buildings) key: BIN; polygons, roof heights
    TMYx weather files of four New York City stations (weather)           key: nearest station by coordinates

The reference pipeline joins them into one row per benchmarked property with the inputs of a physics-based
UBEM: floor area, footprint area, roof height, floors, construction year, a weather file with its degree days,
and measured energy for calibration. The language model performs the integration steps on the three tabular
sources: for each input it chooses the column (selection, given the UBEM-Link definition) and builds the
column's profile (unit, multiplier, missing codes) with the tool's normalization prompt, under four context
conditions: the portal's column description only (entry), with every dataset convention as prose (card), with
only the conventions whose machine-readable scope covers the column (scoped), and scoped with the tool applying
the conventions' stated values deterministically (tool, the ubem-link default). The tool (prompts, unit
vocabulary, conventions of the PLUTO and footprint entries) was committed before any model saw these columns.
"""

from __future__ import annotations

import json
import os
import re
from functools import lru_cache

import numpy as np
import pandas as pd

from . import DATA_RAW, PAPER
from .city import EUI_RANGE, columns, gold_profile, ll84, select_request
from .integrate import nearest, polygon_area_m2, stations
from .io import load_catalog
from .llm import complete, load_cache, parse_json
from ._profiler_frozen import profile_checks as frozen_checks  # checks as frozen before this test
from .profiler import normalize_request, profile_checks, scoped_conventions
from .readers import Column, summarize
from .units import to_canonical

NYC = DATA_RAW / "nyc"
TAB, FIG = PAPER / "tables", PAPER / "figures"
MODELS = os.environ.get("UBEM_CITY_MODELS", "ollama:qwen3:8b,ollama:llama3.1:8b,ollama:qwen3:14b").split(",")
# Qwen3 14B was added after the 8B runs, with the same frozen prompts, as the larger-model check
ENTRY = {"ll84": "chr-nyc-ll84", "pluto": "chr-nyc-pluto", "footprints": "geo-nyc-footprints"}

# role -> (dataset, concept or join key, purpose, acceptable columns)
ROLES = {
    "ll84.bbl": ("ll84", "join:parcel_id", "join each benchmarked property to New York City tax-lot (PLUTO) data",
                 {"nyc_borough_block_and_lot"}),
    "ll84.bin": ("ll84", "join:building_id", "join each benchmarked property to New York City building footprints",
                 {"nyc_building_identification"}),
    "ll84.area": ("ll84", "gross_floor_area", "compute annual energy use intensity per unit floor area",
                  {"property_gfa_self_reported", "property_gfa_calculated", "property_gfa_calculated_1"}),
    "ll84.site": ("ll84", "total_energy_consumption", "compute annual site energy use intensity", {"site_energy_use_kbtu"}),
    "ll84.elec": ("ll84", "electricity_consumption", "compute annual electricity use intensity",
                  {"electricity_use_grid_purchase", "electricity_use_grid_purchase_1",
                   "electricity_use_grid_purchase_2", "electricity_use_grid_purchase_3"}),
    "ll84.gas": ("ll84", "natural_gas_consumption", "compute annual natural gas use intensity",
                 {"natural_gas_use_kbtu", "natural_gas_use_therms_"}),
    "pluto.bbl": ("pluto", "join:parcel_id", "join tax lots to benchmarked properties", {"bbl"}),
    "pluto.cd": ("pluto", "administrative_region", "aggregate results by community district", {"cd"}),
    "pluto.year": ("pluto", "year_of_construction", "group buildings by construction period", {"yearbuilt"}),
    "pluto.floors": ("pluto", "floors_above_ground", "give the number of floors of each building", {"numfloors"}),
    "pluto.lat": ("pluto", "geographic_coordinates",
                  "assign each building the nearest weather station; this column must give the latitude", {"latitude"}),
    "pluto.lon": ("pluto", "geographic_coordinates",
                  "assign each building the nearest weather station; this column must give the longitude", {"longitude"}),
    "footprints.bin": ("footprints", "join:building_id", "join building footprints to benchmarked properties", {"bin"}),
    "footprints.height": ("footprints", "building_height",
                          "build a block (LoD1) model of each building from its footprint and roof height", {"height_roof"}),
    "footprints.footprint": ("footprints", "footprint", "compute the footprint area of each building", {"the_geom"}),
    "footprints.year": ("footprints", "year_of_construction", "group buildings by construction period",
                        {"construction_year"}),
}
REF = {r: sorted(acc)[0] if r != "ll84.area" else "property_gfa_calculated_1" for r, (_, _, _, acc) in ROLES.items()}
REF |= {"ll84.elec": "electricity_use_grid_purchase_1", "ll84.gas": "natural_gas_use_kbtu"}
CONDITIONS = ["entry", "card", "scoped", "tool"]
ERAS = [(0, 1940, "before 1940"), (1940, 1980, "1940-1979"), (1980, 2010, "1980-2009"), (2010, 2100, "2010 or later")]


# ------------------------------------------------------------------------------------------------ data
@lru_cache
def pluto() -> pd.DataFrame:
    p = pd.read_csv(NYC / "pluto.csv", dtype=str, low_memory=False)
    p["bbl"] = p.bbl.str.replace(r"\.0+$", "", regex=True)
    return p


@lru_cache
def footprints() -> pd.DataFrame:
    return pd.read_csv(NYC / "footprints.csv", dtype=str, low_memory=False)


@lru_cache
def footprint_areas() -> pd.Series:
    """True footprint area (m²) per BIN, from the polygons (several polygons of one BIN are summed)."""
    g = json.loads((NYC / "footprints_ll84_geometry.geojson").read_text(encoding="utf-8"))
    rows = [(f["properties"]["bin"], polygon_area_m2(f["geometry"])) for f in g["features"]]
    return pd.DataFrame(rows, columns=["bin", "area"]).groupby("bin").area.sum()


@lru_cache
def weather() -> pd.DataFrame:
    return stations(sorted((NYC / "weather").glob("*.zip")))


def table(ds: str) -> pd.DataFrame:
    return {"ll84": ll84, "pluto": pluto, "footprints": footprints}[ds]()


def dictionary(ds: str) -> pd.DataFrame:
    return columns(ds)


@lru_cache
def entry(ds: str) -> dict:
    return next(e for e in load_catalog() if e["id"] == ENTRY[ds])


def column_doc(ds: str, field: str) -> Column:
    d = dictionary(ds).set_index("field")
    s = table(ds)[field] if field in table(ds) else pd.Series(dtype=str)
    summ, lo, hi, distinct = summarize(s)
    return Column(field, label=d.loc[field, "name"] if field in d.index else field,
                  description=d.loc[field, "description"] if field in d.index else "",
                  value_summary=summ, value_min=lo, value_max=hi, distinct_values=distinct)


# ------------------------------------------------------------------------------------------------ gold
def gold(ds: str, field: str) -> dict:
    """Reference profile of a column (unit, multiplier, missing codes, do_not_use)."""
    if ds == "ll84":
        if field in ("nyc_borough_block_and_lot", "nyc_building_identification"):
            return {"unit": "none", "unit_multiplier": 0, "missing_codes": ["Not Available"] +
                    ([f"{b}000000" for b in range(1, 6)] if field == "nyc_building_identification" else [])}
        return gold_profile(field)
    g = {"unit": "none", "unit_multiplier": 0, "missing_codes": []}
    if ds == "pluto":
        if field == "yearbuilt":
            g["missing_codes"] = ["0"]
        if field in ("bldgarea", "resarea", "comarea"):
            g.update(unit="unit:FT2", unit_multiplier=1, missing_codes=["0"])
    if ds == "footprints":
        if field in ("height_roof", "ground_elevation"):
            g.update(unit="unit:FT", unit_multiplier=1, missing_codes=["0"])
        if field == "construction_year":
            g["missing_codes"] = ["0"]
        if field == "bin":
            g["missing_codes"] = [f"{b}000000" for b in range(1, 6)]
        if field in ("shape_area", "shape_length"):
            g["do_not_use"] = True
    return g


# ------------------------------------------------------------------------------------------------ values
def _clean(s: pd.Series, prof: dict) -> pd.Series:
    miss = {str(c) for c in prof.get("missing_codes") or [] if str(c) != ""}
    return s.where(~s.astype(str).str.strip().isin(miss))


def quantity(ds: str, field: str, prof: dict, kind_hint: str) -> pd.Series:
    """Values of a column in canonical units under a profile. kind_hint: 'kwh', 'm2', 'm' or 'raw'."""
    x = pd.to_numeric(_clean(table(ds)[field], prof), errors="coerce")
    if prof.get("do_not_use"):  # as in `ubem-link apply`: a column the publisher says not to use gives no values
        return pd.Series(np.nan, index=x.index)
    u, m = prof.get("unit") or "none", prof.get("unit_multiplier") or 1
    if kind_hint == "raw":
        if u != "none":
            conv, _ = to_canonical(x, u, m)
            return conv if conv is not None else x
        return x
    if u == "none":
        return x * float(m or 1)
    conv, cu = to_canonical(x, u, m)
    want = {"kwh": "unit:KiloW-HR", "m2": "unit:M2", "m": "unit:M"}[kind_hint]
    return conv if cu == want else pd.Series(np.nan, index=x.index)


def keys(ds: str, field: str, prof: dict, multi: bool) -> pd.Series:
    miss = {str(c) for c in prof.get("missing_codes") or [] if str(c) != ""}

    def clean(v):
        if not isinstance(v, str):
            return [] if multi else None
        raw = [p.strip() for p in re.split(r"[;,]", v) if p.strip() and p.strip() not in miss]
        parts = [re.sub(r"\.0+$", "", re.sub(r"[\s\u00a0-]", "", p)) for p in raw]
        parts = [p for p in parts if p and p not in miss]
        return parts if multi else (parts[0] if parts else None)

    return table(ds)[field].map(clean)


def run(sel: dict, prof: dict) -> dict:
    """The integration pipeline. sel: role -> column; prof: (dataset, column) -> profile."""
    P = lambda role: prof[(ROLES[role][0], sel[role])]  # noqa: E731
    d = ll84()
    n = len(d)
    rep = {"records": n}
    if any(sel.get(r, "none") == "none" for r in ("ll84.bbl", "ll84.area", "ll84.site")):
        return rep | {"failed": True}
    area = quantity("ll84", sel["ll84.area"], P("ll84.area"), "m2")
    site = quantity("ll84", sel["ll84.site"], P("ll84.site"), "kwh")
    gas = quantity("ll84", sel["ll84.gas"], P("ll84.gas"), "kwh") if sel.get("ll84.gas", "none") != "none" else pd.Series(np.nan, index=d.index)
    eui = site / area
    usable = (area > 0) & eui.between(*EUI_RANGE)
    out = pd.DataFrame({"area": area, "site": site, "gas": gas}, index=d.index)[usable]
    # PLUTO through the first BBL
    if sel.get("pluto.bbl", "none") != "none" and sel["pluto.bbl"] in pluto():
        lk = keys("ll84", sel["ll84.bbl"], P("ll84.bbl"), multi=False)[usable]
        pk = keys("pluto", sel["pluto.bbl"], P("pluto.bbl"), multi=False)
        cols = {r.split(".")[1]: sel[r] for r in ("pluto.cd", "pluto.year", "pluto.floors", "pluto.lat", "pluto.lon")
                if sel.get(r, "none") in pluto()}
        lots = pd.DataFrame({name: (quantity("pluto", c, P(f"pluto.{name}"), "raw") if name != "cd" else pluto()[c])
                             for name, c in cols.items()})
        lots["_k"] = pk
        lots = lots.dropna(subset=["_k"]).drop_duplicates("_k").set_index("_k")
        j = lots.reindex(lk.values)
        j.index = out.index
        out = out.join(j)
        rep["linked_pluto"] = int(j.notna().any(axis=1).sum())
    else:
        rep["linked_pluto"] = 0
    # footprints through all BINs of a property
    if sel.get("ll84.bin", "none") != "none" and sel.get("footprints.bin", "none") in footprints():
        lb = keys("ll84", sel["ll84.bin"], P("ll84.bin"), multi=True)[usable]
        fb = keys("footprints", sel["footprints.bin"], P("footprints.bin"), multi=False)
        fp = pd.DataFrame({"_k": fb})
        if sel.get("footprints.height", "none") in footprints():
            fp["height"] = quantity("footprints", sel["footprints.height"], P("footprints.height"), "m")
        fsel = sel.get("footprints.footprint", "none")
        if fsel == "the_geom":
            fp["fp_area"] = fb.map(footprint_areas())
        elif fsel in footprints():
            fp["fp_area"] = quantity("footprints", fsel, P("footprints.footprint"), "m2")
        if sel.get("footprints.year", "none") in footprints():
            fp["fp_year"] = quantity("footprints", sel["footprints.year"], P("footprints.year"), "raw")
        fp = fp.dropna(subset=["_k"])
        ex = lb.explode().dropna()
        m = pd.DataFrame({"row": ex.index, "_k": ex.values}).merge(fp, on="_k", how="inner")
        gb = m.groupby("row")
        g = pd.DataFrame({k: (gb[k].sum(min_count=1) if f == "sum" else gb[k].agg(f))
                          for k, f in {"height": "max", "fp_area": "sum", "fp_year": "min"}.items() if k in m})
        if {"height", "fp_area"} <= set(m):
            m["vol"] = m.height * m.fp_area
            g["volume"] = m.groupby("row").vol.sum(min_count=1)
        out = out.join(g)
        rep["linked_footprints"] = int(g.index.nunique())
    else:
        rep["linked_footprints"] = 0
    # weather: nearest station to the lot's coordinates
    if {"lat", "lon"} <= set(out):
        st = weather()
        k, dist = nearest(out.lat, out.lon, st)
        good = (k >= 0) & (dist < 50)
        out["hdd"] = np.where(good, st.hdd18.values[np.clip(k.values, 0, None)], np.nan)
        out["station"] = np.where(good, st.station.values[np.clip(k.values, 0, None)], None)
        rep["linked_weather"] = int(good.sum())
    else:
        rep["linked_weather"] = 0
    need = [c for c in ("cd", "year", "floors", "height", "fp_area", "hdd") if c in out]
    complete_ = out[need].notna().all(axis=1) if len(need) == 6 else pd.Series(False, index=out.index)
    rep |= {"failed": False, "usable": int(usable.sum()), "complete": int(complete_.sum()), "table": out}
    return rep


def indicators(res: dict) -> dict:
    """UBEM inputs and calibration indicators of the integrated table."""
    if res.get("failed"):
        return {}
    t = res["table"]
    ind = {"linked_pluto": res["linked_pluto"], "linked_footprints": res["linked_footprints"],
           "linked_weather": res["linked_weather"], "complete_inputs": res["complete"]}
    if "year" in t:
        y = t.year
        for lo, hi, lab in ERAS:
            sel = y.between(lo, hi - 1)
            ind[f"floor_area_share_{lab}"] = 100 * t.area[sel].sum() / t.area[y.notna()].sum()
            ind[f"eui_{lab}"] = t.site[sel].sum() / t.area[sel].sum()
    if "height" in t:
        ind["median_height_m"] = float(t.height[t.height > 0].median())
        if "floors" in t:
            hpf = (t.height / t.floors).where((t.floors > 0) & (t.height > 0))
            ind["median_height_per_floor_m"] = float(hpf.median())
    if {"fp_area", "floors"} <= set(t):
        ratio = (t.area / (t.fp_area * t.floors)).where((t.fp_area > 0) & (t.floors > 0))
        ind["median_gfa_to_footprint_x_floors"] = float(ratio.median())
    if "volume" in t:
        ind["total_volume_million_m3"] = float(t.volume.sum() / 1e6)
        ind["median_surface_to_volume"] = np.nan
    if {"hdd", "gas"} <= set(t):
        ok = t.hdd.notna() & t.gas.notna() & (t.gas > 0)
        ind["gas_per_m2_hdd"] = float(t.gas[ok].sum() / (t.area[ok] * t.hdd[ok]).sum())
    return {k: v for k, v in ind.items() if not (isinstance(v, float) and np.isnan(v))}


# ------------------------------------------------------------------------------------------------ model calls
def select_all(model: str, cache: dict) -> dict:
    sel = {}
    for role, (ds, target, purpose, _) in ROLES.items():
        meta = {"task": "E8-select", "dataset": f"nyc_{ds}", "name": role.split(".")[1] if ds != "ll84" else role.split(".")[1],
                "level": "L2"}
        if role in ("ll84.bbl", "ll84.area", "ll84.site", "ll84.elec", "ll84.gas", "pluto.bbl"):
            meta["name"] = role.split(".")[1]  # same request as E8, answered from the cache
        r = complete(model, select_request(ds, target, purpose, "L2"), meta, 0, cache)
        sel[role] = (parse_json(r["response"]) or {}).get("column", "none")
    return sel


def profile_column(model: str, ds: str, field: str, condition: str, cache: dict) -> tuple[dict, dict]:
    """(model answer, profile used by the pipeline) for one column under one condition."""
    col = column_doc(ds, field)
    e = entry(ds)
    convs = scoped_conventions(e, col)
    mode = {"entry": "none", "card": "card", "scoped": "scoped", "tool": "scoped"}[condition]
    shown = convs if mode == "scoped" else (e.get("conventions") or [])
    req = normalize_request(col, f"nyc_{ds}", shown, mode)
    task = {"none": "E8b-norm-entry", "card": "E8b-norm-card", "scoped": "E8b-norm-scoped"}[mode]
    r = complete(model, req, {"task": task, "dataset": f"nyc_{ds}", "name": field}, 0, cache)
    js = parse_json(r["response"]) or {}
    ans = {"unit": js.get("unit") or "none", "unit_multiplier": js.get("unit_multiplier") or 0,
           "missing_codes": [str(c) for c in js.get("missing_codes") or []]}
    used = json.loads(json.dumps(ans))
    if condition == "tool":
        for c in convs:
            for code in c.get("missing_codes") or []:
                if str(code) not in used["missing_codes"]:
                    used["missing_codes"].append(str(code))
            if c.get("unit"):
                used["unit"], used["unit_multiplier"] = c["unit"], c.get("unit_multiplier") or 1
            if c.get("convention_type") == "do_not_use":
                used["do_not_use"] = True
    return ans, used


def profile_status(ds: str, field: str, p: dict) -> str:
    """'error', 'harmless deviation' or 'exact' against the gold profile."""
    g = gold(ds, field)
    s = table(ds)[field].astype(str).str.strip() if field in table(ds) else pd.Series(dtype=str)
    if g.get("do_not_use"):
        return "exact" if p.get("do_not_use") else "error"
    gf = to_canonical(1.0, g["unit"], g["unit_multiplier"])[0] if g["unit"] != "none" else None
    pf = to_canonical(1.0, p["unit"], p["unit_multiplier"])[0] if p["unit"] != "none" else None
    unit_wrong = (gf is not None and (pf is None or abs(pf / gf - 1) > 1e-6)) or \
                 (gf is None and pf is not None and p["unit"] not in ("unit:DEG",) and abs(pf - 1) > 1e-9)
    counts = s.value_counts()
    keeps_invalid = any(counts.get(c, 0) > 0 and c not in p["missing_codes"] for c in g["missing_codes"] if c)
    # a frequent numeric value declared missing drops valid records, except a zero floor area, which the
    # pipeline excludes anyway (it cannot be a denominator of energy use intensity)
    zero_ok = {"0"} if ds == "ll84" and "gfa" in field or field == "bldgarea" else set()
    drops_valid = any(counts.get(c, 0) >= 10 and c not in g["missing_codes"] and c not in zero_ok and
                      pd.notna(pd.to_numeric(c, errors="coerce")) for c in p["missing_codes"] if c)
    if unit_wrong or keeps_invalid or drops_valid:
        return "error"
    return "exact" if sorted(c for c in p["missing_codes"] if c) == sorted(g["missing_codes"]) else "harmless deviation"


NUMERIC_ROLES = ["ll84.bbl", "ll84.bin", "ll84.area", "ll84.site", "ll84.elec", "ll84.gas", "pluto.bbl", "pluto.year",
                 "pluto.floors", "pluto.lat", "pluto.lon", "footprints.bin", "footprints.height", "footprints.footprint",
                 "footprints.year"]


def main() -> int:
    ref_prof = {(ROLES[r][0], c): gold(ROLES[r][0], c) for r, c in REF.items()}
    ref = run(REF, ref_prof)
    ref_ind = indicators(ref)
    rows_sel, rows_prof, rows_ind = [], [], []
    rows_ind.append({"model": "reference", "condition": "reference", **ref_ind,
                     "usable": ref["usable"], "complete": ref["complete"]})
    for model in MODELS:
        cache = load_cache(model)
        sel = select_all(model, cache)
        mname = model.split(":", 1)[1]
        for role, col in sel.items():
            rows_sel.append({"model": mname, "role": role, "column": col, "reference": REF[role],
                             "correct": col in ROLES[role][3]})
        # selection only: model columns with gold profiles
        gp = {(ROLES[r][0], c): gold(ROLES[r][0], c) for r, c in sel.items() if c != "none"}
        res = run(sel, gp)
        rows_ind.append({"model": mname, "condition": "selection only (gold profiles)", **indicators(res),
                         "usable": res.get("usable"), "complete": res.get("complete")})
        for condition in CONDITIONS:
            for variant, columns_ in (("model columns", sel), ("reference columns", REF)):
                prof = {}
                for role in NUMERIC_ROLES:
                    c = columns_.get(role, "none")
                    ds = ROLES[role][0]
                    if c == "none" or c not in table(ds) and c != "the_geom":
                        continue
                    if c == "the_geom":
                        prof[(ds, c)] = {"unit": "none", "unit_multiplier": 0, "missing_codes": []}
                        continue
                    ans, used = profile_column(model, ds, c, condition, cache)
                    prof[(ds, c)] = used
                    if variant == "reference columns" and condition == "tool":
                        # the tool's review flags on the model's own answer (before conventions are applied)
                        col = column_doc(ds, c)
                        convs = scoped_conventions(entry(ds), col)
                        disagree = [f"convention set unit {cv['unit']}" for cv in convs
                                    if cv.get("unit") and (cv["unit"], float(cv.get("unit_multiplier") or 1))
                                    != (ans["unit"], float(ans["unit_multiplier"] or 1))]
                        flags = profile_checks(col, ans, ROLES[role][1], convs) + disagree
                        flags_frozen = frozen_checks(col, ans, ROLES[role][1], convs) + disagree
                    else:
                        flags = flags_frozen = None
                    if variant == "reference columns":
                        rows_prof.append({"model": mname, "condition": condition, "dataset": ds, "column": c,
                                          "unit": used["unit"], "multiplier": used["unit_multiplier"],
                                          "missing_codes": "; ".join(used["missing_codes"]),
                                          "model_unit": ans["unit"], "model_multiplier": ans["unit_multiplier"],
                                          "status": profile_status(ds, c, used),
                                          "status_model_answer": profile_status(ds, c, ans),
                                          "review_flags_on_answer": None if flags is None else "; ".join(flags),
                                          "review_flags_frozen": None if flags_frozen is None else "; ".join(flags_frozen)})
                res = run(columns_, prof)
                rows_ind.append({"model": mname, "condition": f"{condition}, {variant}", **indicators(res),
                                 "usable": res.get("usable"), "complete": res.get("complete")})
    ind = pd.DataFrame(rows_ind)
    ind.to_csv(TAB / "city4_indicators.csv", index=False)
    pd.DataFrame(rows_sel).to_csv(TAB / "city4_selection.csv", index=False)
    pd.DataFrame(rows_prof).to_csv(TAB / "city4_profiles.csv", index=False)
    pd.DataFrame([{"links": "reference", **{k: ref[k] for k in ("records", "usable", "linked_pluto",
                                                                  "linked_footprints", "linked_weather", "complete")}}]) \
        .to_csv(TAB / "city4_reference.csv", index=False)
    weather().drop(columns=["source"]).to_csv(TAB / "city4_weather_stations.csv", index=False)
    pd.set_option("display.width", 250)
    print(pd.DataFrame(rows_sel).to_string(index=False))
    print(pd.DataFrame(rows_prof).to_string(index=False))
    print(ind.round(3).T.to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
