# Meta-Urban: schema, open-data catalog and LLM alignment benchmark for urban building energy modeling

TensorBuild Lab, University of Arizona. Companion repository for the manuscript in `paper/` (draft), which
replaces the preprint *Taxonomy, Semantic Data Schema, and Schema Alignment for Open Data in Urban Building
Energy Modeling* (Zhang, Chen, Zou; arXiv:2311.08535).

Every number and figure in the paper is regenerated from this repository.

## What is here

| Path | Content |
|---|---|
| `schema/meta_urban.yaml` | **Meta-Urban 2.0** schema (LinkML): dataset level (DCAT 3 profile with six UBEM facets) and variable level (concept, QUDT unit, code list, aggregation, weights, imputation flags) |
| `schema/generated/` | JSON Schema, SHACL shapes and OWL ontology compiled from the schema |
| `schema/vocab/ubem_concepts.yaml` | Concept vocabulary v0.1 (81 concepts, SKOS hierarchy, CityGML and EPW mappings) |
| `catalog/datasets/*.yaml` | **91 verified open-dataset profiles** (weather, geometry, characteristics, operation, energy, simulation, context) |
| `src/meta_urban/` | Python package: validation, catalog analytics and competency questions, codebook parsing, benchmark, baselines, LLM runners, downstream analysis |
| `benchmark/` | Items, evaluation sample, gold labels (T3 automatic; T2 draft awaiting two-annotator verification), cached model outputs |
| `scripts/download_data.py` | Downloads CBECS 2018, RECS 2020 and EIA MER files with SHA-256 manifest (`data/manifest.json`) |
| `paper/` | Manuscript draft, verified bibliography (145 entries), generated tables and figures |
| `docs/diagnosis.md` | Why the 2023 version was rejected, problem by problem |
| `docs/redesign.md` | The research design of the new paper |
| `docs/reviewer_map.md` | Where each past reviewer concern is answered |
| `legacy/2023-chatgpt-case-studies/` | The 2023 ChatGPT outputs, unchanged, for comparison |

## Quick start

```bash
pip install -e ".[dev]"            # add [schema] to recompile the schema, [llm] for API models
python scripts/download_data.py    # EIA source files -> data/raw/
python -m meta_urban.validate      # validate all catalog entries
python -m meta_urban.downstream    # RQ4 tables (weighted vs. unweighted CBECS, error sensitivity)
python -m meta_urban.analytics     # RQ1/RQ2 tables, competency questions, figures
python -m meta_urban.gold_draft    # draft T2 labels for annotation
python -m meta_urban.bench items   # benchmark items and the 300-variable evaluation sample
python -m meta_urban.bench baselines
pytest -q
```

Running LLMs. Put credentials in a git-ignored `.env` file at the repository root (for example
`ANTHROPIC_API_KEY=...`); the scripts read it and never print it. Open-weight models run through a local
Ollama server.

```bash
python -m meta_urban.bench plan --repeats 5                                   # calls and tokens, no spending
python -m meta_urban.bench t2 --model ollama:qwen3:8b --repeats 5
python -m meta_urban.bench t2 --model anthropic:claude-opus-5-5 --repeats 5 --workers 8
python -m meta_urban.bench t3 --model anthropic:claude-opus-5-5 --repeats 3 --workers 8
python -m meta_urban.bench score                                              # summary tables for all models
```

Every call is cached in `benchmark/results/cache/` with token counts and latency, so results can be
re-scored without re-running models.

To recompile the schema after editing it:

```bash
pip install -e ".[schema]"
gen-json-schema schema/meta_urban.yaml > schema/generated/meta_urban.schema.json
gen-shacl schema/meta_urban.yaml > schema/generated/meta_urban.shacl.ttl
gen-owl schema/meta_urban.yaml > schema/generated/meta_urban.owl.ttl
```

## Status (2026-11-13)

- Done: schema v2.0, vocabulary v0.1, 91-entry catalog (agent-drafted, schema-valid), codebook parsing and
  T3 gold, T2 draft labels and frozen evaluation sample, blind annotation sheets, lexical baseline, LLM harness,
  open-weight runs (Qwen3 8B, Llama 3.1 8B; T2 x 4 levels x 5 repeats, T3 x 3 repeats), downstream analysis
  (pipeline reproduces EIA totals within 0.01%), catalog analytics and figures, manuscript draft with
  provisional results.
- To do before submission: two-annotator blind T2 gold with kappa (`python -m meta_urban.gold_sheets make`,
  then `merge`); author spot-check of catalog entries; T1 documentation snapshots; frontier-model runs;
  BEDES/Brick/Energy ADE mappings; discussion and conclusions.

All benchmark numbers are recomputed from the cache with:

```bash
python -m meta_urban.bench score      # summary CSVs in benchmark/results/
python -m meta_urban.bench_report     # paper tables (bench_*.csv) and Figs. 3-4
```

## Licenses

Code: MIT. Schema, vocabulary, catalog and gold labels: CC BY 4.0. Source datasets keep their own licenses
(see each catalog entry). [TODO: confirm with co-authors before making the repository public.]

## Citation

[TODO: add the journal citation and Zenodo DOI at release.]
