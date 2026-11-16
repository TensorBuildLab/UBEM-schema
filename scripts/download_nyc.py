"""Download the New York City data for the city-scale integration case (E8; data/raw/nyc/, git-ignored).

    python scripts/download_nyc.py           # download and record SHA-256 in data/nyc_manifest.json
    python scripts/download_nyc.py --verify  # check files against the manifest

Sources (NYC Open Data, Socrata API; public, no registration):
    LL84 benchmarking, dataset 5zyy-y8am: all 265 columns, calendar year 2023 (report_year = 2023)
    LL84 data dictionary (column names and descriptions), from the dataset's metadata endpoint
    PLUTO, dataset 64uk-42ks: tax-lot identifier, geography and building attributes (selected columns)
    PLUTO data dictionary, from the dataset's metadata endpoint
    Community districts, dataset 5crt-au7u: boundaries as GeoJSON
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
FILES = {
    "ll84_2023.csv": f"{API}/resource/5zyy-y8am.csv?$where=report_year=2023&$limit=100000",
    "ll84_columns.json": f"{API}/api/views/5zyy-y8am.json",
    "pluto.csv": f"{API}/resource/64uk-42ks.csv?$select={','.join(PLUTO_COLS)}&$limit=2000000",
    "pluto_columns.json": f"{API}/api/views/64uk-42ks.json",
    "community_districts.geojson": f"{API}/resource/5crt-au7u.geojson?$limit=1000",
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if "--verify" in sys.argv:
        man = json.loads(MANIFEST.read_text())
        bad = [f for f, m in man["files"].items() if sha256(OUT / f) != m["sha256"]]
        print("all files match" if not bad else f"changed: {bad}")
        return int(bool(bad))
    OUT.mkdir(parents=True, exist_ok=True)
    man = {"downloaded": date.today().isoformat(), "files": {}}
    for name, url in FILES.items():
        r = requests.get(url, timeout=600)
        r.raise_for_status()
        (OUT / name).write_bytes(r.content)
        man["files"][name] = {"url": url, "bytes": len(r.content), "sha256": sha256(OUT / name)}
        print(f"{name}: {len(r.content) / 1e6:.1f} MB")
    MANIFEST.write_text(json.dumps(man, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
