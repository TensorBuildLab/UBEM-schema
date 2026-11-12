"""Validate catalog entries against the JSON Schema generated from the LinkML schema.

Usage:
    python -m meta_urban.validate [catalog/datasets]

Checks: (1) JSON Schema for DatasetProfile (types, enums, patterns, required slots);
(2) the schema rule that weighted sample surveys name their weights; (3) unique ids that match file names.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

from . import CATALOG_DIR, SCHEMA_JSON
from .io import load_catalog


def _dataset_validator() -> jsonschema.Draft7Validator:
    with open(SCHEMA_JSON, encoding="utf-8") as fh:
        full = json.load(fh)
    sub = dict(full)
    sub["$ref"] = "#/$defs/DatasetProfile"
    for key in ("properties", "required", "additionalProperties", "type", "title"):
        sub.pop(key, None)
    return jsonschema.Draft7Validator(sub)


def _clean(entry: dict) -> dict:
    """Drop private keys and YAML-native dates/ints that JSON Schema expects as strings."""
    out = {k: v for k, v in entry.items() if not k.startswith("_")}

    def fix(obj):
        if isinstance(obj, dict):
            return {k: fix(v) for k, v in obj.items() if v is not None}
        if isinstance(obj, list):
            return [fix(v) for v in obj]
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        return obj

    out = fix(out)
    for key in ("temporal_coverage",):
        if isinstance(out.get(key), dict):
            out[key] = {k: str(v) for k, v in out[key].items()}
    if isinstance(out.get("verified"), dict) and "date" in out["verified"]:
        out["verified"]["date"] = str(out["verified"]["date"])
    return out


def validate(directory: Path | str = CATALOG_DIR) -> list[tuple[str, str]]:
    validator = _dataset_validator()
    problems: list[tuple[str, str]] = []
    seen: set[str] = set()
    for entry in load_catalog(directory):
        fname = entry["_file"]
        doc = _clean(entry)
        for err in validator.iter_errors(doc):
            loc = "/".join(str(p) for p in err.absolute_path) or "(root)"
            problems.append((fname, f"{loc}: {err.message[:200]}"))
        if doc.get("statistical_nature") == "sample_survey_weighted" and not doc.get("sampling_weights"):
            problems.append((fname, "rule: sample_survey_weighted requires sampling_weights"))
        did = doc.get("id")
        if did in seen:
            problems.append((fname, f"duplicate id {did}"))
        seen.add(did)
        if did and fname != f"{did}.yaml":
            problems.append((fname, f"file name does not match id {did}"))
    return problems


def main(argv: list[str]) -> int:
    directory = Path(argv[1]) if len(argv) > 1 else CATALOG_DIR
    n = len(list(directory.glob("*.yaml")))
    problems = validate(directory)
    for fname, msg in problems:
        print(f"{fname}: {msg}")
    print(f"{n} entries, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
