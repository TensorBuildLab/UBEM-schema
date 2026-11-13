---
title: "Does domain semantics help large language models integrate open data for urban building energy modeling? The Meta-Urban schema, a verified open-data catalog, and a reproducible alignment benchmark"
short_title: "Meta-Urban: schema, catalog and LLM alignment benchmark for UBEM open data"
authors: "Liang Zhang (University of Arizona; National Laboratory of the Rockies), Jianli Chen (University of Utah), Jia Zou (Arizona State University) [TODO: confirm author list, order, and whether the T2 annotator joins]"
status: "DRAFT v0.1, 2026-11-12. Results marked [TODO] or PROVISIONAL are not final."
bibliography: references.bib
---

<!-- Drafting conventions: American spelling; "Fig. N"; "38%" without space; no em-dashes. Citation keys refer
to paper/references.bib (all entries verified against Crossref, arXiv or official pages on 2026-11-12). -->

## Highlights

- Meta-Urban 2.0: a LinkML schema for open UBEM data, compiled to JSON Schema, SHACL and OWL
- Verified catalog of 91 open datasets coded on six independent facets
- Only 3 of 48 non-geometric building datasets can be linked to individual buildings
- Ignoring survey weights shifts CBECS energy use intensity by -16% to +102% by building type
- Concept definitions, not labels, raise LLM mapping accuracy by 16 points [PROVISIONAL]

## Abstract

Urban building energy modeling (UBEM) draws on dozens of open datasets that describe the same buildings,
places and periods with different variables, codes, units, spatial granularities and statistical designs.
Integrating them is still manual, and the descriptions that exist are written for people to read, not for
software or large language models (LLMs) to act on. This paper asks whether a domain schema makes that
integration more reliable. We present Meta-Urban 2.0, a schema with a dataset level (an application profile
of DCAT 3 with six UBEM facets: workflow role, statistical nature, spatial granularity, temporal resolution,
access, and join keys) and a variable level (concept, unit, code list, aggregation, weights and imputation
flags), with an 81-concept vocabulary mapped to CityGML and EnergyPlus weather fields. We used it to build a
catalog of 91 open datasets, each verified against its publisher. Computed indicators show that geometry and
weather are well covered at building or station resolution, but only 3 of 48 datasets that carry
characteristics, operation, energy or simulation data share an identifier with building footprints, and 21
have no usable key at all. We then define a benchmark with three tasks on the CBECS 2018 and RECS 2020
codebooks (2,048 variables): dataset-profile extraction, variable-to-concept mapping, and code and unit
normalization, and test four levels of schema context with open-weight and frontier LLMs over five repeats.
PROVISIONAL (draft labels): for two 8-billion-parameter open-weight models, concept definitions raised top-1
mapping accuracy from 0.38-0.41 to 0.53-0.57, while concept labels alone did not help; retrieving ten
candidates first kept that accuracy at 18% of the input tokens. [TODO: update with adjudicated gold and
frontier models.] Finally, we show that alignment errors matter downstream: a correct
pipeline reproduces EIA's published totals within 0.01%, whereas ignoring survey weights changes building
counts by three orders of magnitude and floor-area-weighted energy use intensity by -16% to +102% across
building types. The schema, catalog, benchmark, code and all results are open.

**Keywords:** urban building energy modeling; open data; metadata schema; FAIR; large language models;
schema matching; building stock; CBECS

## 1. Introduction

Buildings account for [TODO: one sourced statistic, e.g., share of U.S. or global energy-related emissions,
with citation] and urban building energy modeling (UBEM) is the standard way to estimate how policies,
technologies and climate change will affect a whole building stock [@reinhart2016urban; @ferrando2020urban;
@johari2020urban; @hong2020ten]. Bottom-up, physics-based UBEM needs weather, the location and shape of every
building, non-geometric characteristics such as use type, vintage and systems, assumptions on how buildings
are operated, and measured energy use to calibrate and validate the result [@cerezodavila2016modeling;
@wang2022data; @malhotra2022information]. Almost every one of these inputs now has an open source.

The difficulty is not finding data. It is combining it. Weather comes as station records, reanalysis grids
or typical years; footprints come as polygons from remote sensing, crowdsourcing or cadastres; building
characteristics come as weighted sample surveys released at census-division level; measured energy comes as
anonymized meters without location, or as utility totals by service territory. Each source codes its
variables differently: the 2018 Commercial Buildings Energy Consumption Survey (CBECS) writes `1=New
England`, the 2020 Residential Energy Consumption Survey (RECS) writes `1 Mobile home`, the first reports
energy in thousand Btu and floor area in square feet, and both ship hundreds of imputation flags and
replicate weights next to the data. Chen et al. [@chen2019development] found that cities usually have
enough public data for UBEM but that the data lack standard formats and common keys. Reviews since then
have catalogued inputs and sources for people to read [@goy2020data; @wang2022data; @jin2023review;
@bishop2024review; @anselmo2026urban], and Malhotra et al. [@malhotra2022information] found that most UBEM
studies cannot be reproduced. Standards such as CityGML and its Energy ADE describe buildings and their
energy systems [@groger2012citygml; @kutzner2020citygml; @agugiaro2018energy], but not the datasets that
feed them: their granularity, statistical design, license and the keys that link one to another.

