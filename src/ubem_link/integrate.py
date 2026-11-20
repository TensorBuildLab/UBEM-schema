"""Integrate several profiled datasets into one table for UBEM, following a recipe.

A recipe (YAML) names the datasets, the columns the integration needs (by concept or join key, resolved from
each dataset's profile or chosen explicitly), and the links between datasets:

    base: ll84
    datasets:
      ll84:       {data: ll84.csv, profile: ll84.ubem.yaml}
      pluto:      {data: pluto.csv, profile: pluto.ubem.yaml}
      footprints: {data: footprints.csv, profile: footprints.ubem.yaml}
      weather:    {epw: [weather/*.zip]}
    needs:                      # output column: [dataset, concept, optional explicit column]
      floor_area: [ll84, gross_floor_area, property_gfa_calculated_1]
      year_built: [pluto, year_of_construction]
    links:
      - {from: ll84, to: pluto, key: parcel_id, multi: first}       # key column found from join_key in profiles
      - {from: ll84, to: footprints, key: building_id, multi: all, aggregate: {height: max, footprint_area: sum}}
      - {from: pluto, to: weather, nearest: true}                    # nearest station by coordinates

Keys are cleaned before joining: a property may list several identifiers separated by ';' or ','
(multi: first or all), hyphens are removed, and identifier placeholders declared as missing codes in the profile
(for example NYC's "million BINs") never match. Every link reports how many records found a partner.
"""

from __future__ import annotations

import io
import math
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from .apply import apply_profile


# ------------------------------------------------------------------------------------------------ keys
def split_keys(s: pd.Series, multi: str = "first", placeholders: set[str] | None = None) -> pd.Series:
    """Clean identifier values; with multi='all' returns lists of identifiers."""
    placeholders = placeholders or set()

    def clean(x):
        if not isinstance(x, str) or not x.strip():
            return [] if multi == "all" else None
        raw = [p.strip() for p in re.split(r"[;,]", x) if p.strip() and p.strip() not in placeholders]
        parts = [re.sub(r"\.0$", "", re.sub(r"[\s\u00a0-]", "", p)) for p in raw]
        parts = [p for p in parts if p and p not in placeholders]
        if multi == "all":
            return parts
        return parts[0] if parts else None

    return s.astype("string").astype(object).map(clean)


def find_column(variables: list[dict], concept: str | None = None, join_key: str | None = None) -> str | None:
    """Column of a profile that holds a concept or join key (highest confidence first)."""
    hits = [v for v in variables if (concept and v.get("concept") == concept) or (join_key and v.get("join_key") == join_key)]
    hits = [v for v in hits if not v.get("do_not_use")]
    if not hits:
        return None
    return sorted(hits, key=lambda v: -(v.get("confidence") or 0))[0]["name"]


# ------------------------------------------------------------------------------------------------ weather
EPW_COLUMNS = ["year", "month", "day", "hour", "minute", "flags", "dry_bulb_c", "dew_point_c", "rel_humidity_pct",
               "pressure_pa", "extra_horiz_rad", "extra_dni", "horiz_ir", "ghi_wh_m2", "dni_wh_m2", "dhi_wh_m2",
               "glob_illum", "dir_illum", "diff_illum", "zenith_lum", "wind_dir_deg", "wind_speed_m_s"]


def read_epw(path: str | Path) -> tuple[dict, pd.DataFrame]:
    """Read an EPW file (or the .epw inside a zip): station header and hourly records."""
    p = Path(path)
    if p.suffix.lower() == ".zip":
        with zipfile.ZipFile(p) as z:
            name = next(n for n in z.namelist() if n.lower().endswith(".epw"))
            text = z.read(name).decode("latin-1")
    else:
        text = p.read_text(encoding="latin-1")
    lines = text.splitlines()
    h = lines[0].split(",")
    head = {"station": h[1], "state": h[2], "country": h[3], "source": h[4], "wmo": h[5],
            "latitude": float(h[6]), "longitude": float(h[7]), "tz": float(h[8]), "elevation_m": float(h[9]),
            "file": p.name}
    data = pd.read_csv(io.StringIO("\n".join(lines[8:])), header=None)
    data = data.iloc[:, :len(EPW_COLUMNS)]
    data.columns = EPW_COLUMNS
    return head, data


