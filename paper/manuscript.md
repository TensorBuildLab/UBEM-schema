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
- Benchmark tests whether schema semantics improve LLM alignment [TODO: headline number]

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
normalization, and test five levels of schema context with open-weight and frontier LLMs over five repeats.
[TODO: main LLM result, e.g., "Full schema semantics raised top-1 mapping accuracy from X to Y; retrieval
added Z; run-to-run agreement was W".] Finally, we show that alignment errors matter downstream: a correct
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
3. An alignment benchmark with three tasks, gold labels, five levels of schema context, and a protocol that
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
concepts. Two annotators then accept or correct each draft label in the evaluation sample independently. We
report Cohen's kappa and the share of draft labels changed. [TODO: run annotation; report kappa.] The draft
rules are never shown to any baseline or model.

### 5.3 Conditions

Five levels of target context test what the schema contributes: **L0** concept ids only; **L1** ids and
preferred labels; **L2** full semantics (definition, broader concept, entity, canonical unit, synonyms);
**L3** L2 restricted to the top 10 candidates from the lexical retriever (retrieve-then-rerank). For T1, the
contrast is free-form metadata, the 2023 field list, and the Meta-Urban JSON Schema with enum definitions.
[TODO: confirm conditions with co-authors.]

### 5.4 Models, baselines and protocol

Baselines are a TF-IDF lexical matcher (word and character n-grams) and a sentence-embedding matcher.
Models: [TODO: at least two open-weight models run locally and two frontier models; record exact model ids
and dates]. Each condition is run five times at temperature 0.7 to measure self-consistency (pairwise
agreement, unanimous share, standard deviation of accuracy), and once at temperature 0 for the point
estimate. All prompts and raw responses are cached and released. We report token cost and a
coverage-accuracy curve that accepts mappings above a confidence threshold and routes the rest to a human.

### 5.5 Results

PROVISIONAL (draft labels, not to be reported): the lexical baseline reaches Acc@1 = 0.31, Acc@5 = 0.71 and
MRR = 0.48 on the 277 mappable items of the sample; the correct concept is among its top 10 candidates for
80% of items, which bounds L3. [TODO: replace with results on adjudicated gold; add Table 4 (T2 by model and
level), Table 5 (T3 field accuracy), Fig. 3 (coverage-accuracy), and an error analysis with examples.]

## 6. Do alignment errors matter downstream? (RQ4)

### 6.1 Reference pipeline

Applying the CBECS final weights (`FINALWT`) to the public microdata gives 5,918 thousand buildings, 96,527
million square feet and 6,789 trillion Btu of major-fuel consumption. These match EIA's published Tables B1
and C1 to within 0.01%, which validates the pipeline used as the reference below.

### 6.2 Ignoring the survey design

The 2023 case study processed CBECS records without weights. Doing so reports 6.4 thousand buildings instead of
5.9 million. Less obviously, it also biases intensities. Fig. 3 compares the floor-area-weighted energy use
intensity (EUI) by principal building activity with and without weights. For the 16 activities that hold at
least 0.5% of buildings, the unweighted EUI is off by -16% (food sales) to +102% (other), with 12 of 16
overestimated: retail other than mall +45%, public assembly +31%, outpatient health care +27%. Inpatient
health care holds 4.3% of records but 0.1% of buildings, so unweighted counts also distort the stock mix that
archetype-based UBEM samples from.

![Fig. 3. Error in floor-area-weighted EUI by principal building activity when CBECS 2018 survey weights are
ignored, relative to the weighted estimate. Activities with at least 0.5% of weighted buildings are shown.](figures/fig_weights_eui_error.png)

### 6.3 Sensitivity to each normalization error

Table 4 injects each T3 error type into the reference pipeline. Unit errors are the most damaging (a dropped
"thousand" multiplier or a Btu-kWh confusion changes national EUI by -99.9% or +241%), but they are also the
easiest to catch with a plausibility check. Top-codes read as values are subtler: CBECS codes buildings with
10 to 14 floors as 994 and 15 or more as 995, and treating these as numbers raises the weighted mean number of
floors by 179%. A withheld climate-zone code kept as a category shifts the hot-zone share by only 2.5%. These
sensitivities, combined with each model's T3 error rates, give the expected downstream error of each model.
[TODO: combine with T3 results.]

Table 4. Effect of single normalization errors on CBECS 2018 quantities (generated:
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