Large language models (LLMs) are an obvious candidate to automate this integration, and the schema-matching
literature now uses them routinely [@narayan2022foundation; @sheetrit2024rematch; @liu2025magneto;
@parciak2024schema]. Two things are missing for UBEM. First, a target: an LLM can only align data to a
schema that exists in machine-actionable form. Second, evidence: results on public benchmarks overestimate
LLMs on real data [@kayali2025goby], outputs vary from run to run [@buss2025scalable], and in buildings,
mapping real BACnet point names to Brick classes reaches only 27% to 36% accuracy [@jain2025bacnetbrick].
Whether a domain schema actually helps, as opposed to any list of field names, has not been tested.

An earlier preprint of this work [@zhang2023taxonomy] proposed a taxonomy, a per-category table of metadata
fields, and three single-session ChatGPT demonstrations. It did not test whether the schema helped, did not
release the schema in machine-readable form, and on re-examination its demonstrations contained errors
(Section 6.4). This paper replaces it. It asks four questions:

- **RQ1.** Which UBEM workflow steps are well served by open data, at which granularity, under which access
  terms, and with which keys that allow records to be linked to buildings?
- **RQ2.** Can a single schema describe these datasets and their variables well enough to answer practical
  modeling queries?
- **RQ3.** Does giving an LLM the schema's semantics (definitions, units, hierarchy) improve alignment over
  identifiers alone, labels alone, and non-LLM baselines, and how consistent are the results?
- **RQ4.** How much do alignment and statistical-design errors change UBEM quantities?

The contributions are:

1. Meta-Urban 2.0, a schema written in LinkML [@moxon2025linkml] and compiled to JSON Schema, SHACL and OWL,
   with a dataset level that profiles DCAT 3 [@w3c2024dcat3] and a variable level with units (QUDT), code
   lists, aggregation semantics, weights and imputation flags, plus an 81-concept SKOS vocabulary (Section 3).
2. A catalog of 91 open datasets coded with the schema and verified against publisher pages, and computed
   gap indicators, including a new linkage indicator (Section 4).
3. An alignment benchmark with three tasks, gold labels, four levels of schema context, and a protocol that
   follows current schema-matching practice (Section 5).
4. A downstream analysis on CBECS 2018 that quantifies the effect of each class of alignment error on UBEM
   quantities (Section 6).
