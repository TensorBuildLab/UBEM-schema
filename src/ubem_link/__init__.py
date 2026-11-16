"""UBEM-Link: an AI-ready semantic schema, open-data catalog and benchmark for UBEM."""

from pathlib import Path

__version__ = "1.0.0"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_YAML = ROOT / "schema" / "ubem_link.yaml"
SCHEMA_JSON = ROOT / "schema" / "generated" / "ubem_link.schema.json"
CONCEPTS_YAML = ROOT / "schema" / "vocab" / "ubem_concepts.yaml"
CATALOG_DIR = ROOT / "catalog" / "datasets"
DATA_RAW = ROOT / "data" / "raw"
BENCH = ROOT / "benchmark"
PAPER = ROOT / "paper"