def degree_days(data: pd.DataFrame, base_c: float = 18.0) -> tuple[float, float]:
    """Heating and cooling degree days from daily mean dry-bulb temperature (base 18 °C)."""
    daily = data.groupby(["month", "day"]).dry_bulb_c.mean()
    return float((base_c - daily).clip(lower=0).sum()), float((daily - base_c).clip(lower=0).sum())


def stations(paths: list[str | Path]) -> pd.DataFrame:
    rows = []
    for p in paths:
        head, data = read_epw(p)
        hdd, cdd = degree_days(data)
        rows.append({**head, "hdd18": hdd, "cdd18": cdd, "mean_temp_c": float(data.dry_bulb_c.mean())})
    return pd.DataFrame(rows)


def nearest(lat: pd.Series, lon: pd.Series, st: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Index of the nearest station (haversine) and the distance in km, for each point."""
    la, lo = np.radians(lat.astype(float).values)[:, None], np.radians(lon.astype(float).values)[:, None]
    sla, slo = np.radians(st.latitude.values)[None, :], np.radians(st.longitude.values)[None, :]
    a = np.sin((sla - la) / 2) ** 2 + np.cos(la) * np.cos(sla) * np.sin((slo - lo) / 2) ** 2
    d = 2 * 6371.0 * np.arcsin(np.sqrt(a))
    d = np.where(np.isnan(d), np.inf, d)
    k = d.argmin(axis=1)
    dist = d[np.arange(len(k)), k]
    ok = np.isfinite(dist)
    return pd.Series(np.where(ok, k, -1), index=lat.index), pd.Series(np.where(ok, dist, np.nan), index=lat.index)


# ------------------------------------------------------------------------------------------------ geometry
def polygon_area_m2(geom) -> float:
    """Area of a GeoJSON (Multi)Polygon in WGS84, in m², on a local equirectangular projection (error well below
    0.1% at city scale)."""
    if not geom:
        return math.nan
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    total = 0.0
    for poly in polys:
        for k, ring in enumerate(poly):
            xy = np.asarray(ring, dtype=float)
            lat0 = np.radians(xy[:, 1].mean())
            x = np.radians(xy[:, 0]) * 6371008.8 * math.cos(lat0)
            y = np.radians(xy[:, 1]) * 6371008.8
            a = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
            total += a if k == 0 else -a
    return total


# ------------------------------------------------------------------------------------------------ recipe
def link_report(name: str, n_from: int, n_linked: int) -> dict:
    return {"link": name, "records": n_from, "linked": n_linked, "linked_pct": 100 * n_linked / max(n_from, 1)}


def join_on_key(left: pd.DataFrame, lkey: pd.Series, right: pd.DataFrame, rkey: pd.Series, how_multi: str,
                aggregate: dict | None = None) -> tuple[pd.DataFrame, int]:
    """Attach right-hand columns to left records through cleaned keys. With multi='all', each left record may
    match several right records, aggregated column by column (sum, max, mean, first)."""
    r = right.assign(_k=rkey.values).dropna(subset=["_k"])
    if how_multi == "all":
        ex = left.assign(_k=lkey.values).explode("_k").dropna(subset=["_k"])
        m = ex[["_k"]].reset_index().merge(r, on="_k", how="inner")
        agg = {c: (aggregate or {}).get(c, "first") for c in r.columns if c != "_k"}
        g = m.groupby("index").agg(agg)
        return left.join(g, how="left"), int(g.index.nunique())
    r = r.drop_duplicates("_k").set_index("_k")
    g = r.reindex(lkey.values)
    g.index = left.index
    return left.join(g, how="left"), int(g.notna().any(axis=1).sum())


def _load_profile(path: str | Path) -> dict:
    import yaml

    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _coords(variables: list[dict], df: pd.DataFrame, spec: dict) -> tuple[str | None, str | None]:
    if spec.get("lat") and spec.get("lon"):
        return spec["lat"], spec["lon"]
    cand = [v["name"] for v in variables if v.get("concept") == "geographic_coordinates"] or list(df.columns)
    lat = next((c for c in cand if re.search(r"lat", c, re.I)), None)
    lon = next((c for c in cand if re.search(r"lon|lng", c, re.I)), None)
    return lat, lon


def run_recipe(recipe: dict, base_dir: str | Path = ".") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run an integration recipe; returns (integrated table, link report)."""
    from .readers import read_table

    base_dir = Path(base_dir)
    data, profiles, normalized = {}, {}, {}
    for name, spec in recipe["datasets"].items():
        if "epw" in spec:
            files = [p for pat in spec["epw"] for p in sorted(base_dir.glob(pat))]
            data[name] = stations(files)
            continue
        df = read_table(base_dir / spec["data"])
        prof = _load_profile(base_dir / spec["profile"])
        profiles[name] = prof.get("variables", [])
        data[name] = df
        normalized[name], _ = apply_profile(df, profiles[name])
    base = recipe["base"]
    out = pd.DataFrame(index=data[base].index)
    reports = []
    # columns each dataset contributes
    needs: dict[str, dict[str, str]] = {}
    for col, spec in (recipe.get("needs") or {}).items():
        ds, concept = spec[0], spec[1]
        src = spec[2] if len(spec) > 2 else find_column(profiles.get(ds, []), concept=concept)
        if src is None:
            reports.append({"link": f"need {col}", "records": 0, "linked": 0, "linked_pct": 0.0,
                            "note": f"no column of {ds} maps to {concept}"})
            continue
        needs.setdefault(ds, {})[col] = src
    tables = {ds: (normalized[ds][list(cols.values())].rename(columns={v: k for k, v in cols.items()})
                   if ds in normalized else None) for ds, cols in needs.items()}
    current = {base: tables.get(base, pd.DataFrame(index=out.index))}
    out = current[base].copy()
    origin = {base: out.index.to_series()}  # row of each dataset that each output row is linked to (for chaining)
    for link in recipe.get("links") or []:
        a, b = link["from"], link["to"]
        if link.get("nearest"):
            src = data[a] if a == base else None
            lat_c, lon_c = _coords(profiles.get(a, []), data[a], link)
            if a == base:
                lat, lon = normalized[a][lat_c], normalized[a][lon_c]
            else:
                lat = out.get(f"{a}.__lat")
                lon = out.get(f"{a}.__lon")
            st = data[b]
            k, dist = nearest(pd.to_numeric(lat, errors="coerce"), pd.to_numeric(lon, errors="coerce"), st)
            for c in ("station", "wmo", "hdd18", "cdd18", "mean_temp_c", "file"):
                out[f"{b}.{c}"] = np.where(k.values >= 0, st[c].values[np.clip(k.values, 0, None)], None)
            out[f"{b}.distance_km"] = dist.values
            reports.append(link_report(f"{a} -> {b} (nearest station)", len(out), int((k >= 0).sum())))
            del src
            continue
        lprof, rprof = profiles[a], profiles[b]
        lcol = link.get("from_column") or find_column(lprof, join_key=link["key"])
        rcol = link.get("to_column") or find_column(rprof, join_key=link["key"])
        if lcol is None or rcol is None:
            reports.append({"link": f"{a} -> {b} ({link['key']})", "records": len(out), "linked": 0,
                            "linked_pct": 0.0, "note": f"no {link['key']} column in {a if lcol is None else b}"})
            continue
        ph = lambda prof, c: {str(m) for v in prof if v["name"] == c for m in (v.get("missing_codes") or [])}  # noqa: E731
        multi = link.get("multi", "first")
        lkey = split_keys(data[a][lcol], multi, ph(lprof, lcol))
        if a != base:  # chain: key of the record of `a` linked to each output row
            lkey = out[f"{a}.__key"] if f"{a}.__key" in out else pd.Series(None, index=out.index)
        rkey = split_keys(data[b][rcol], "first", ph(rprof, rcol))
        right = tables.get(b, pd.DataFrame(index=data[b].index)).copy()
        lat_c, lon_c = _coords(rprof, data[b], {})
        if lat_c and lon_c:
            right["__lat"], right["__lon"] = normalized[b][lat_c], normalized[b][lon_c]
        right["__key"] = rkey
        right = right.add_prefix(f"{b}.")
        agg = {f"{b}.{k}": v for k, v in (link.get("aggregate") or {}).items()}
        joined, n = join_on_key(out, lkey.reindex(out.index), right, rkey, multi, agg)
        out = joined
        reports.append(link_report(f"{a} -> {b} ({link['key']}: {lcol} = {rcol})", len(out), n))
    out = out[[c for c in out.columns if "__" not in c]]
    return out, pd.DataFrame(reports)