5. An open repository from which every number and figure in this paper is regenerated
   (https://github.com/TensorBuildLab/UBEM-schema).

## 2. Related work

### 2.1 Open data for UBEM

UBEM reviews agree that data are the main bottleneck [@reinhart2016urban; @johari2020urban;
@ali2021review; @kamel2022systematic; @hong2025ten]. Goy et al. [@goy2020data] related data availability
to the choice of UBEM approach. Chen et al. [@chen2019development] built a standardized city buildings
dataset from heterogeneous city data. Wang et al. [@wang2022data] classified UBEM inputs into geometric,
non-geometric, weather and calibration data and assessed their availability and cost. Jin et al.
[@jin2023review] reviewed more than 190 open city-level building energy datasets. Bishop et al.
[@bishop2024review] organized multi-domain urban energy data into seven domains with formats and sources.
Anselmo et al. [@anselmo2026urban] reviewed the integration of GIS and remote sensing in UBEM. On the GIS
side, open footprints and heights now cover most of the world [@heris2020rasterized; @sirko2021continental;
@milojevicdupont2023eubucco; @esch2022world; @pesaresi2024advances], with known completeness gaps in
crowdsourced data [@haklay2008openstreetmap], and data quality measurably changes UBEM results
[@nouvel2017influence].

**Gap.** These works are inventories and categorizations for human readers. None releases a machine-actionable
profile per dataset, none separates the dimensions along which datasets differ, and none measures whether
datasets can be linked to individual buildings.

### 2.2 Semantic models for buildings and cities

At building scale, Brick, Haystack, RealEstateCore, BOT, SAREF4BLDG, BuildingSync, BEDES and the proposed
ASHRAE 223P standardize equipment, points and building descriptions [@balaji2018brick; @haystack4;
@hammar2019realestatecore; @rasmussen2021bot; @etsi2025saref4bldg; @long2021buildingsync; @bedes;
@ashrae223p]; Pritoni et al. [@pritoni2021metadata] compared them. At city scale, CityGML 3.0 and the Energy ADE
model buildings, their thermal zones and energy systems [@kutzner2020citygml; @agugiaro2018energy;
@agugiaro2026further], and urban energy ontologies support specific workflows [@corrado2015data;
@allan2020linked; @chadzynski2021semantic; @ma2024ontology]. Dataset-level metadata is the domain of DCAT,
schema.org and the FAIR principles [@w3c2024dcat3; @schemaorgDataset; @wilkinson2016fair].

**Gap.** Building and city models describe objects, not datasets. Generic dataset vocabularies have no notion of
a UBEM workflow role, a survey weight, a top-code or a join key. Meta-Urban sits between them and maps to both
rather than replacing either.

### 2.3 LLMs for schema matching and data integration

Schema matching has a long history [@rahm2001survey; @do2002coma; @melnik2002similarity] and a standard
benchmark suite [@koutras2021valentine]. LLMs entered with Narayan et al. [@narayan2022foundation], and the
current design is retrieve-then-rerank: a retriever proposes candidate targets and an LLM chooses
[@sheetrit2024rematch; @liu2025magneto; @seedat2024matchmaker]. Studies report that both too little and too
much context hurt [@parciak2024schema; @gan2026lessismore], that outputs are inconsistent across runs
[@buss2025scalable], and that confidence estimates need calibration [@wang2023selfconsistency;
@xiong2024uncertainty]. In buildings, language models have been used for schema matching of energy data
[@pan2022semantic], LLM-generated SQL for data transformation [@sharma2023sqlmorpher;
@sharma2025datamorpher], Brick metadata [@mulayim2024llmontologies; @zheng2025bmstagging;
@wang2026point2brick; @jain2025bacnetbrick] and UBEM itself [@choi2024gpt].

**Gap.** No benchmark exists for aligning open UBEM data, and no study has ablated the semantic content of the
target schema to test whether it, rather than the LLM, drives accuracy.

Table 1 places this paper among the closest prior work.

Table 1. Closest prior work and what this paper adds. Y: yes; P: partly; -: no.

| Work | Dataset inventory | Facets separated | Machine-actionable profile | Variable-level semantics | Linkage indicator | LLM benchmark with gold |
|---|---|---|---|---|---|---|
| Goy et al. 2020 [@goy2020data] | P | - | - | - | - | - |
| Wang et al. 2022 [@wang2022data] | P | - | - | - | - | - |
| Malhotra et al. 2022 [@malhotra2022information] | - | P | - | - | - | - |
| Jin et al. 2023 [@jin2023review] | Y | - | - | - | - | - |
| Bishop et al. 2024 [@bishop2024review] | Y | P | - | - | - | - |
| CityGML Energy ADE [@agugiaro2018energy] | - | - | Y (objects) | Y (objects) | - | - |
| Zhang et al. 2023 preprint [@zhang2023taxonomy] | P | - | - | P | - | - (3 demos) |
| This paper | Y (91, verified) | Y (6) | Y (LinkML) | Y | Y | Y |

## 3. The Meta-Urban 2.0 schema

### 3.1 Design requirements

We derived six requirements from the UBEM workflow and from the failures of the 2023 version. R1: say which
workflow step a dataset can feed. R2: say how fine its locations and time steps are, separately. R3: say how
it was produced, because a weighted survey, a remote-sensing product and a simulation must be handled
differently. R4: say how it can be joined to other data. R5: at variable level, say what each column means,
in which unit, with which codes, and whether it is data, a weight or a flag. R6: be machine-validated and
reuse existing standards.

### 3.2 A faceted taxonomy

The 2023 taxonomy listed seven categories that mixed three different things: content (weather, geometry),
spatial scale ("macroscopic" vs. "microscopic" energy data) and distribution channel ("data lake"). A dataset
such as the Building Data Genome Project fell into two categories at once. Meta-Urban 2.0 replaces the list
with six independent facets (Table 2), so that a dataset is a point in a six-dimensional space and gaps can
be counted along each.

Table 2. Facets of the Meta-Urban taxonomy (controlled values in `schema/meta_urban.yaml`).

| Facet | Values |
|---|---|
| UBEM workflow role | boundary conditions; geometry and inventory; building characteristics; operation and use; calibration and validation; reference simulation; context and coupling |
| Statistical nature | census; weighted sample survey; administrative record; measured monitoring; remote-sensing derived; crowdsourced; reanalysis; typical year; climate projection; simulation; standard or code; compilation |
| Spatial granularity (finest public) | 17 ordered levels from building or station to nation, plus none and unknown |
| Temporal resolution | ISO 8601 duration, static, or irregular |
| Access | open download; open API; free registration; request or agreement; restricted or commercial |
| Join keys | 25 key types, from UBID, parcel id and address to census geographies, grid cells, climate zones and timestamps |

### 3.3 Dataset and variable levels

The `DatasetProfile` class profiles `dcat:Dataset`: title, publisher, license, DOI, descriptor paper,
distributions, the six facets, coverage, record count, sampling weights, known limitations and the provenance
of the profile itself (who verified it, when, against which pages). A schema rule requires every weighted
sample survey to name its weights. The `VariableProfile` class profiles `csvw:Column`: the concept it maps to
and the mapping relation (SKOS exact, close, broad, narrow, related), the QUDT unit and a multiplier (CBECS
reports energy in thousand Btu), aggregation semantics (static, instantaneous, total or average over a
period), the entity it describes, the code list, missing-value codes, and two flags that the 2023 version
lacked: whether the variable is a sampling weight and whether it is an imputation flag for another variable.

### 3.4 Concept vocabulary

The vocabulary (`schema/vocab/ubem_concepts.yaml`) has 81 concepts: 8 grouping concepts and 73 mapping
targets organized by workflow role with `skos:broader`. Each target has a definition, the entity it
describes, a QUDT quantity kind and canonical unit where applicable, generic synonyms, and mappings to
CityGML 2.0 building attributes and EnergyPlus weather file fields. [TODO (co-authors): add BEDES, Brick and
Energy ADE mappings after expert review; only mappings the authors are certain of are recorded.]

### 3.5 Implementation

The schema is written in LinkML and compiled to JSON Schema (used by the validator), SHACL shapes and an OWL
ontology. Catalog entries are YAML files validated in continuous integration. [TODO: register the w3id.org
namespace.]

## 4. A verified catalog of open UBEM data (RQ1, RQ2)

### 4.1 Method

Inclusion criteria were: data obtainable at no cost (directly or after free registration), feeding at least
one UBEM workflow role, and of national, multinational or global scope, or a city dataset that serves as a de
facto reference. Widely used datasets that need an agreement or payment were kept and flagged, so that the
gap analysis can count them. Each entry was drafted by an LLM research agent (Claude, Anthropic; November
2026) instructed to fill every field only from the publisher's page or a peer-reviewed descriptor, to resolve
every DOI through Crossref, to write null rather than guess, and to list the pages it checked. Every entry was
then validated against the schema. [TODO (authors): spot-check at least 20 entries against publisher pages,
prioritizing fields the agents left null; report the error rate found. This step is required before
submission.]

### 4.2 Landscape

The catalog holds 91 datasets: 15 boundary-condition, 23 geometry, 15 characteristics, 7 operation, 21
calibration, 5 reference-simulation and 5 context datasets (by primary role). Of these, 35 cover the United
States only and 23 are global. 93% can be obtained without an agreement, but only 65% state a license that
we could verify, 27% have a persistent identifier, and 43% have a peer-reviewed descriptor.

Fig. 1 crosses workflow role with spatial granularity. Geometry is the best-served role: 18 of 23 datasets
release individual buildings. Weather is released at stations (5) or on grids coarser than 1 km (10).
Building characteristics are the opposite: 6 of 15 datasets release nothing finer than state, region or
nation, and the two main U.S. surveys stop at census division (CBECS) and state (RECS). Ten of 21 calibration
datasets release no location at all, because meters are anonymized.

![Fig. 1. Number of catalog datasets by primary UBEM workflow role and the finest spatial granularity they
release publicly. Darker cells hold more datasets.](figures/fig_role_by_granularity.png)

![Fig. 2. Access terms by primary role. Blue: obtainable without an agreement; gray: agreement or commercial
license required.](figures/fig_role_by_access.png)

### 4.3 Linkage to buildings

Granularity alone does not say whether a record can be attached to a building. We therefore classified every
dataset by its best way of linking to individual building footprints: a shared identifier (UBID, cadastral
parcel id, address), building-precise location (coordinates or geometry at building granularity), area codes
only, attributes only (building type, vintage), or none. A dataset-internal record id does not count. Of the
48 datasets whose primary role is characteristics, operation, calibration or reference simulation, 3 share an
identifier with footprints (all are administrative: energy certificates and benchmarking disclosure), none
offers building-precise location without an identifier, 23 can be linked only through area codes, and 21 have
no usable key (Table 3). For most of open UBEM, therefore, characteristics and energy can be joined to
geometry only statistically, by area and building type, never record by record. This is a stronger and more
specific statement than "data lack common keys" [@chen2019development], and it points to the identifier
(UBID or parcel) rather than to more data as the missing piece.

Table 3. Linkage class by primary role (generated: `paper/tables/catalog_linkability.csv`).

| Role | Shared identifier | Building location | Area code | Attribute only | None |
|---|---|---|---|---|---|
| Boundary conditions | 0 | 0 | 15 | 0 | 0 |
| Geometry and inventory | 2 | 16 | 5 | 0 | 0 |
| Building characteristics | 2 | 0 | 9 | 0 | 4 |
| Operation and use | 0 | 0 | 4 | 1 | 2 |
| Calibration and validation | 1 | 0 | 7 | 0 | 13 |
| Reference simulation | 0 | 0 | 3 | 0 | 2 |
| Context and coupling | 0 | 0 | 5 | 0 | 0 |

### 4.4 Competency questions

Ontology engineering tests a schema with competency questions it must answer. We wrote six and executed
them as queries over the catalog (`paper/tables/competency.md`). For example, "which open datasets report
measured energy at building or meter level?" returns ten datasets, none of which carries an identifier or
building-precise location in its profile that would link it to a footprint (Liang: verify BDG2 site
coordinates), and "which datasets lack an explicit license?" returns 32, including most weather products. The answers
depend only on the schema's facets, which shows that the profiles are machine-actionable (RQ2). [TODO: decide
whether to keep CQ results that depend on agent-filled fields not yet spot-checked.]

