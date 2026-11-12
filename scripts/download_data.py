"""Download the public source files used by the benchmark and the downstream analysis.

Files go to data/raw/ (not committed). A manifest with SHA-256 checksums and the download date is written to
data/manifest.json, which IS committed, so that a later run can detect whether EIA changed a file.

Usage:
    python scripts/download_data.py            # download missing files
    python scripts/download_data.py --verify   # compare local files with data/manifest.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MANIFEST = ROOT / "data" / "manifest.json"

EIA = "https://www.eia.gov"
FILES = {
    # CBECS 2018 public-use microdata, codebook, and published summary tables used for validation
    "cbecs2018_final_public.csv": f"{EIA}/consumption/commercial/data/2018/xls/cbecs2018_final_public.csv",
    "cbecs2018_codebook.xlsx": f"{EIA}/consumption/commercial/data/2018/xls/2018microdata_codebook.xlsx",
    "cbecs2018_table_b1.xlsx": f"{EIA}/consumption/commercial/data/2018/xls/b1_public_data.xlsx",
    "cbecs2018_table_c1.xlsx": f"{EIA}/consumption/commercial/data/2018/xls/c1_public_data.xlsx",
    # RECS 2020 public-use microdata (v7) and codebook
    "recs2020_public_v7.csv": f"{EIA}/consumption/residential/data/2020/csv/recs2020_public_v7.csv",
    "recs2020_codebook_v7.xlsx": f"{EIA}/consumption/residential/data/2020/xls/RECS%202020%20Codebook%20for%20Public%20File%20-%20v7.xlsx",
    # Monthly Energy Review Table 2.3 (commercial sector energy consumption)
    "mer_table_2_3.csv": f"{EIA}/totalenergy/data/browser/csv.php?tbl=T02.03",
    "mer_table_2_3.xlsx": f"{EIA}/totalenergy/data/browser/xls.php?tbl=T02.03",
}

HEADERS = {"User-Agent": "meta-urban-benchmark/2.0 (research data download)"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(force: bool = False) -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    for name, url in FILES.items():
        dest = RAW / name
        if dest.exists() and not force:
            print(f"have  {name}")
        else:
            print(f"get   {name}")
            r = requests.get(url, headers=HEADERS, timeout=120)
            r.raise_for_status()
            dest.write_bytes(r.content)
            manifest[name] = {"url": url, "downloaded": dt.date.today().isoformat()}
        manifest.setdefault(name, {"url": url, "downloaded": None})
        manifest[name]["sha256"] = sha256(dest)
        manifest[name]["bytes"] = dest.stat().st_size
    MANIFEST.write_text(json.dumps(manifest, indent=2))
    return manifest


def verify() -> int:
    manifest = json.loads(MANIFEST.read_text())
    bad = 0
    for name, meta in manifest.items():
        dest = RAW / name
        if not dest.exists():
            print(f"missing  {name}")
            bad += 1
        elif sha256(dest) != meta["sha256"]:
            print(f"CHANGED  {name} (publisher may have revised the file)")
            bad += 1
        else:
            print(f"ok       {name}")
    return 1 if bad else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    sys.exit(verify() if args.verify else (download(args.force) and 0))
