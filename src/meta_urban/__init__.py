"""Meta-Urban: metadata schema, open-data catalog and LLM alignment benchmark for UBEM."""

from pathlib import Path

__version__ = "2.0.0.dev0"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_YAML = ROOT / "schema" / "meta_urban.yaml"
SCHEMA_JSON = ROOT / "schema" / "generated" / "meta_urban.schema.json"
CONCEPTS_YAML = ROOT / "schema" / "vocab" / "ubem_concepts.yaml"
CATALOG_DIR = ROOT / "catalog" / "datasets"
DATA_RAW = ROOT / "data" / "raw"
BENCH = ROOT / "benchmark"
PAPER = ROOT / "paper"
