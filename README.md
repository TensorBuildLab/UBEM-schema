# UBEM-Link: an AI-ready semantic schema, open-data catalog and benchmark for urban building energy modeling

TensorBuild Lab, University of Arizona. Companion repository for the manuscript in `paper/`.

Every number and figure in the paper is regenerated from this repository.

## What is here

| Path | Content |
|---|---|
| `schema/ubem_link.yaml` | **UBEM-Link** schema (LinkML): dataset level (DCAT 3 profile with six UBEM facets) and variable level (concept, QUDT unit, code list, aggregation, weights, imputation flags) |
| `schema/generated/` | JSON Schema, SHACL shapes and OWL ontology compiled from the schema |
| `schema/vocab/ubem_concepts.yaml` | Concept vocabulary (81 concepts, SKOS hierarchy, CityGML and EPW mappings) |
| `catalog/datasets/*.yaml` | **91 verified open-dataset profiles** (weather, geometry, characteristics, operation, energy, simulation, context) |
| `src/ubem_link/` | Python package: validation, catalog analytics and competency questions, codebook parsing, benchmark, baselines, LLM runners, downstream analysis |
| `benchmark/` | Items, evaluation sample, gold labels (T3 automatic; T2 draft awaiting two-annotator verification), cached model outputs |
| `scripts/download_data.py` | Downloads CBECS 2018, RECS 2020 and EIA MER files with SHA-256 manifest (`data/manifest.json`) |
| `paper/` | Manuscript draft, verified bibliography (145 entries), generated tables and figures |

## Quick start

```bash
pip install -e ".[dev]"            # add [schema] to recompile the schema, [llm] for API models
python scripts/download_data.py    # EIA source files -> data/raw/
python -m ubem_link.validate      # validate all catalog entries
python -m ubem_link.downstream    # RQ4 tables (weighted vs. unweighted CBECS, error sensitivity)
python -m ubem_link.analytics     # RQ1/RQ2 tables, competency questions, figures
python -m ubem_link.gold_draft    # draft T2 labels for annotation
python -m ubem_link.bench items   # benchmark items and the 300-variable evaluation sample
python -m ubem_link.bench baselines
pytest -q
```

Running LLMs. Put credentials in a git-ignored `.env` file at the repository root (for example
`ANTHROPIC_API_KEY=...`); the scripts read it and never print it. Open-weight models run through a local
Ollama server.

```bash
python -m ubem_link.bench plan --repeats 5                                   # calls and tokens, no spending
python -m ubem_link.bench t2 --model ollama:qwen3:8b --repeats 5
python -m ubem_link.bench t2 --model anthropic:claude-opus-5-5 --repeats 5 --workers 8
python -m ubem_link.bench t3 --model anthropic:claude-opus-5-5 --repeats 3 --workers 8
python -m ubem_link.bench score                                              # summary tables for all models
```

Every call is cached in `benchmark/results/cache/` with token counts and latency, so results can be
re-scored without re-running models.

To recompile the schema after editing it:

```bash
pip install -e ".[schema]"
gen-json-schema schema/ubem_link.yaml > schema/generated/ubem_link.schema.json
gen-shacl schema/ubem_link.yaml > schema/generated/ubem_link.shacl.ttl
gen-owl schema/ubem_link.yaml > schema/generated/ubem_link.owl.ttl
```

## Status (2026-11-13)

Manuscript v0.3, rebuilt around AI-ready schemas (target: *Computers, Environment and Urban Systems*, Elsevier;
desk-rejected by *Energy* on scope). New in v0.3: definitions for all 271 schema terms, a
`Convention` class, the AI documentation layer (`schema/ai/`, `python -m ubem_link.ai_docs`), an
AI-readiness audit of five standards (`python -m ubem_link.standards`) and the schema-design experiments
E1-E6 (`bash scripts/run_ai_ready.sh`, then `python -m ubem_link.design_report`) and the end-to-end
building-stock experiment E7 (`python -m ubem_link.endtoend`). Also done: the schema,
the vocabulary with verified external mappings, 91-entry catalog with a field-level verification of a random
20-entry sample (`catalog/verification_2026-11-13.csv`), T2 gold from two blind LLM annotators plus blind
adjudication (kappa 0.91; `benchmark/gold/annotation/`), T3 gold from the codebooks, open-weight runs
(Qwen3 8B, Llama 3.1 8B), downstream analysis, cover letter (`paper/cover_letter.md`) and a Word build
(`paper/build/manuscript.docx`).

Left for the authors: the journal's submission forms.

To rebuild the submission files: `python scripts/graphical_abstract.py` then `python scripts/build_docx.py` (output in `paper/submission/`, checklist in `paper/submission/CHECKLIST.md`).

All benchmark numbers are recomputed from the cache with:

```bash
python -m ubem_link.bench score      # summary CSVs in benchmark/results/
python -m ubem_link.bench_report     # paper tables (bench_*.csv) and Figs. 3-4
```

## Licenses

Code: MIT. Schema, vocabulary, catalog and gold labels: CC BY 4.0. Source datasets keep their own licenses
(see each catalog entry). See `LICENSE` and `LICENSE-DATA.md`.

## Citation

[TODO: add the journal citation after publication.]
