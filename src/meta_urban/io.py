"""Loading the catalog, the concept vocabulary and the schema enums."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import yaml

from . import CATALOG_DIR, CONCEPTS_YAML, SCHEMA_YAML


def load_catalog(directory: Path | str = CATALOG_DIR) -> list[dict]:
    """Return all dataset profiles, sorted by id."""
    entries = []
    for path in sorted(Path(directory).glob("*.yaml")):
        with open(path, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
        doc["_file"] = path.name
        entries.append(doc)
    return entries


@lru_cache(maxsize=1)
def load_concepts(path: Path | str = CONCEPTS_YAML) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)["concepts"]


def concept_index(concepts: list[dict] | None = None) -> dict[str, dict]:
    concepts = concepts or load_concepts()
    return {c["id"]: c for c in concepts}


def leaf_concepts(concepts: list[dict] | None = None) -> list[dict]:
    """Concepts that a variable can be mapped to (all concepts with a `broader` parent).

    Top-level grouping concepts (weather, geometry, characteristics, ...) are excluded as mapping targets,
    because a variable should be mapped to the most specific concept that applies.
    """
    concepts = concepts or load_concepts()
    return [c for c in concepts if c.get("broader")]


@lru_cache(maxsize=1)
def schema_enums(path: Path | str = SCHEMA_YAML) -> dict[str, list[str]]:
    with open(path, encoding="utf-8") as fh:
        schema = yaml.safe_load(fh)
    return {name: list((e.get("permissible_values") or {}).keys()) for name, e in schema["enums"].items()}


def granularity_rank() -> dict[str, int]:
    with open(SCHEMA_YAML, encoding="utf-8") as fh:
        schema = yaml.safe_load(fh)
    pv = schema["enums"]["SpatialGranularity"]["permissible_values"]
    return {k: int(v["annotations"]["rank"]) for k, v in pv.items()}


def dump_json(obj, path: Path | str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False, default=str)
