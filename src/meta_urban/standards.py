"""Parse the compared standards and measure how AI-ready their machine-readable artifacts are.

    python scripts/download_standards.py      # once
    python -m meta_urban.standards            # writes paper/tables/ai_readiness_audit.csv

Each standard is reduced to a list of terms {id, label, definition, kind, unit, enum_value}. The audit counts
properties an AI system needs to use a vocabulary without a human in the loop (Section 3 of the paper):
natural-language definitions, documented enumeration values, unit information, statistical-design terms,
a JSON Schema for constrained generation, machine-checkable validation, and the token cost of the full
vocabulary. Binary properties that cannot be read from the files (for example whether a standard publishes
SHACL shapes) are recorded with their source in AUDIT_FACTS.
"""

from __future__ import annotations

import csv
import json
import re
from functools import lru_cache
from pathlib import Path

import pandas as pd
import yaml

from . import PAPER, ROOT, SCHEMA_YAML
from .io import load_concepts

STD = ROOT / "data" / "raw" / "standards"
MAPPINGS = ROOT / "schema" / "vocab" / "mappings_2026-11-13.csv"
XS = "{http://www.w3.org/2001/XMLSchema}"
STAT_DESIGN = re.compile(r"\b(sampl\w* weight|survey weight|replicate weight|final weight|imputat\w*|imputed|"
                         r"top-?cod\w*)\b", re.I)


def _words(s: str | None) -> int:
    return len(re.findall(r"\w+", s or ""))


def _clean(s: str | None) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


# ------------------------------------------------------------------------------------------- parsers
@lru_cache
def brick_terms() -> list[dict]:
    import rdflib
    from rdflib.namespace import OWL, RDF, RDFS, SKOS

    g = rdflib.Graph().parse(STD / "Brick.ttl", format="turtle")
    BRICK = "https://brickschema.org/schema/Brick#"
    out = []
    for s in set(g.subjects()):
        if not isinstance(s, rdflib.URIRef) or not str(s).startswith(BRICK):
            continue
        types = set(g.objects(s, RDF.type))
        if (s, OWL.deprecated, rdflib.Literal(True)) in g:
            continue
        if OWL.Class in types or rdflib.URIRef("http://www.w3.org/ns/shacl#NodeShape") in types:
            kind = "class"
        elif types & {OWL.ObjectProperty, OWL.DatatypeProperty, RDF.Property}:
            kind = "property"
        else:
            kind = "value"
        d = g.value(s, SKOS.definition) or g.value(s, RDFS.comment)
        q = g.value(s, rdflib.URIRef(BRICK + "hasQuantity")) or g.value(s, rdflib.URIRef(BRICK + "hasQUDTReference"))
        out.append({"id": str(s), "label": str(g.value(s, RDFS.label) or str(s).split("#")[1].replace("_", " ")),
                    "definition": _clean(str(d)) if d else "", "kind": kind, "unit": bool(q), "enum_value": False})
    return out


@lru_cache
def bedes_terms() -> list[dict]:
    from lxml import etree

    out = []
    for n in etree.parse(str(STD / "bedes_v2.5_terms.xml")).getroot():
        f = {c.tag: (c.text or "") for c in n}
        uom = f.get("Unit-of-Measure", "").strip()
        out.append({"id": f.get("URL", ""), "label": f.get("Term", ""), "definition": _clean(f.get("Definition")),
                    "kind": "term", "unit": uom not in ("", "None", "none"), "enum_value": False,
                    "uuid": f.get("Content-UUID", "")})
    for n in etree.parse(str(STD / "bedes_v2.5_list_options.xml")).getroot():
        f = {c.tag: (c.text or "") for c in n}
        out.append({"id": f.get("URL", ""), "label": f"{f.get('List-Option', '')} (list option of "
                    f"{f.get('Related-Term', '')})", "definition": _clean(f.get("List-Option-Definition")),
                    "kind": "value", "unit": False, "enum_value": True, "uuid": f.get("Content-UUID", "")})
    return out


