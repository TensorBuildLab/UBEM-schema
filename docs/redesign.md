# Redesign: from a descriptive review to a testable resource-and-benchmark paper

Read `diagnosis.md` first. This note is the plan for the new manuscript and for this repository.

## 1. New framing

**Working title.** *Does domain semantics help large language models integrate open data for urban building
energy modeling? The Meta-Urban schema, a verified open-data catalog, and a reproducible alignment benchmark*

Shorter alternative: *Meta-Urban: a machine-actionable metadata schema and LLM alignment benchmark for open
data in urban building energy modeling*

**Core problem (one sentence).** UBEM depends on dozens of open datasets that describe the same buildings,
places and times with different variables, codes, units, granularities and statistical designs, and there is
no machine-actionable description of what each dataset is and how its variables relate to UBEM inputs, so every
project re-does the same manual integration, and LLMs that could automate it have no reference to align to and
no benchmark to be judged by.

**What is new compared with the 2023 version.**

| 2023 version | 2026 version |
|---|---|
| Narrative review, U.S.-centric, URLs | Verified catalog of open datasets (one YAML per dataset, ~90+), each coded on six facets, with inclusion criteria and verification dates |
| 7 categories mixing content, scale, channel | Faceted taxonomy: UBEM role x statistical nature x spatial granularity x temporal resolution x access/license x join keys |
| Table of field names | LinkML schema (`schema/meta_urban.yaml`) compiled to JSON Schema, SHACL and OWL; dataset level (DCAT-3 profile) plus variable level (units, code lists, weights) plus a SKOS concept vocabulary mapped to BEDES, Brick, CityGML Energy ADE and EnergyPlus |
| "Well developed / underdeveloped" opinion | Gap indicators computed from the catalog (coverage by role x granularity x region, openness, join-key availability) |
| 3 datasets, 1 ChatGPT session, no metrics | Benchmark with 3 tasks, gold labels, 5 prompting conditions (ablation of the schema's semantics), open-weight and frontier models, 5 repeats, lexical and embedding baselines |
| "LLM succeeded, so schema is good" | Hypothesis tests: does adding definitions, units and relations improve mapping accuracy and consistency over a flat field list? |
| None | Downstream check: does an alignment error change a UBEM quantity (weighted floor area and EUI by building type and census division from CBECS 2018)? Includes the cost of ignoring survey weights, the error the 2023 case study made |

## 2. Research questions

- **RQ1 (landscape).** Which UBEM workflow steps are well served by open data, at which spatial and temporal
  granularity, under which licenses, and with which join keys? Answered by computed indicators over the catalog.
- **RQ2 (representation).** Can one schema describe the datasets and their variables well enough to answer
  practical modeling queries? Answered by (a) competency questions executed against the catalog and
  (b) concept coverage: the share of variables in K real datasets that map to a Meta-Urban concept.
- **RQ3 (alignment).** Does giving an LLM the schema's semantics (definitions, units, hierarchy, mappings)
  improve dataset-profile extraction, variable-to-concept mapping and code/unit normalization, compared with no
  schema, the 2023 flat field list, and non-LLM baselines? How consistent are the results across repeats and
  across open-weight vs. frontier models?
- **RQ4 (consequence).** How large are the downstream errors in a UBEM quantity caused by alignment errors,
  and by statistical-design errors such as ignoring survey weights?

## 3. Benchmark design (`benchmark/`)

| Task | Input | Output | Gold label source | Metrics |
|---|---|---|---|---|
| T1 Dataset profile extraction | Publisher documentation text (landing page and codebook header, saved snapshot) | `DatasetProfile` JSON | Verified catalog entries | Field accuracy (exact for enums, normalized for strings, interval overlap for dates), macro-F1 per enum |
| T2 Variable-to-concept mapping | Variable name, label, codes (CBECS 2018, RECS 2020, EIA MER, BDG2 metadata, NYC LL84, ComStock metadata) | Meta-Urban concept id or `none` | Two-annotator labels with Cohen's kappa; adjudicated | Top-1 accuracy, macro-F1, `none` precision/recall, MRR for ranked outputs |
| T3 Code and unit normalization | Variable + codebook entry + raw values | Decoded labels, QUDT unit, SI conversion factor, weight flag | Generated deterministically from codebooks (exact gold) | Exact match, unit accuracy, weight-variable recall |

**Conditions (ablation of semantics).** C0 no schema; C1 the 2023 Table 1 field list; C2 concept ids and
labels only; C3 full Meta-Urban (definitions, units, broader/narrower, standard mappings); C4 C3 plus retrieved
top-k candidate concepts (retrieval-augmented).

**Models.** At least two open-weight models that can be run locally (for reproducibility) and two frontier API
models, each with exact model id and date. Temperature and seed fixed where the API allows; 5 repeats per item to
measure self-consistency (agreement rate, Fleiss' kappa across runs).

**Baselines.** TF-IDF lexical similarity, sentence-embedding similarity, and (if Jia Zou agrees) DataMorpher /
TreeMorpher for transformation tasks.

**Downstream (RQ4).** Pipeline that computes weighted floor area, weighted EUI, and building counts by
principal building activity and census division from CBECS 2018, run with (i) the gold mapping, (ii) each
model's mapping, (iii) unweighted records. Report relative error against EIA published tables.

## 4. Repository map (what is built here)

| Path | Content | Status |
|---|---|---|
| `schema/meta_urban.yaml` | LinkML schema v2.0 | built |
| `schema/vocab/ubem_concepts.yaml` | SKOS-style concept vocabulary with standard mappings | built (v0.1, needs co-author review) |
| `catalog/datasets/*.yaml` | Verified dataset profiles | built by research agents, needs author spot-check |
| `src/meta_urban/` | Loader, validator, catalog analytics, competency queries, benchmark harness, baselines, LLM runners | built |
| `benchmark/gold/` | Gold labels: T3 automatic; T2 draft labels to be verified by two annotators | partial |
| `scripts/` | Data download with checksums, figure and table generation | built |
| `paper/` | Manuscript draft, references, figures generated from scripts | draft |
| `legacy/2023-chatgpt-case-studies/` | The 2023 outputs kept for transparency and for the before/after comparison | copied |

## 5. Target journals (recommendation)

1. **Advanced Engineering Informatics** (best fit: semantics + AI + engineering data; publishes ontology and
   LLM benchmark papers).
2. **Energy and AI** or **Journal of Building Performance Simulation** (UBEM audience, accepts method papers
   with open benchmarks).
3. **Automation in Construction** (published the Brick occupant extension; strong on building information).

Avoid sending the same framing back to Applied Energy, SCS, B&E, BRI, Urban Informatics or E&B. If the catalog
grows large, a separate *Scientific Data* data descriptor for the catalog is a natural second paper.

## 6. Decisions (updated 2026-11-13)

- [x] Target journal: Automation in Construction, subscription route (backup: Computers, Environment and
      Urban Systems). Excluded by the authors: AEI, Building Simulation, Building and Environment, SoftwareX,
      Energy and Buildings, JBPS, Applied Energy, and open-access-only journals. One paper, not split.
- [x] LLMs: two local open-weight models (Qwen3 8B, Llama 3.1 8B); frontier runs dropped (no API budget), the
      harness supports them.
- [x] T1 dropped: its gold would be the LLM-drafted catalog.
- [x] T2 gold: two blind LLM annotators plus blind adjudication; first-author audit of 50 labels pending.
- [x] Catalog: random 20-entry field-level re-verification, errors corrected.
- [x] Vocabulary mappings to Brick 1.4.4, BEDES 2.5 and Energy ADE 1.0, verified against release files.
- [x] 2023 expert survey not used.
- [ ] Author list, order and CRediT roles (Jianli Chen, Jia Zou).
- [ ] Funding statement and competing interests.
- [x] Repository public (2026-11-13) with MIT (code) and CC BY 4.0 (schema, catalog, benchmark); no Zenodo archive.