## 5. Alignment benchmark (RQ3)

### 5.1 Tasks and data

The benchmark uses the public codebooks of CBECS 2018 (1,249 variables) and RECS 2020 (799 variables), which
differ in format, units and conventions, and together contain 733 imputation flags and 213 sampling weights.

- **T1, dataset-profile extraction.** Input: a saved snapshot of the publisher's documentation. Output: a
  `DatasetProfile`. Gold: the verified catalog entries. Metrics: field accuracy, macro-F1 per facet.
- **T2, variable-to-concept mapping.** Input: variable name, label, questionnaire section and up to eight
  codes. Output: one concept id or `none`, two alternatives and a confidence. Gold: two independent human
  annotators with adjudication, starting from rule-based draft labels (Section 5.2). Evaluation sample: 300
  substantive variables (150 per survey), stratified by concept, fixed seed. Metrics: Acc@1, Acc@3, MRR,
  macro-F1, precision and recall of `none`.
- **T3, code and unit normalization.** Input: the verbatim codebook entry. Output: weight and imputation
  flags, the flagged variable, unit and multiplier, missing codes and code list. Gold: derived exactly from
  the codebook. Metrics: field accuracy, code-list Jaccard.

### 5.2 Gold labels

T3 gold is derived deterministically and unit-tested. For T2, documented rules (`meta_urban.gold_draft`)
pre-fill a draft label for every variable; they map 92.2% of the 1,104 substantive variables to 46 distinct
concepts, and they were used only to stratify the evaluation sample. Two annotators then label the sample
blind and independently: they see the variable and the vocabulary but neither the draft label nor any model
output, because the provisional runs showed draft labels that annotators would likely have accepted although
they are wrong (Section 5.5). Each annotator records the most specific concept and, for variables that
genuinely fit two concepts, the other acceptable ones; we report strict and lenient accuracy. We report
Cohen's kappa and the share of draft labels each annotator changed, and adjudicate disagreements in
discussion (protocol in `benchmark/gold/README.md`). [TODO: run annotation; report kappa.]

