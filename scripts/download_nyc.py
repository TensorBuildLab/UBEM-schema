"""Download the New York City data for the city-scale integration case (E8; data/raw/nyc/, git-ignored).

    python scripts/download_nyc.py           # download and record SHA-256 in data/nyc_manifest.json
    python scripts/download_nyc.py --verify  # check files against the manifest

Sources (NYC Open Data, Socrata API; public, no registration):
    LL84 benchmarking, dataset 5zyy-y8am: all 265 columns, calendar year 2023 (report_year = 2023)
    LL84 data dictionary (column names and descriptions), from the dataset's metadata endpoint
    PLUTO, dataset 64uk-42ks: tax-lot identifier, geography and building attributes (selected columns)
    PLUTO data dictionary, from the dataset's metadata endpoint
    Community districts, dataset 5crt-au7u: boundaries as GeoJSON
    Building footprints, dataset 5zhs-2jue: identifiers, roof height, ground elevation, construction year and
        footprint area of every building (selected columns, no geometry)
    Building footprints data dictionary, from the dataset's metadata endpoint
    Weather: TMYx 2009-2023 EPW files of four New York City stations (climate.onebuilding.org)

    Footprint polygons of the buildings named in LL84 (BIN-filtered queries of dataset 5zhs-2jue, GeoJSON)

    python scripts/download_nyc.py --only footprints,weather   # download a subset of the files
    python scripts/download_nyc.py --geometry                  # footprint polygons of LL84 buildings
"""
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "nyc"
MANIFEST = ROOT / "data" / "nyc_manifest.json"
API = "https://data.cityofnewyork.us"
PLUTO_COLS = ["bbl", "borough", "cd", "bct2020", "zipcode", "bldgclass", "landuse", "yearbuilt", "numfloors",
              "numbldgs", "bldgarea", "resarea", "comarea", "latitude", "longitude", "version"]
FOOTPRINT_COLS = ["bin", "base_bbl", "mappluto_bbl", "height_roof", "ground_elevation", "construction_year",
                  "feature_code", "shape_area", "geom_source", "last_status_type"]
OB = ("https://climate.onebuilding.org/WMO_Region_4_North_and_Central_America/USA_United_States_of_America/"
      "NY_New_York/")
STATIONS = ["USA_NY_New.York-Central.Park.Obs-Belvedere.Castle.725053", "USA_NY_New.York-LaGuardia.AP.725030",
            "USA_NY_New.York-Kennedy.Intl.AP.744860", "USA_NY_New.York-Downtown.Manhattan.Heli.720553"]
FILES = {
    "ll84_2023.csv": f"{API}/resource/5zyy-y8am.csv?$where=report_year=2023&$limit=100000",
    "ll84_columns.json": f"{API}/api/views/5zyy-y8am.json",
    "pluto.csv": f"{API}/resource/64uk-42ks.csv?$select={','.join(PLUTO_COLS)}&$limit=2000000",
    "pluto_columns.json": f"{API}/api/views/64uk-42ks.json",
    "community_districts.geojson": f"{API}/resource/5crt-au7u.geojson?$limit=1000",
    "footprints.csv": f"{API}/resource/5zhs-2jue.csv?$select={','.join(FOOTPRINT_COLS)}&$limit=2000000",
    "footprints_columns.json": f"{API}/api/views/5zhs-2jue.json",
    **{f"weather/{s}_TMYx.2009-2023.zip": f"{OB}{s}_TMYx.2009-2023.zip" for s in STATIONS},
}
GROUPS = {"footprints": ("footprints",), "weather": ("weather/",)}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def footprint_geometry() -> None:
    """Polygons of the footprints whose BIN appears in LL84 (queried in batches; about 40,000 buildings)."""
    import re
    import time

    import pandas as pd

    ll = pd.read_csv(OUT / "ll84_2023.csv", dtype=str, usecols=["nyc_building_identification"])
    pat = re.compile("(?<![0-9])[1-5][0-9]{6}(?![0-9])")
    bins = sorted({b for v in ll.nyc_building_identification.dropna() for b in pat.findall(v)
                   if not b.endswith("000000")})
    feats = []
    for k in range(0, len(bins), 250):
        q = ",".join(f"'{b}'" for b in bins[k:k + 250])
        url = f"{API}/resource/5zhs-2jue.geojson?$select=bin,base_bbl,the_geom&$where=bin in({q})&$limit=5000"
        r = requests.get(url, timeout=300, headers={"User-Agent": "ubem-link-benchmark/1.0"})
        r.raise_for_status()
        feats += r.json()["features"]
        time.sleep(0.2)
    path = OUT / "footprints_ll84_geometry.geojson"
    path.write_text(json.dumps({"type": "FeatureCollection", "features": feats}), encoding="utf-8")
    man = json.loads(MANIFEST.read_text())
    man["files"][path.name] = {"url": f"{API}/resource/5zhs-2jue.geojson (bin in LL84 BINs, {len(bins)} BINs)",
                               "bytes": path.stat().st_size, "sha256": sha256(path),
                               "downloaded": date.today().isoformat()}
    MANIFEST.write_text(json.dumps(man, indent=2))
    print(f"{path.name}: {len(feats)} footprints of {len(bins)} BINs, {path.stat().st_size / 1e6:.1f} MB")


def main() -> int:
    if "--geometry" in sys.argv:
        footprint_geometry()
        return 0
    if "--verify" in sys.argv:
        man = json.loads(MANIFEST.read_text())
        bad = [f for f, m in man["files"].items() if sha256(OUT / f) != m["sha256"]]
        print("all files match" if not bad else f"changed: {bad}")
        return int(bool(bad))
    files = FILES
    if "--only" in sys.argv:
        prefixes = tuple(p for g in sys.argv[sys.argv.index("--only") + 1].split(",") for p in GROUPS[g])
        files = {k: v for k, v in FILES.items() if k.startswith(prefixes)}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "weather").mkdir(exist_ok=True)
    man = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"files": {}}
    for name, url in files.items():
        r = requests.get(url, timeout=900, headers={"User-Agent": "ubem-link-benchmark/1.0"})
        r.raise_for_status()
        (OUT / name).write_bytes(r.content)
        man["files"][name] = {"url": url, "bytes": len(r.content), "sha256": sha256(OUT / name),
                              "downloaded": date.today().isoformat()}
        print(f"{name}: {len(r.content) / 1e6:.1f} MB")
    MANIFEST.write_text(json.dumps(man, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
