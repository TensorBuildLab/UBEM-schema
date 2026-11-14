"""Download the release files of the standards Meta-Urban is compared with (data/raw/standards/, git-ignored).

    python scripts/download_standards.py           # download and record SHA-256 in data/standards_manifest.json
    python scripts/download_standards.py --verify  # check files against the manifest

Sources (versions pinned where the publisher allows it):
    Brick 1.4.4            GitHub release asset
    BEDES 2.5              term and list-option exports, BuildingSync project repository at a fixed commit
                           (bedes.lbl.gov blocks scripted access)
    CityGML Energy ADE 1.0 official schema location
    DCAT 3                 W3C namespace document (Turtle)
    schema.org             current release (JSON-LD)
"""
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "standards"
MANIFEST = ROOT / "data" / "standards_manifest.json"
BS = "https://raw.githubusercontent.com/BuildingSync/BuildingSync-website/8cc6b42445de05bc25afc7327a0059da12ef2a69/bsyncviewer/lib/bedes/v2.5"
FILES = {
    "Brick.ttl": "https://github.com/BrickSchema/Brick/releases/download/v1.4.4/Brick.ttl",
    "bedes_v2.5_terms.xml": f"{BS}/bedes_online_dictionary_uuid-terms.xml",
    "bedes_v2.5_list_options.xml": f"{BS}/bedes_online_dictionary_uuid-lo.xml",
    "EnergyADE.xsd": "https://www.sig3d.org/citygml/2.0/energy/1.0/EnergyADE.xsd",
    "dcat3.ttl": "https://www.w3.org/ns/dcat3.ttl",
    "schemaorg-current-https.jsonld": "https://schema.org/version/latest/schemaorg-current-https.jsonld",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    if "--verify" in sys.argv:
        man = json.loads(MANIFEST.read_text())
        bad = [f for f, m in man.items() if not (OUT / f).exists() or sha(OUT / f) != m["sha256"]]
        print("all files match" if not bad else f"mismatch: {bad}")
        return 1 if bad else 0
    man = {}
    for name, url in FILES.items():
        p = OUT / name
        if not p.exists():
            r = requests.get(url, timeout=120, headers={"User-Agent": "meta-urban-research/1.0"})
            r.raise_for_status()
            p.write_bytes(r.content)
        man[name] = {"url": url, "downloaded": str(date.today()), "sha256": sha(p), "bytes": p.stat().st_size}
        print(f"{name}: {man[name]['bytes']:,} bytes")
    MANIFEST.write_text(json.dumps(man, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