### 5.3 Conditions

Four levels of target context test what the schema contributes: **L0** concept ids only; **L1** ids and
preferred labels; **L2** full semantics (definition, broader concept, entity, canonical unit, synonyms);
**L3** L2 restricted to the top 10 candidates from the lexical retriever (retrieve-then-rerank). For T1, the
contrast is free-form metadata, the 2023 field list, and the Meta-Urban JSON Schema with enum definitions.
[TODO: confirm conditions with co-authors.]

### 5.4 Models, baselines and protocol

Baselines are a TF-IDF lexical matcher (word and character n-grams) and a sentence-embedding matcher.
Models: two open-weight models run locally through Ollama 0.40.16 on a laptop GPU (Qwen3 8B and Llama 3.1
8B, both 4-bit quantized, thinking disabled, 8,192-token context; run 12-13 November 2026) and [TODO:
frontier models, e.g., Claude Opus 5.5; record exact model ids and dates]. Outputs are constrained to a JSON
schema whose concept field is an enumeration of the vocabulary, so every answer is a valid concept id. Each condition is run five times at temperature 0.7 to measure self-consistency (pairwise
agreement, unanimous share, standard deviation of accuracy), and once at temperature 0 for the point
estimate. All prompts and raw responses are cached and released. We report token cost and a
coverage-accuracy curve that accepts mappings above a confidence threshold and routes the rest to a human.

### 5.5 Results

PROVISIONAL. All numbers in this section are scored against the rule-based draft labels and will change once
the adjudicated gold exists; the gold is read at scoring time, so no model needs to be re-run. They are given
here to fix the analysis, not to be cited. Frontier-model results are pending.

