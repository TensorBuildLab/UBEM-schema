"""AI documentation layer of the Meta-Urban schema, generated from the single LinkML source.

    python -m meta_urban.ai_docs        # writes schema/ai/

The schema is written once (schema/meta_urban.yaml, schema/vocab/ubem_concepts.yaml, catalog/) and compiled into
artifacts for two audiences. People read the YAML, the generated documentation and the paper. AI systems get
four artifacts, each sized for a context window and each usable without a human explaining it:

    schema_card.md           what the schema is for, every class and field with its definition and allowed
                             values, the validation rules, and a worked example (system prompt for profiling)
    concept_cards.jsonl      one self-contained card per concept (retrieval unit for variable mapping)
    dataset_cards/<id>.md    one card per catalog entry, including its conventions (context for integration)
    ../generated/*.json|ttl  JSON Schema (constrained generation) and SHACL (verification of AI output)
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from . import ROOT, SCHEMA_YAML
from .io import concept_index, leaf_concepts, load_catalog

AI = ROOT / "schema" / "ai"


def _schema() -> dict:
    return yaml.safe_load(SCHEMA_YAML.read_text(encoding="utf-8"))


def approx_tokens(text: str) -> int:
    return len(text) // 4


# ------------------------------------------------------------------------------------------------ cards
def concept_card(c: dict, idx: dict | None = None) -> dict:
    idx = idx or concept_index()
    card = {"id": c["id"], "label": c["pref_label"], "definition": c["definition"],
            "group": idx.get(c.get("broader"), {}).get("pref_label", c.get("broader")),
            "describes": c.get("entity"), "unit": c.get("canonical_unit"),
            "synonyms": c.get("alt_labels", []), "role": c.get("concept_role")}
    maps = {k: c[k] for k in ("exact_match", "close_match", "broad_match", "narrow_match", "related_match") if c.get(k)}
    if maps:
        card["mappings"] = maps
    return {k: v for k, v in card.items() if v not in (None, [], "")}


def concept_card_text(card: dict) -> str:
    """The text an AI system sees for one concept (used as L2 context and as a retrieval unit)."""
    extra = [f"group={card['group']}" if card.get("group") else "",
             f"describes={card['describes']}" if card.get("describes") else "",
             f"unit={card['unit']}" if card.get("unit") else "",
             ("also called: " + ", ".join(card["synonyms"][:6])) if card.get("synonyms") else ""]
    extra = "; ".join(e for e in extra if e)
    return f"{card['id']}: {card['label']}. {card['definition']}" + (f" [{extra}]" if extra else "")


FACETS = [("ubem_roles", "UBEM workflow roles"), ("statistical_nature", "Statistical nature"),
          ("spatial_granularity", "Finest public spatial granularity"), ("temporal_resolution", "Temporal resolution"),
          ("access_level", "Access"), ("join_keys", "Join keys"), ("license", "License")]


def dataset_card(entry: dict, conventions_only: bool = False) -> str:
    """Compact, self-contained description of one dataset for an AI system."""
    lines = []
    if not conventions_only:
        lines.append(f"# {entry.get('title')} ({entry['id']})")
        for k, lab in FACETS:
            v = entry.get(k)
            if v not in (None, [], ""):
                lines.append(f"- {lab}: {', '.join(map(str, v)) if isinstance(v, list) else v}")
    if entry.get("sampling_weights"):
        lines.append(f"- Survey weights: {entry['sampling_weights']}")
    conv = entry.get("conventions") or []
    if conv:
        lines.append("- Conventions (apply to many variables; individual codebook entries do not repeat them):")
        for c in conv:
            ex = f" Example: {c['example']}" if c.get("example") else ""
            lines.append(f"  - {c.get('applies_to', 'all variables')}: {c['rule']}{ex}")
    return "\n".join(lines)


def schema_card() -> str:
    s = _schema()
    out = ["# Meta-Urban 2.0: schema card for AI systems", "",
           "Purpose: describe open datasets for urban building energy modeling (UBEM) so that they can be found, "
           "judged and joined, and describe their variables so that values are interpreted correctly. Use only "
           "the fields and values defined here; write null when the source does not state a value; never guess.",
           ""]
    slots = s["slots"]
    for cname in ("DatasetProfile", "Distribution", "SpatialCoverage", "TemporalCoverage", "Convention",
                  "VariableProfile", "CodeEntry", "Verification"):
        c = s["classes"].get(cname)
        if not c:
            continue
        out.append(f"## {cname}")
        out.append(" ".join(str(c.get("description", "")).split()))
        req = {k for k, v in (c.get("slot_usage") or {}).items() if (v or {}).get("required")}
        for sl in c.get("slots", []):
            d = slots.get(sl) or {}
            rng = d.get("range", "string")
            flags = []
            if sl in req or d.get("required"):
                flags.append("required")
            if d.get("multivalued"):
                flags.append("list")
            line = f"- {sl} ({rng}{', ' + ', '.join(flags) if flags else ''}): {' '.join(str(d.get('description', '')).split())}"
            out.append(line)
            enum = s["enums"].get(rng)
            if enum:
                for v, pv in (enum.get("permissible_values") or {}).items():
                    out.append(f"    - {v}: {(pv or {}).get('description', '')}")
        for r in c.get("rules", []) or []:
            out.append(f"- Rule: {' '.join(str(r.get('description', '')).split())}")
        out.append("")
    cat = {e["id"]: e for e in load_catalog()}
    out += ["## Worked example (dataset level)", dataset_card(cat["chr-cbecs-2018"]), ""]
    return "\n".join(out)


def main() -> int:
    AI.mkdir(parents=True, exist_ok=True)
    (AI / "dataset_cards").mkdir(exist_ok=True)
    sc = schema_card()
    (AI / "schema_card.md").write_text(sc, encoding="utf-8")
    idx = concept_index()
    cards = [concept_card(c, idx) for c in leaf_concepts()]
    with open(AI / "concept_cards.jsonl", "w", encoding="utf-8") as fh:
        for c in cards:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    n = 0
    for e in load_catalog():
        (AI / "dataset_cards" / f"{e['id']}.md").write_text(dataset_card(e) + "\n", encoding="utf-8")
        n += 1
    ct = [approx_tokens(concept_card_text(c)) for c in cards]
    print(f"schema_card.md: ~{approx_tokens(sc):,} tokens; {len(cards)} concept cards, ~{sum(ct):,} tokens in "
          f"total (median {sorted(ct)[len(ct) // 2]} per card); {n} dataset cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
