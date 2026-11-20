"""Propose dataset conventions from a publisher's documentation (user guide, metadata page, README).

Conventions are rules a publisher states once for many variables (codes for missing values, units given only in
a field name, imputation-flag naming, placeholder identifiers, fields not to use). The paper found that a model
given such rules as prose applies them beyond their scope, so each proposal carries a machine-readable scope
(`applies_to_variables` or `applies_to_pattern`) that the profiler applies deterministically. Proposals must be
confirmed by a person against the documentation before they are added to a dataset entry.
"""

from __future__ import annotations

from .llm import ROLE, complete, parse_json

CONV_TYPES = ["missing_code", "unit", "top_or_bottom_code", "imputation_flag", "weight", "identifier_format",
              "do_not_use", "definition"]
SYSTEM = (
    f"{ROLE}\n\nTask: read an excerpt of a dataset's documentation and list the conventions it states that apply "
    "to many variables or to fields whose individual descriptions do not repeat them: codes meaning missing, "
    "unknown or not applicable; units or scale factors stated once; how imputation flags or weights are named; "
    "placeholder identifiers; fields that must not be used. For each convention give:\n"
    f"convention_type: one of {CONV_TYPES};\n"
    "applies_to: the variables it concerns, in words;\n"
    "applies_to_variables: exact variable names if the excerpt names them, else [];\n"
    "applies_to_pattern: a regular expression over variable names if the excerpt states a naming pattern, else \"\";\n"
    "rule: the convention as one sentence that can be applied without other context;\n"
    "missing_codes: the codes it declares missing, else [];\n"
    "unit: a QUDT unit id such as unit:FT, unit:KiloBTU_IT or unit:FT2 if it states a unit, else \"\";\n"
    "unit_multiplier: the scale factor it states, else 1;\n"
    "quote: the sentence of the excerpt that states it, verbatim.\n"
    "List only conventions the excerpt states; return an empty list if there are none."
)
SCHEMA = {"type": "object", "properties": {"conventions": {"type": "array", "items": {
    "type": "object", "properties": {
        "convention_type": {"type": "string", "enum": CONV_TYPES}, "applies_to": {"type": "string"},
        "applies_to_variables": {"type": "array", "items": {"type": "string"}},
        "applies_to_pattern": {"type": "string"}, "rule": {"type": "string"},
        "missing_codes": {"type": "array", "items": {"type": "string"}}, "unit": {"type": "string"},
        "unit_multiplier": {"type": "number"}, "quote": {"type": "string"}},
    "required": ["convention_type", "applies_to", "applies_to_variables", "applies_to_pattern", "rule",
                 "missing_codes", "unit", "unit_multiplier", "quote"], "additionalProperties": False}}},
    "required": ["conventions"], "additionalProperties": False}


def chunks(text: str, size: int = 6000, overlap: int = 400) -> list[str]:
    out, i = [], 0
    while i < len(text):
        out.append(text[i:i + size])
        i += size - overlap
    return out


def extract_conventions(text: str, model: str, cache_dir=None) -> list[dict]:
    found, seen = [], set()
    for k, part in enumerate(chunks(text)):
        r = complete(model, {"system": SYSTEM, "user": f"DOCUMENTATION EXCERPT {k + 1}\n{part}", "schema": SCHEMA},
                     {"task": "tool-conventions", "name": f"chunk{k}"}, 0, cache_dir=cache_dir)
        for c in (parse_json(r["response"]) or {}).get("conventions", []):
            key = (c["convention_type"], c["rule"].strip().lower())
            if key in seen or (c.get("quote") and c["quote"] not in text):
                continue  # duplicates, and quotes that do not occur in the documentation, are dropped
            seen.add(key)
            conv = {"convention_type": c["convention_type"], "applies_to": c["applies_to"], "rule": c["rule"]}
            if c.get("applies_to_variables"):
                conv["applies_to_variables"] = c["applies_to_variables"]
            if c.get("applies_to_pattern"):
                conv["applies_to_pattern"] = c["applies_to_pattern"]
            if c.get("missing_codes"):
                conv["missing_codes"] = [str(x) for x in c["missing_codes"]]
            if c.get("unit"):
                conv["unit"] = c["unit"]
                conv["unit_multiplier"] = c.get("unit_multiplier") or 1
            conv["example"] = f"Documentation: \"{c['quote'][:200]}\"" if c.get("quote") else None
            found.append({k2: v for k2, v in conv.items() if v is not None})
    return found