**Task T2.** Table 4 and Fig. 3 report top-1 accuracy on the 277 mappable items of the sample (23 have no
applicable concept). Both open-weight models beat the lexical baseline at every level. Concept ids alone
(L0) already give 0.38-0.40, because many ids are readable names; adding preferred labels (L1) changes
little (+0.03 and -0.02, exact McNemar p = 0.12 and 0.42). Adding definitions, broader concepts, entities,
units and synonyms (L2) is what helps: +0.16 over L1 for both models (Qwen3: 53 items gained, 8 lost;
Llama 3.1: 57 gained, 13 lost; both p < 0.001). The two models do not differ significantly at any level
(p >= 0.28).

Table 4. T2 variable-to-concept mapping, provisional (draft labels). Acc@1 with bootstrap 95% interval,
Acc@3 and MRR on 277 mappable items at temperature 0; macro-F1 and recall of `none` on all 300 items;
agreement is the mean pairwise agreement of five repeats (one at temperature 0, four at 0.7). Tokens: mean
input tokens per call. Generated: `paper/tables/bench_t2_main.csv`.

| Method | Level | Acc@1 [95% CI] | Acc@3 | MRR | Macro-F1 | `none` recall | Agreement | Tokens |
|---|---|---|---|---|---|---|---|---|
| Lexical TF-IDF | - | 0.31 [0.25, 0.36] | 0.60 | 0.47 | 0.37 | 0.00 | - | - |
| Llama 3.1 8B | L0 | 0.40 [0.34, 0.45] | 0.69 | 0.54 | 0.36 | 0.00 | 0.79 | 477 |
| Llama 3.1 8B | L1 | 0.38 [0.32, 0.43] | 0.62 | 0.49 | 0.39 | 0.17 | 0.87 | 800 |
| Llama 3.1 8B | L2 | 0.53 [0.48, 0.59] | 0.79 | 0.65 | 0.48 | 0.13 | 0.91 | 3,873 |
| Llama 3.1 8B | L3 | 0.53 [0.47, 0.59] | 0.71 | 0.62 | 0.50 | 0.43 | 0.91 | 701 |
| Qwen3 8B | L0 | 0.38 [0.32, 0.44] | 0.53 | 0.45 | 0.43 | 0.04 | 0.98 | 486 |
| Qwen3 8B | L1 | 0.41 [0.35, 0.47] | 0.57 | 0.49 | 0.48 | 0.09 | 0.98 | 809 |
| Qwen3 8B | L2 | 0.57 [0.52, 0.63] | 0.72 | 0.64 | 0.53 | 0.09 | 0.98 | 3,884 |
| Qwen3 8B | L3 | 0.53 [0.48, 0.59] | 0.69 | 0.61 | 0.52 | 0.30 | 0.98 | 710 |
| [TODO: frontier] | | | | | | | | |

![Fig. 3. Top-1 accuracy of variable-to-concept mapping by level of schema context (PROVISIONAL, draft
labels). Error bars: bootstrap 95% intervals. Dashed line: lexical baseline.](figures/fig_t2_levels.png)

Retrieve-then-rerank (L3) matches full semantics at 18% of the input tokens (about 705 instead of 3,880 per
call); the difference from L2 is not significant (Qwen3 -0.04, p = 0.28; Llama 3.1 0.00). Its ceiling is the
retriever: the gold concept is among the ten lexical candidates for 221 of 277 items (80%). On those items L3
is more accurate than L2 (0.67 for both models, against 0.61), and on the other 56 it cannot be right, whereas
L2 still recovers 25% (Llama 3.1) to 43% (Qwen3) of them. A better retriever, not a larger prompt, is
therefore the cheaper route to higher accuracy. L3 also makes the models abstain more often: recall of
`none` rises from 0.09-0.13 to 0.30-0.43, at the cost of more false abstentions (6-11% of items against
1-4%).

Errors show what the semantics do (`paper/tables/bench_t2_errors.csv`). At L0, 30% of Qwen3's answers (13%
of Llama 3.1's) fall in a different top-level group than the gold concept, such as an energy concept for a
system variable; at L2 these drop to 15% and 7%. Most remaining errors stay within the right group (23% and
32% of items at L2), and many of these are where the draft labels are weakest: both models agree with each
other and against the draft on 43 items at L2. Some of these are plain draft errors (a lighting type labeled
as energy use intensity because its name contains "intensity"; an induction cooktop labeled as a ventilation
system), and some are genuinely ambiguous, such as the CBECS and RECS indicators "natural gas used for water
heating", which are both energy-source flags and water-heating attributes. The blind, two-annotator gold with
acceptable alternatives (Section 5.2) is designed for exactly these cases; the provisional accuracies are
therefore likely to be lower bounds.