@lru_cache
def energy_ade_terms() -> list[dict]:
    from lxml import etree

    root = etree.parse(str(STD / "EnergyADE.xsd")).getroot()
    ns = "http://www.sig3d.org/citygml/2.0/energy/1.0#"

    def doc(el):
        d = el.find(f"{XS}annotation/{XS}documentation")
        return _clean(d.text) if d is not None and d.text else ""

    out = []
    for el in root:
        name = el.get("name")
        if not name:
            continue
        kind = {"element": "class", "complexType": "class", "simpleType": "value-list"}.get(etree.QName(el).localname, "x")
        out.append({"id": f"{ns}{name}", "label": name, "definition": doc(el), "kind": kind,
                    "unit": False, "enum_value": False})
        for m in el.iter(f"{XS}element", f"{XS}attribute"):
            if m is el or not m.get("name"):
                continue
            t = m.get("type") or ""
            out.append({"id": f"{ns}{name}/{m.get('name')}", "label": m.get("name"), "definition": doc(m),
                        "kind": "property", "unit": "Measure" in t or "Length" in t or "Area" in t,
                        "enum_value": False})
        for e in el.iter(f"{XS}enumeration"):
            out.append({"id": f"{ns}{name}/{e.get('value')}", "label": e.get("value"), "definition": doc(e),
                        "kind": "value", "unit": False, "enum_value": True})
    return out


@lru_cache
def dcat_terms() -> list[dict]:
    import rdflib
    from rdflib.namespace import RDFS, SKOS

    g = rdflib.Graph().parse(STD / "dcat3.ttl", format="turtle")
    out = []
    for s in set(g.subjects()):
        if not str(s).startswith("http://www.w3.org/ns/dcat#"):
            continue
        d = [str(o) for o in g.objects(s, SKOS.definition) if getattr(o, "language", None) in (None, "en")]
        c = [str(o) for o in g.objects(s, RDFS.comment) if getattr(o, "language", None) in (None, "en")]
        lab = [str(o) for o in g.objects(s, RDFS.label) if getattr(o, "language", None) in (None, "en")]
        out.append({"id": str(s), "label": lab[0] if lab else str(s).split("#")[1],
                    "definition": _clean((d or c or [""])[0]), "kind": "term", "unit": False, "enum_value": False})
    return out


@lru_cache
def schemaorg_terms(dataset_only: bool = True) -> list[dict]:
    js = json.loads((STD / "schemaorg-current-https.jsonld").read_text(encoding="utf-8"))
    graph = js["@graph"]
    keep_types = {"schema:Dataset", "schema:CreativeWork", "schema:Thing", "schema:DataCatalog",
                  "schema:DataDownload", "schema:MediaObject"}
    out = []
    for t in graph:
        tid = t.get("@id", "")
        types = t.get("@type") if isinstance(t.get("@type"), list) else [t.get("@type")]
        dom = t.get("schema:domainIncludes", [])
        dom = {d["@id"] for d in (dom if isinstance(dom, list) else [dom])}
        if dataset_only and not ((("rdfs:Class" in types) and tid in keep_types) or (dom & keep_types)):
            continue
        com = t.get("rdfs:comment", "")
        com = com.get("@value", "") if isinstance(com, dict) else com
        lab = t.get("rdfs:label", "")
        lab = lab.get("@value", "") if isinstance(lab, dict) else lab
        out.append({"id": tid, "label": lab, "definition": _clean(com),
                    "kind": "class" if "rdfs:Class" in types else "property", "unit": False, "enum_value": False})
    return out


@lru_cache
def meta_urban_terms() -> list[dict]:
    sch = yaml.safe_load(SCHEMA_YAML.read_text(encoding="utf-8"))
    out = []
    for n, c in (sch.get("classes") or {}).items():
        out.append({"id": f"meta_urban:{n}", "label": n, "definition": c.get("description", ""), "kind": "class",
                    "unit": False, "enum_value": False})
    for n, s in (sch.get("slots") or {}).items():
        out.append({"id": f"meta_urban:{n}", "label": n, "definition": (s or {}).get("description", ""),
                    "kind": "property", "unit": False, "enum_value": False})
    for en, e in (sch.get("enums") or {}).items():
        for v, pv in (e.get("permissible_values") or {}).items():
            out.append({"id": f"meta_urban:{en}/{v}", "label": v, "definition": (pv or {}).get("description", ""),
                        "kind": "value", "unit": False, "enum_value": True})
    for c in load_concepts():
        out.append({"id": f"meta_urban:{c['id']}", "label": c["pref_label"], "definition": c["definition"],
                    "kind": "concept", "unit": bool(c.get("canonical_unit")) or not c.get("quantity_kind"),
                    "enum_value": False, "quantitative": bool(c.get("quantity_kind"))})
    return out


STANDARDS = {
    "Meta-Urban 2.0": meta_urban_terms,
    "Brick 1.4.4": brick_terms,
    "BEDES 2.5": bedes_terms,
    "CityGML Energy ADE 1.0": energy_ade_terms,
    "DCAT 3": dcat_terms,
    "schema.org (Dataset-related)": schemaorg_terms,
}

