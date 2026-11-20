"""Publish the UBEM-Link concept mappings as an SSSOM mapping set (schema/mappings/ubem_link.sssom.tsv).

SSSOM (Simple Standard for Sharing Ontological Mappings) is the format in which ontology projects exchange
mappings; it records the subject, predicate, object and how each mapping was justified. Source:
schema/vocab/mappings_2026-11-13.csv (168 mappings, each target checked to exist in the release files).

    python scripts/make_sssom.py
"""

from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "schema" / "vocab" / "mappings_2026-11-13.csv"
OUT = ROOT / "schema" / "mappings" / "ubem_link.sssom.tsv"
OBJECT_SOURCE = {"brick": ("https://brickschema.org/schema/Brick", "1.4.4"),
                 "bedes": ("https://bedes.lbl.gov", "2.5"),
                 "energy_ade": ("http://www.sig3d.org/citygml/2.0/energy/1.0", "1.0")}

df = pd.read_csv(SRC)
rows = []
for r in df.itertuples():
    src, ver = OBJECT_SOURCE.get(r.standard, (r.standard, ""))
    rows.append({"subject_id": f"ubem_link:{r.concept_id}", "predicate_id": f"skos:{r.relation}",
                 "object_id": r.target_id, "object_label": r.target_label,
                 "mapping_justification": "semapv:ManualMappingCuration",
                 "object_source": src, "object_source_version": ver,
                 "author_label": "UBEM-Link authors (relation assigned with AI assistance)",
                 "confidence": "", "comment": "" if pd.isna(r.note) else str(r.note)})
meta = {"mapping_set_id": "https://w3id.org/ubem-link/mappings/ubem_link.sssom.tsv",
        "mapping_set_version": "1.0.0", "license": "https://creativecommons.org/licenses/by/4.0/",
        "subject_source": "https://w3id.org/ubem-link/", "mapping_date": "2026-11-13",
        "curie_map": {"ubem_link": "https://w3id.org/ubem-link/", "skos": "http://www.w3.org/2004/02/skos/core#",
                      "semapv": "https://w3id.org/semapv/vocab/"},
        "comment": "Each object_id was checked to exist in the release file of its standard; the relation type was "
                   "assigned with AI assistance and has not been audited by an independent expert."}
OUT.parent.mkdir(parents=True, exist_ok=True)
head = "".join(f"#{line}\n" for line in yaml.safe_dump(meta, sort_keys=False).splitlines())
OUT.write_text(head + pd.DataFrame(rows).to_csv(sep="\t", index=False), encoding="utf-8")
print(f"{len(rows)} mappings -> {OUT.relative_to(ROOT)}")