Repeated runs are stable. The standard deviation of accuracy across five repeats is at most 0.015, and
Qwen3's five repeats agree pairwise on 98% of items; Llama 3.1 is less consistent (79-91%). Self-consistency
is therefore not a useful signal of correctness for these models (Fig. 4): accepting only unanimous answers
keeps 95% of Qwen3's mappings at almost unchanged accuracy. Qwen3's own confidence is more useful (accepting
answers with confidence of at least 0.95 maps 51% of variables at 0.78 accuracy), Llama 3.1's is not, and
agreement across conditions is the most model-agnostic signal: when both models agree at both L2 and L3, 36%
of variables are mapped at 0.78 accuracy. This suggests a human-in-the-loop design in which agreement between
cheap runs decides what a person must review.

![Fig. 4. Coverage and accuracy when only some mappings are accepted automatically (L2, PROVISIONAL). Lines:
threshold on the model's own confidence. Markers: accept only when the five repeats are unanimous, when L2
and L3 agree, or when both models agree at both levels.](figures/fig_t2_coverage.png)

**Task T3.** Because the T2 sample excludes imputation flags and replicate weights, T3 adds a fixed supplement
of 60 imputation flags and 30 replicate weights (seed 20261113; `benchmark/inputs/t3_extra_sample.csv`), so
that detection is measured on positives as well as negatives. Table 5 reports each field on the items where
it is informative. Both models detect weights, replicate weights and imputation flags almost perfectly, with
no false alarms on the 300 substantive variables. Two failures stand out. First, finding the variable that an
imputation flag refers to: both models are always right when the codebook names it (RECS: "Imputation
indicator for DRYER") and never right when it must be inferred from the naming convention (CBECS: "Imputation
flag: Months in use" for `ZMONUSE`, which flags `MONUSE`); they return the flag's own name instead. The
convention is documented in the survey's user guide, not in the codebook entry, which is the kind of
dataset-level knowledge the Meta-Urban profile is meant to carry. Second, units and missing codes: Qwen3 gets
the unit right for 96% of variables with a unit and the multiplier for 96% of scaled units, while Llama 3.1
gets 80% and 79%. Missing-value codes match the codebook exactly in only 20-32% of answers (26-57% when an
empty-string entry that both models add by habit is ignored), and some answers include codes the codebook
does not define.

Table 5. T3 code and unit normalization, three repeats per item (one at temperature 0, two at 0.7). Gold is
derived exactly from the codebooks. Generated: `paper/tables/bench_t3_fields.csv`.

| Field (items scored) | Qwen3 8B | Llama 3.1 8B |
|---|---|---|
| Valid JSON (390 items) | 1.00 | 0.99 |
| Weight detected (32 weights) / false alarm | 1.00 / 0.00 | 1.00 / 0.00 |
| Replicate weight detected (30) / false alarm | 0.98 / 0.00 | 1.00 / 0.00 |
| Imputation flag detected (60) / false alarm | 1.00 / 0.00 | 1.00 / 0.00 |
| Flagged variable, RECS (label names it; 30) | 1.00 | 1.00 |
| Flagged variable, CBECS (convention only; 30) | 0.00 | 0.00 |
| Unit (52 variables with a unit) | 0.96 | 0.80 |
| Unit given where there is none | 0.04 | 0.06 |
| Multiplier, scaled units (31) | 0.96 | 0.79 |
| Missing codes, exact / ignoring empty strings | 0.32 / 0.57 | 0.20 / 0.26 |
| Code list, mean Jaccard | 0.74 | 0.68 |

Combined with the sensitivities in Table 6, the multiplier errors matter most: each miss on an energy variable
changes its total by a factor of 1,000, so a pipeline built on Llama 3.1's answers would carry such an error
in about one in five scaled energy variables unless a plausibility check catches it. Weight and flag detection,
by contrast, is reliable enough to automate.

## 6. Do alignment errors matter downstream? (RQ4)

### 6.1 Reference pipeline

Applying the CBECS final weights (`FINALWT`) to the public microdata gives 5,918 thousand buildings, 96,527
million square feet and 6,789 trillion Btu of major-fuel consumption. These match EIA's published Tables B1
and C1 to within 0.01%, which validates the pipeline used as the reference below.

### 6.2 Ignoring the survey design

The 2023 case study processed CBECS records without weights. Doing so reports 6.4 thousand buildings instead of
5.9 million. Less obviously, it also biases intensities. Fig. 5 compares the floor-area-weighted energy use
intensity (EUI) by principal building activity with and without weights. For the 16 activities that hold at
least 0.5% of buildings, the unweighted EUI is off by -16% (food sales) to +102% (other), with 12 of 16
overestimated: retail other than mall +45%, public assembly +31%, outpatient health care +27%. Inpatient
health care holds 4.3% of records but 0.1% of buildings, so unweighted counts also distort the stock mix that
archetype-based UBEM samples from.

![Fig. 5. Error in floor-area-weighted EUI by principal building activity when CBECS 2018 survey weights are
ignored, relative to the weighted estimate. Activities with at least 0.5% of weighted buildings are shown.](figures/fig_weights_eui_error.png)

### 6.3 Sensitivity to each normalization error

Table 6 injects each T3 error type into the reference pipeline. Unit errors are the most damaging (a dropped
"thousand" multiplier or a Btu-kWh confusion changes national EUI by -99.9% or +241%), but they are also the
easiest to catch with a plausibility check. Top-codes read as values are subtler: CBECS codes buildings with
10 to 14 floors as 994 and 15 or more as 995, and treating these as numbers raises the weighted mean number of
floors by 179%. A withheld climate-zone code kept as a category shifts the hot-zone share by only 2.5%. These
sensitivities, combined with each model's T3 error rates, give the expected downstream error of each model.
[TODO: combine with T3 results.]

Table 6. Effect of single normalization errors on CBECS 2018 quantities (generated:
`paper/tables/downstream_d3_sensitivity.csv`).

| Error type | Quantity | Correct | With error | Relative error |
|---|---|---|---|---|
| Unit multiplier dropped (thousand Btu read as Btu) | National EUI (kWh/m2) | 221.9 | 0.22 | -99.9% |
| Wrong unit (thousand Btu read as kWh) | National EUI (kWh/m2) | 221.9 | 757.1 | +241% |
| ft2 read as m2 | Total floorspace (million m2) | 8,968 | 96,527 | +976% |
| Top-codes read as values (NFLOOR 994/995) | Weighted mean floors | 1.46 | 4.08 | +179% |
| Withheld code kept (PUBCLIM 7) | Share in hot zone | 0.138 | 0.135 | -2.5% |
| Survey weights ignored | Buildings (thousand) | 5,918 | 6.4 | -99.9% |

Note: for NFLOOR the correct value assumes 12 floors for code 994 and 15 for code 995 (midpoint and lower bound).

### 6.4 What went wrong in 2023

Re-examined with the gold labels, the 2023 outputs [@zhang2023taxonomy] were not "accurate" as reported: the
coverage of CBECS was returned as raw codes ("Regions: [3 4 1 2]"), the weights were dropped, and the EIA
monthly series was given a timestamp format with hours and seconds. These are exactly the error types that
T3 now measures. The legacy outputs are kept in the repository for comparison.

## 7. Discussion

[TODO after results: answer RQ3 in a calibrated way ("the results support a qualified yes / no").]

**Implications for UBEM practice.** Three recommendations follow from Sections 4 and 6 regardless of the LLM
results. (i) Treat weights, top-codes and imputation flags as part of the data contract; a pipeline that does
not read them is wrong even when every value is transcribed correctly. (ii) Invest in identifiers (UBID,
parcel) rather than in more datasets: without them, characteristics and energy can only be joined to
geometry statistically. (iii) Publish machine-actionable profiles with explicit licenses; a third of the
catalog has none we could verify.

**What the schema does not do.** Meta-Urban describes datasets and the meaning of their variables. It does
not model buildings, thermal zones or systems, which CityGML and the Energy ADE already do; it maps to them.

**Limitations.** The catalog is agent-drafted and author-checked, and it is a purposive sample of national
and global datasets, not an exhaustive census; city portals are out of scope. The benchmark uses two U.S.
surveys for T2 and T3; [TODO: add one non-U.S. dataset, e.g., UK EPC or EUBUCCO attributes, if time
allows]. The vocabulary is version 0.1 and will change as annotators find missing concepts. LLM results
depend on model versions that will be retired; we release prompts and raw outputs so that the comparison can
be repeated with new models.

## 8. Conclusions

[TODO: restate the questions; list findings with numbers; end on the recommendation, not the limitation.]

## Code and data availability

All code, the schema and its generated artifacts, the catalog, gold labels, prompts, cached model outputs,
and the scripts that produce every table and figure are at https://github.com/TensorBuildLab/UBEM-schema
[TODO: make public and archive a release on Zenodo with a DOI at submission]. Source data are downloaded from
EIA by `scripts/download_data.py`, which records SHA-256 checksums.

## Declaration of generative AI use

Claude (Anthropic) was used to draft catalog entries under the verification protocol in Section 4.1, to
verify references, to write code, and to edit text. LLMs are also the object of study in Section 5. The
authors reviewed all content and take full responsibility for it. [TODO: adapt to the journal's required
wording.]

## Acknowledgments

[TODO: funding statement; acknowledge experts who provided input in 2023 only if they agree to be named.]

## CRediT authorship contribution statement

[TODO]

## References

<!-- generated from references.bib -->