# Properties that are facts about the publication, not countable from the term files. Sources in comments.
AUDIT_FACTS = {
    # json_schema: official JSON Schema usable as a constrained-decoding grammar
    # validation: machine-checkable constraints published with the standard
    "Meta-Urban 2.0": {"json_schema": "yes", "validation": "JSON Schema + SHACL", "level": "dataset + variable"},
    "Brick 1.4.4": {"json_schema": "no", "validation": "SHACL shapes in Brick.ttl", "level": "building points, equipment"},
    "BEDES 2.5": {"json_schema": "no", "validation": "none (dictionary)", "level": "building characteristics"},
    "CityGML Energy ADE 1.0": {"json_schema": "no", "validation": "XML Schema", "level": "building objects"},
    "DCAT 3": {"json_schema": "no", "validation": "none in the W3C namespace file", "level": "dataset"},
    "schema.org (Dataset-related)": {"json_schema": "no", "validation": "none", "level": "dataset (web)"},
}


def audit() -> pd.DataFrame:
    rows = []
    for name, fn in STANDARDS.items():
        t = fn()
        defs = [x for x in t if _words(x["definition"]) >= 3]
        ev = [x for x in t if x["enum_value"]]
        stat = [x for x in t if STAT_DESIGN.search(x["label"] + " " + x["definition"])]
        chars = sum(len(x["label"]) + len(x["definition"]) + 2 for x in t)
        rows.append({
            "standard": name, "terms": len(t),
            "with_definition_pct": 100 * len(defs) / max(1, len(t)),
            "median_definition_words": float(pd.Series([_words(x["definition"]) for x in defs]).median()) if defs else 0.0,
            "enum_values": len(ev),
            "enum_values_defined_pct": 100 * sum(_words(x["definition"]) >= 2 for x in ev) / len(ev) if ev else float("nan"),
            "statistical_design_terms": len(stat),
            "vocabulary_tokens_k": chars / 4 / 1000,
            **AUDIT_FACTS[name],
        })
    return pd.DataFrame(rows)


# ------------------------------------------------------------- documentation transplant (Experiment E2)
RELATION_ORDER = ["exactMatch", "closeMatch", "narrowMatch", "broadMatch", "relatedMatch"]


@lru_cache
def _index(standard: str) -> dict:
    fn = {"brick": brick_terms, "bedes": bedes_terms, "energy_ade": energy_ade_terms}[standard]
    terms = fn()
    idx = {x["id"]: x for x in terms}
    if standard == "brick":  # rec: replacements are in the same file but outside the Brick namespace
        import rdflib
        from rdflib.namespace import RDFS, SKOS

        g = rdflib.Graph().parse(STD / "Brick.ttl", format="turtle")
        for s in set(g.subjects()):
            if str(s).startswith("https://w3id.org/rec#"):
                d = g.value(s, SKOS.definition) or g.value(s, RDFS.comment)
                idx[str(s)] = {"label": str(g.value(s, RDFS.label) or str(s).split("#")[1]),
                               "definition": _clean(str(d)) if d else ""}
    return idx


@lru_cache
def transplant_docs(standard: str) -> dict[str, str]:
    """Concept id -> documentation of the best-matching term of `standard` (its own label and definition).

    Concepts with no mapping to the standard get no documentation (the model sees the id only)."""
    best = {}
    with open(MAPPINGS, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["standard"] != standard:
                continue
            rank = RELATION_ORDER.index(r["relation"])
            if r["concept_id"] not in best or rank < best[r["concept_id"]][0]:
                best[r["concept_id"]] = (rank, r["target_id"])
    idx = _index(standard)
    out = {}
    for cid, (_, tid) in best.items():
        t = idx.get(tid)
        if t is None:  # Energy ADE ids for members of types, or BEDES nodes, are matched by suffix
            t = next((v for k, v in idx.items() if k.endswith(tid.split("/")[-1]) and tid.split("#")[-1] in k), None)
        if t is None:
            continue
        lab, d = t["label"], t["definition"]
        out[cid] = f"{lab}. {d}".strip() if d else lab
    return out


def main() -> int:
    a = audit()
    (PAPER / "tables").mkdir(parents=True, exist_ok=True)
    a.to_csv(PAPER / "tables" / "ai_readiness_audit.csv", index=False)
    print(a.round(1).to_string(index=False))
    for s in ("brick", "bedes", "energy_ade"):
        d = transplant_docs(s)
        print(s, len(d), "concepts documented; example:", next(iter(d.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
