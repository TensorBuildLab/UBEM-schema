---
title: "UBEM-Link: an AI-ready semantic schema for integrating open data in urban building energy modeling"
bibliography: references.bib
---

<!-- Drafting conventions: American spelling; "Fig. N"; "38%" without space; en dashes for ranges; no em-dashes. -->

Liang Zhang^a,b,\*^, Jianli Chen^c^, Jia Zou^d^

^a^ University of Arizona, Tucson, AZ 85721, USA

^b^ National Laboratory of the Rockies, Golden, CO 80401, USA

^c^ Tongji University, Shanghai 200092, China

^d^ Arizona State University, Tempe, AZ 85281, USA

^\*^ Corresponding author. Email: liangzhang1@arizona.edu

## Highlights {.unnumbered}

- Seven open-data categories refined into six facets and typed category profiles
- Concept definitions alone matched full concept cards for variable mapping
- Only 4 of 49 cataloged building datasets share a key with footprints or parcels
- Models read kBtu as kWh and overstated New York City energy intensity by 215%
- With conventions applied by software, a four-source city integration was exact

## Abstract {.unnumbered}

Urban building energy modeling (UBEM) combines heterogeneous open data, increasingly with help from
language models that read schemas written for people. Building on an earlier seven-category taxonomy of open UBEM
data, we present UBEM-Link: six facets and seven typed category profiles, a variable-level LinkML schema and an
81-concept vocabulary compiled into artifacts for people and AI, a catalog of 93 datasets, and an open tool that turns
a dataset and its codebook into a checked profile. In experiments with three local open-weight models (8B and 14B), concept definitions,
not labels, made mapping possible (definitions alone matched full cards), a closed vocabulary prevented invalid
answers at no cost, and documentation borrowed from Brick, BEDES and the CityGML Energy ADE did not help.
Conventions given as prose were applied beyond their scope, and with kBtu missing from the unit list, two models
overstated New York City's energy intensity by 215%. With source units in the vocabulary and conventions applied by
the tool, all three models reproduced a four-source integration of benchmarking, tax lots, building footprints and
weather for 29,077 buildings exactly; without them, feet read as metres tripled building heights. Quantities that
combine sources exposed such errors where single-source checks could not.

**Keywords:** Urban building energy modeling; Open data; Data schema; Data integration; Large language models;
Semantic interoperability

## Nomenclature {.unnumbered}

| Abbreviation or symbol | Meaning |
|---|---|
| acc@1 | Top-1 accuracy: share of variables whose first-ranked concept is the gold concept |
| ADE | Application Domain Extension (of CityGML) |
| BBL, BIN | Borough-block-lot (tax-lot) and building identification numbers of New York City |
| BEDES | Building Energy Data Exchange Specification |
| CBECS, RECS | Commercial Buildings and Residential Energy Consumption Surveys (U.S.) |
| CSVW | CSV on the Web (W3C metadata vocabulary for tabular data) |
| DCAT | Data Catalog Vocabulary |
| EPW | EnergyPlus weather file |
| EUI | Energy use intensity, site energy per floor area and year (kWh/(m²·yr)) |
| HDD | Heating degree days (base 18 °C) |
| LinkML | Linked data Modeling Language |
| LL84 | New York City Local Law 84 energy benchmarking disclosures |
| LLM | Large language model |
| LoD | Level of detail (CityGML) |
| PLUTO | Primary Land Use Tax Lot Output (New York City tax-lot data) |
| QUDT | Quantities, Units, Dimensions and Types ontology |
| SHACL | Shapes Constraint Language |
| SKOS, SSSOM | Simple Knowledge Organization System; Simple Standard for Sharing Ontological Mappings |
| TMY | Typical meteorological year |
| UBEM | Urban building energy modeling |
| L0–L3, L2D, L2N, L2S, L2U, L3E, O0, O2D, XBR, XBE, XEA | Schema conditions of the mapping experiments (Section 5.4) |
| T | Sampling temperature of the language model |

## 1. Introduction

Urban building energy modeling (UBEM) estimates how policies, technologies and climate change will affect the
energy use of a building stock, and supports city decarbonization plans, building performance standards and grid
planning [@reinhart2016urban; @ferrando2020urban; @hong2020ten]. Buildings and construction account for 32% of
global energy use and 34% of energy-related CO₂ emissions [@unep2025gsr]. A physics-based UBEM needs weather,
building geometry, building characteristics, occupant behavior and measured energy use for calibration
[@cerezodavila2016modeling; @wang2022data], and most of these inputs now have open sources. The difficulty lies in
combining them. A national survey of commercial buildings reports energy in thousand Btu, codes regions as
numbers, releases 151 replicate weights next to the data and marks imputed values in separate flag variables; a
city's footprint dataset gives roof heights in feet and an area field its publisher says must not be used; a
benchmarking disclosure lists several tax lots for one property. Cities often have enough public data for UBEM,
but the data lack common formats and keys [@chen2019development], and most UBEM studies cannot be reproduced
[@malhotra2022information].

Reviews have classified open UBEM data by modeling input or data domain [@goy2020data; @wang2022data;
@jin2023review; @bishop2024review]. An earlier taxonomy sorted open data for physics-based UBEM into seven categories (weather; building stock GIS; occupant behavior; building characteristics; macroscopic
and microscopic energy data; comprehensive data lakes) and listed, for each category, the metadata a modeler needs
[@zhang2023taxonomy]. That list was free text, and a classification does not by itself tell software how to read a
dataset. Schemas exist at other levels. Brick, Project Haystack and BuildingSync describe building equipment,
points and audits, BEDES defines terms for building energy data, and CityGML with its Energy ADE models city
objects and their energy systems [@balaji2018brick; @haystack4; @long2021buildingsync; @bedes; @agugiaro2018energy];
an exchange schema couples UBEM with urban microclimate models [@luo2025schema]. They describe buildings, not the
datasets a modeler must find, judge and join. DCAT describes catalog entries [@w3c2024dcat3], and DDI-Codebook and
CSVW describe survey variables and table columns [@ddi2025codebook; @w3c2015tabularmetadata], without UBEM
semantics.

Generative artificial intelligence (AI) is beginning to take over integration work. Large language models (LLMs)
match schemas [@narayan2022foundation; @sheetrit2024rematch; @liu2025magneto], generate building energy models
[@jiang2024eplusllm; @zhang2025agentic], extract building data into exchange schemas [@jia2026bemeval] and act as
agents that read documentation and write data pipelines [@anthropic2024mcp]. They read the same schemas and
codebooks people read, with different limitations: they cannot ask what a code means, see only what fits in their
context window, answer fluently where documentation is silent, and are only as checkable as the format their
answer is requested in. Mapping real BACnet point names to Brick classes with LLMs reached 27% to 36% accuracy
[@jain2025bacnetbrick]. Techniques that address these limitations exist separately: retrieval of documentation
[@lewis2020rag], constrained decoding to a JSON Schema [@willard2023guided; @geng2025jsonschemabench], and
documentation of datasets for machine learning [@gebru2021datasheets; @akhtar2024croissant;
@clark2024aireadiness]. No study has compiled them from one domain schema, measured which of them help a language
model integrate building energy data, or followed the remaining errors into urban energy results.

This paper asks **which properties of a UBEM data schema help small, locally run language models integrate open
building energy data, and whether the errors that remain reach national and city-scale energy indicators.** It
contributes, in the order of the paper:

1. A taxonomy and category profiles for open UBEM data that refine the earlier seven categories into six
   independent facets and seven typed category profiles, applied to a catalog of 93 open datasets (Section 2).
2. UBEM-Link, a LinkML schema with a dataset level, the category profiles, a variable level and an 81-concept
   vocabulary mapped to Brick, BEDES and the Energy ADE, compiled into artifacts for people and for AI; and a
   definition of AI-ready schemas with six design principles (Section 3).
3. `ubem-link`, an open tool that turns a dataset and its codebook into a checked UBEM-Link profile with a local
   or hosted model and joins profiled datasets, released with tutorials in a repository organized like other
   open building schemas (Section 4).
4. Controlled experiments with three open-weight models, including a factorial ablation of concept documentation
   and a documentation transplant from three standards (Sections 5 and 6).
5. End-to-end tests: AI-built profiles in a national survey pipeline, and a city-scale integration of four New
   York City sources from four data categories into the inputs of a physics-based UBEM (Section 7).

## 2. A taxonomy and category profiles for open UBEM data

### 2.1 From seven categories to six facets

The seven categories of @zhang2023taxonomy follow the inputs of a building energy model, which makes them easy to
use but mixes three kinds of distinction: what the data are used for (weather, geometry, characteristics), how
fine they are (macroscopic versus microscopic energy data) and how they are assembled (a data lake that combines
sources). UBEM-Link keeps the categories as the user-facing entry point and separates the distinctions into six
independent facets: UBEM workflow role, statistical nature, finest public spatial granularity, temporal
resolution, access and join keys (Table 1). Every dataset is then a point in a six-dimensional space, and gaps can
be counted along each facet. Two roles were added while cataloging, for datasets that fit none of the seven
categories: reference simulations (synthetic building stocks and prototype models) and context and coupling data
(land use, socio-economic data, grid emissions and tariffs).

Table 1. From the categories of the earlier taxonomy [@zhang2023taxonomy] to UBEM-Link's facets and category
profiles.

| Earlier category | UBEM-Link role | Facet values that carry the remaining distinction | Category profile |
|---|---|---|---|
| Weather information | boundary conditions | statistical nature: observed, reanalysis, typical year, projection | WeatherProfile |
| Building stock GIS | geometry and inventory | spatial granularity: building, parcel, grid cell | GeometryProfile |
| Occupant behavior | operation and use | unit of observation: person, household, building | OperationProfile |
| Building characteristics | building characteristics | statistical nature: sample survey, administrative record, standard | CharacteristicsProfile |
| Macroscopic energy data | calibration and validation | energy data scale macroscopic; granularity coarser than a building | EnergyProfile |
| Microscopic energy data | calibration and validation | energy data scale microscopic; granularity building or finer | EnergyProfile |
| Comprehensive data lake | (a collection, not a kind of data) | statistical nature: compilation; a catalog of profiles | (its datasets' profiles) |
| (added) | reference simulation | statistical nature: simulation | SimulationProfile |
| (added) | context and coupling | – | ContextProfile |

### 2.2 Category profiles

For each category, the earlier taxonomy listed the information a modeler needs in free text, such as
"Timestamp format: e.g., HH:MM:SS MM/DD/YYYY" or "AMY/TMY/Others". UBEM-Link turns each item into a typed field
with a closed list of defined values, one profile class per role (Table 2). Variable lists became links to the
concept vocabulary (`provides_concepts`), so that a catalog can be queried for every dataset that provides, say,
building heights. Fields were added where integration needs them: the timestamp convention and clock of weather
data (an EPW hour marks the end of the interval, in local standard time), the reference points and coordinate
system of building heights, the representativeness of characteristics data (a probability sample generalizes, a
mandated subset such as benchmarked buildings above a size threshold does not), and the metering level and
measurement basis of energy data. The earlier description of CityGML levels of detail was replaced by the CityGML
definitions.

Table 2. Category profiles: fields carried over from the earlier per-category metadata (now typed) and fields
added. Full definitions and allowed values: Supplement S3.

| Profile | Carried over (typed) | Added |
|---|---|---|
| Weather | year type (AMY, TMY, normals, projections); file format (EPW or other); time step; gap filling; variables | timestamp convention; clock (UTC, local standard time); grid resolution; station id scheme; scenarios |
| Geometry | dimension (2D, 2.5D, 3D); CityGML level of detail; data format | height source and reference; coordinate reference system and its unit; building id scheme; capture threshold |
| Operation | behavior types; control actions; building types; behavior factors | collection method |
| Characteristics | data form (microdata, building records, aggregate tables); characteristics; joint distributions | representativeness; coverage threshold |
| Energy | sector; carriers and metrics; time series and step; geographic keys; existing metadata standard | scale (macroscopic or microscopic); metering level; measurement basis; weather-normalized values; reporting period |
| Simulation, Context | – | engine, stock representation, weather basis; kind of context data |

Facts that apply to many columns of one dataset are stated once as conventions, each with a machine-readable
scope: a list of variable names, a pattern over names, or codes that must occur in a variable's code list (for
example Yes, No and Don't know, which identify yes/no questions). New York City's building footprint entry, for
instance, states that roof heights are in feet above ground, that zero means "not available", that seven-digit
identifiers ending in six zeros are placeholders, and that the system-generated area must not be used; we found
that area to be 1.74 times the area computed from the polygons (the Web Mercator scale factor at that latitude).
None of these facts is in the city portal's column descriptions; all are in the publisher's metadata page.

### 2.3 A catalog of 93 open datasets

To show that the taxonomy and profiles describe real data, we profiled 93 open UBEM datasets selected by four
criteria: free access, at least one UBEM role, national or wider scope (or a city dataset used in this paper's
city case: New York City's benchmarking disclosures, tax lots and building footprints), and facts verifiable from
the publisher or a peer-reviewed descriptor. Entries were drafted by an LLM agent restricted to publisher pages
and peer-reviewed descriptors and validated against the schema; a random sample of 20 was re-checked field by
field by two further agents (213 settled checks: 82% correct, 16% partly correct, 2% wrong, all corrected). The
category profiles were then drafted by agents from the verified entries, with fields the entries did not state
left empty (provenance per entry in the repository). No entry was verified by a person, so the catalog is a
purposive sample with an agent-based audit, and the statistics below describe this catalog.

Because the profiles are machine-readable, gap analysis becomes a query (Fig. 1). Geometry is well served (18 of 24
geometry datasets release individual buildings; 12 give heights or 3D shapes), and weather data are mature but heterogeneous: of
15 weather datasets, 3 are released as EPW files ready for simulation, and the timestamp convention and clock
could be established for none from the verified entries. Of 31 datasets with energy data, 23 are microscopic,
mostly anonymized collections of metered buildings or households. Building characteristics come mostly as building
records (11 of 24) or aggregate tables (6); only 3 are probability samples whose weighted estimates represent a
stock, and 4 cover mandated subsets. Linkage is the most consequential gap. Of the 49 datasets whose primary role
is characteristics, operation, calibration or reference simulation, 4 share an identifier with a footprint or
parcel dataset of the same jurisdiction (energy certificates, benchmarking disclosures and tax lots), 23 can be
linked only through an area code, 1 only by attributes, and 21 have no usable key.

![Fig. 1. Catalog datasets by primary UBEM workflow role and the finest spatial granularity they release
publicly.](figures/fig_role_by_granularity.png)

## 3. UBEM-Link

### 3.1 AI-ready schemas

We call a schema AI-ready when its machine-readable artifacts are sufficient for an AI system to (i) understand
what every element means, (ii) produce instances that conform to it, and (iii) check those instances, without a
person explaining the schema, while the same artifacts remain a faithful and reviewable encoding of domain
knowledge for people. Readiness is designed into the artifacts but can only be measured for a given model and
task. Six design principles follow from documented limitations of language models reading documentation
[@geng2025jsonschemabench; @gan2026lessismore; @parciak2024schema] and from the practice of reusing standards
(Table 3); the last column gives the verdict reached in Section 8.

Table 3. Design principles, their mechanism in UBEM-Link, the experiment that tests them, and the verdict for the
tested models and tasks.

| Principle | Mechanism | Test | Verdict |
|---|---|---|---|
| P1 Define every term | A definition for every class, field, value and concept | E1, E6, E8 | Supported: descriptions beyond a name made mapping possible for all three models; definitions alone matched full cards, and other card fields could substitute for them; models read definitions literally (E8) |
| P2 Close the vocabulary | Enumerations compiled to JSON Schema for constrained output | E2, E8, E8b | Supported as a guarantee at no accuracy cost (5 of 300 invented identifiers without it); the unit list must include the source's units (E8, E8b) |
| P3 State the conventions | Conventions at dataset level with machine-readable scope; weights and flags at variable level | E3, E7, E8, E8b | Supported when typed and applied by software: as prose, conventions were also applied beyond their scope (E7, E8, E8b); applied by the tool, they removed every indicator-changing profile error (E8b) |
| P4 Make output checkable | Types and enumerations (JSON Schema, SHACL); units and quantity kinds; profile checks | E4, E7, E8, E8b | Partly: mapping checks catch 5–16% of wrong mappings; profile checks catch most consequential errors once they know the source's conventions; cross-source quantities exposed every geometry unit error (E8b) |
| P5 Fit the context window | Self-contained cards (about 60 tokens per concept) and retrieval | E5 | Supported when retrieval recall is high: ten cards kept accuracy at a fifth of the tokens |
| P6 Ground in domain standards | SSSOM mappings to Brick, BEDES and the Energy ADE; reuse of DCAT, QUDT, SKOS | E6 | Not supported for reusing documentation: transplanted definitions were no better than identifiers; the mappings themselves were not tested |

### 3.2 Architecture

UBEM-Link is written once, in LinkML [@moxon2025linkml], and compiled for two audiences (Fig. 2). The dataset level
profiles `dcat:Dataset` [@w3c2024dcat3] with the six facets, coverage, license, access, sampling weights, scoped
conventions and the provenance of the profile; the category profiles of Section 2.2 attach to it, one per role.
The variable level profiles `csvw:Column`: each variable is linked to a concept or a join-key type and carries its
QUDT unit and multiplier, code list, missing codes, aggregation over time, whether it is a sampling weight or an
imputation flag for another variable, and, when produced by a model, its provenance, confidence and review flags
(Fig. 3). People receive YAML, generated documentation and an OWL ontology; AI systems receive a schema card,
concept cards and dataset cards for their context, JSON Schema for constrained output and SHACL shapes. JSON
Schema and SHACL check structure; checks of meaning, such as whether a unit agrees with a column's documentation,
are separate functions that use the schema's unit vocabulary of 45 QUDT units with conversion factors.

![Fig. 2. Architecture of UBEM-Link: domain knowledge, including the taxonomy of open UBEM data, is encoded once in
a LinkML source and compiled into artifacts for people and for AI systems.](figures/fig_architecture.png)

![Fig. 3. Classes, key fields and relations of UBEM-Link. Every class, field and enumeration value carries a
definition.](figures/fig_class_diagram.png)

### 3.3 Vocabulary and documentation layer

The vocabulary has 81 SKOS concepts: 8 groups and 73 mapping targets, each with a definition, the entity it
describes, a quantity kind and canonical unit where applicable, and generic synonyms. Definitions and synonyms were
drafted with AI assistance from general UBEM knowledge, with the CBECS and RECS codebooks in view; Section 6.1 tests
how much lexical overlap with survey labels matters. Sixty-three targets and two groups have 168 mappings to Brick
1.4.4, BEDES 2.5 and the CityGML Energy ADE 1.0, published as an SSSOM mapping set [@matentzoglu2022sssom]; each
linked term was checked to exist in the release files, the relation type was assigned with AI assistance, and only
4 are exact matches, because those standards describe equipment, points and objects while UBEM-Link's concepts
describe what a dataset column measures. Ten targets, among them survey and replicate weights, have no
counterpart. The documentation layer is generated by one command and cannot drift from the source: a schema card
of about 8,900 tokens, a card of about 60 tokens per concept (4,300 tokens for all), and a card per dataset with its
facets, weights and conventions (Fig. 4).

![Fig. 4. UBEM-Link applied to CBECS 2018. (a) Excerpt of the dataset card, including conventions that the
publisher states only in its user guide. (b) Three variable profiles: an energy total with its unit and
multiplier, a top-coded count, and an imputation flag linked to the variable it flags. (c) The concept cards an
AI system receives for these variables.](figures/fig_worked_example.png)

### 3.4 Audit of machine-readable releases

Table 4 compares the released term files of UBEM-Link and five standards on properties a language model needs. A
term counts as defined when it carries a natural-language definition. UBEM-Link defines all of its terms, against
74% for Brick, 55% for BEDES and 22% for the Energy ADE; it is the only one with a JSON Schema usable for
constrained output and with terms for a survey's statistical design (DDI-Codebook has such terms but no UBEM
vocabulary [@ddi2025codebook]). All its terms fit in about 8,900 tokens, against about 32,000 for Brick and
174,000 for BEDES. The audit reflects our choice of properties, on which UBEM-Link was designed to score well; it
shows what a schema built for language models must add, not the quality of standards designed for other purposes.

Table 4. Audit of the released term files (tokens: all labels and definitions, at four characters per token).

| Standard | Terms | Defined (%) | Enum values defined (%) | Statistical-design terms | Tokens (thousands) | JSON Schema | Validation artifact |
|---|---|---|---|---|---|---|---|
| UBEM-Link | 467 | 100 | 100 | 10 | 8.9 | yes | JSON Schema, SHACL |
| Brick 1.4.4 | 1,434 | 74 | – | 0 | 32.0 | no | SHACL |
| BEDES 2.5 | 6,217 | 55 | 58 | 0 | 174.1 | no | none |
| CityGML Energy ADE 1.0 | 665 | 22 | 51 | 0 | 6.4 | no | XML Schema |
| DCAT 3 | 52 | 87 | – | 0 | 1.1 | no | none in the namespace file |
| schema.org (Dataset-related) | 163 | 100 | – | 0 | 7.6 | no | none |

## 4. The ubem-link tool

The schema is released with a tool that applies it to new data. `ubem-link describe` reads a data file and any
documentation it comes with (portal data dictionaries such as Socrata metadata, Frictionless and CSVW metadata,
DDI-Codebook XML, Markdown metadata pages, and CSV or Excel codebooks including the EIA codebooks, whose header row
is detected) and writes a UBEM-Link profile of every column, a review file and a dataset card. Each step follows a
result of Sections 6 and 7:

1. Concept mapping: a dense retriever selects the ten most similar concept cards and the model chooses among them
   or among the join-key types under constrained output (E2, E5).
2. Normalization: the model chooses a unit from the full unit vocabulary, which includes the units in which sources
   publish, such as kBtu, therms and feet (E8).
3. Conventions: only conventions whose scope covers a column are shown to the model, and the tool applies their
   stated units, multipliers and missing codes, recording any disagreement (E3, E7, E8).
4. Review: profile checks and low confidence rank the columns in a review file; every profile is marked unreviewed
   until a person accepts it (E4, E8).

`ubem-link apply` then converts the data to SI units and removes missing codes without a model, and
`ubem-link integrate` joins profiled datasets through their keys (splitting multi-valued keys and ignoring
placeholder identifiers) and assigns each building its nearest weather station, as in Section 7.4. The tool runs
local models through Ollama by default; any OpenAI-compatible server, the Anthropic API, or an assistant without an
API (requests and answers are exchanged as files, for example with Claude Code) can be used instead. The
repository follows the layout of other open schemas such as Brick and BuildingSync: the schema source and its
generated artifacts, mappings, a catalog, examples that must validate, generated reference documentation, five
tutorials, tests, and instructions for AI coding agents (link withheld for anonymized review).

## 5. Evaluation design

### 5.1 Data and tasks

The experiments use the public codebooks of CBECS 2018 [@eia2018cbecs] (1,249 variables) and the 2020 Residential
Energy Consumption Survey (RECS) [@eia2020recs] (799 variables), which together contain 733 imputation flags and 213
sampling weights.

- **Variable mapping.** Given a variable (name, label, section, up to eight codes), the model chooses the most
  specific concept it measures, or `none`, with two alternatives and a confidence. The sampling frame is the
  1,104 substantive variables (imputation flags and replicate weights excluded), stratified by survey and by a
  rule-based draft concept (48 strata, including a stratum of 68 variables matching no concept); 300 variables (150
  per survey) were drawn with proportional allocation, at least one per stratum and a fixed seed.
- **Code and unit normalization.** Given the verbatim codebook entry, the model returns whether the variable is a
  weight, a replicate weight or an imputation flag, the variable it flags, its unit and multiplier, its missing
  codes and its code list. Items: the 300 variables plus 60 imputation flags and 30 replicate weights.

### 5.2 Gold labels

Normalization gold is derived from the codebooks by a unit-tested parser written for these two surveys; it solves
normalization for them by construction but does not transfer, so Section 7 tests normalization on city data without
one. Mapping gold was produced in three blind steps: two annotators labeled all 300 variables independently,
seeing the variable and the full concept cards but no draft labels or model output, and recorded alternatives; a
separate adjudicator resolved disagreements. No qualified domain expert was available, so the annotators and the
adjudicator were LLM agents in fresh contexts (Claude Opus 5.5 and Claude Sonnet 5.5 as annotators, Claude Opus 5.5
as adjudicator), from a developer other than those of the evaluated models. Agreement was high (κ = 0.91), but
agreement between related models is not evidence of correctness [@ziems2024css], and because the annotators read
UBEM-Link's definitions, conditions that show a model the same definitions may be favored. Every comparison is
therefore re-scored against three further label sets, including deterministic keyword rules fixed before any model
ran (Section 6.7). The adjudicated gold uses 44 concepts; 5 variables have no applicable concept and 80 have an
accepted alternative.

### 5.3 Models and protocol

We evaluate three open-weight models run locally through Ollama 0.40.16 on one 8 GB laptop GPU (Q4_K_M
quantization, thinking disabled, 8,192-token context, output constrained by JSON Schema): Qwen3 8B [@yang2025qwen3]
and Llama 3.1 8B [@grattafiori2024llama3] in all experiments, and Qwen3 14B, from the same family as Qwen3 8B and
run with partial CPU offload, in the core mapping conditions and the four-source integration (E8b) to separate the effect of model size from that of the
schema. Small local models are what a city or utility can run on its own hardware at no per-call cost. Each
condition is run at T = 0; the base mapping conditions were repeated four times and normalization twice at T = 0.7
to measure run-to-run variation. Every prompt and raw response is cached and released.

### 5.4 Experiments and statistics

Each experiment changes one property of the schema and holds the rest fixed (Table 3).

- **E1 Definitions (P1).** A factorial on what the concept list contains: opaque codes (O0), identifiers (L0),
  identifiers and labels (L1), opaque codes with definitions (O2D), identifiers, labels and definitions (L2D),
  full cards without definitions (L2N) and full cards (L2); full cards in shuffled order (L2S) test order.
- **E2 Closed vocabulary (P2).** Full cards with output constrained to the concept enumeration (L2) or free (L2U).
- **E3 Conventions (P3).** Normalization with the codebook entry only, or with the dataset card.
- **E4 Checks on mappings (P4).** A variable with a unit mapped to a concept of another dimension or to a
  categorical concept, or a categorical variable mapped to a unit-bearing concept, is flagged.
- **E5 Context budget (P5).** Ten retrieved cards from a lexical (L3) or dense embedding retriever (L3E,
  nomic-embed-text) against all cards (L2).
- **E6 Standards' documentation (P6).** The same concept identifiers documented with the label and definition of
  the matching Brick, BEDES or Energy ADE term, compared with L0 and L2.
- **E7 and E8** feed AI-built inputs into a national survey pipeline and a city-scale integration (Section 7).

Baselines rank concept cards by TF-IDF over word and character n-grams and by dense embeddings. Paired conditions
are compared with exact McNemar tests, Holm-adjusted over all comparisons and models; 95% intervals resample whole
concepts (cluster bootstrap), because variables of one concept are correlated.

### 5.5 Use of AI in this study

AI was used in the research in six places: drafting and auditing catalog entries and drafting their category
profiles (Claude Opus 5.5 and Sonnet 5.5 agents; Section 2.3); drafting concept definitions and synonyms and
assigning mapping relations (Section 3.3); producing and adjudicating the mapping gold (Section 5.2); verifying
references; and writing the analysis code and the tool. The evaluated models are the object of study. No step was
repeated by an independent domain expert; Section 8.3 discusses this limitation.

## 6. Results

### 6.1 E1: concept documentation

Concept documentation decided whether the models could map at all (Table 5, Fig. 5a). With opaque codes and
nothing else, both 8B models scored near zero (0.01 and 0.02), so neither had a hidden key to the concepts.
Meaningful identifiers alone gave 0.42 and 0.43, and labels did not change this significantly (Qwen3 +0.05,
p_Holm = 0.10; Llama 3.1 −0.03, p_Holm = 1.00). Adding definitions to labels raised accuracy by 0.08 for Qwen3
(p_Holm = 0.028) and 0.13 for Llama 3.1 (p_Holm < 0.001), although the concept-clustered intervals of both
differences reach just below zero. Definitions were sufficient: with opaque codes and definitions (O2D), Qwen3
reached 0.62, its highest accuracy, and Llama 3.1 0.55, equal to its full cards. They were not necessary: cards
without definitions (L2N) improved on labels by a similar amount (+0.08 and +0.18; p_Holm = 0.015 and < 0.001),
and adding definitions to them changed nothing significant. Descriptive content beyond a label therefore helps,
and the definition and the other card fields largely substitute for each other. On the 224 variables whose label
contains neither the gold concept's label nor a synonym, the ordering is the same (labels, definitions with opaque
codes, full cards: Qwen3 0.41, 0.59, 0.52; Llama 3.1 0.29, 0.50, 0.48; S9). Shuffling the cards left accuracy
unchanged in aggregate (p_Holm = 1.00) but changed correctness for 20% and 28% of variables, so single answers
depend on prompt order. Ranking cards by TF-IDF or embedding similarity, without a language model, reached 0.27 and
0.29. Qwen3 14B, run on the core conditions, showed the same pattern (Table 5, S23): definitions raised accuracy over labels by 0.10 (p_Holm < 0.001) and full cards did not improve on definitions (−0.03, p_Holm = 0.35). It beat Qwen3 8B with identifiers alone (+0.10, p_Holm = 0.011) but not significantly with definitions or cards (+0.06 and 0.00). It answered "none" for 59–88 of the 295 mappable variables (Qwen3 8B: 5–20), often listing the right concept as an alternative; when it chose a concept, it was right 72–80% of the time, against 43–60% for Qwen3 8B. The larger model traded coverage for precision; it did not make definitions unnecessary.

Table 5. Variable mapping by schema condition (top-1 accuracy on 295 mappable variables, T = 0; intervals
resample concepts; tokens are mean input tokens per call as counted by Qwen3; Qwen3 14B was run on the core
conditions only).

| Condition | Concept list shown to the model | Qwen3 8B | Llama 3.1 8B | Qwen3 14B | Tokens |
|---|---|---|---|---|---|
| O0 | Opaque codes | 0.01 [0.00, 0.03] | 0.02 [0.00, 0.04] | – | 545 |
| L0 | Identifiers | 0.42 [0.29, 0.59] | 0.43 [0.28, 0.61] | 0.52 [0.41, 0.63] | 486 |
| L1 | Identifiers and labels | 0.47 [0.31, 0.65] | 0.40 [0.27, 0.59] | 0.52 [0.43, 0.63] | 809 |
| O2D | Opaque codes and definitions | 0.62 [0.52, 0.73] | 0.55 [0.42, 0.68] | – | 1,559 |
| L2D | Identifiers, labels and definitions | 0.55 [0.39, 0.72] | 0.53 [0.38, 0.69] | 0.61 [0.51, 0.73] | 1,823 |
| L2N | Full cards without definitions | 0.55 [0.41, 0.73] | 0.58 [0.47, 0.70] | – | 2,871 |
| L2 | Full concept cards | 0.59 [0.44, 0.74] | 0.55 [0.42, 0.69] | 0.58 [0.48, 0.71] | 3,884 |
| L2S | Full cards, shuffled order | 0.55 [0.42, 0.70] | 0.55 [0.44, 0.68] | – | 3,884 |
| L2U | Full cards, open output | 0.59 [0.44, 0.74] | 0.53 [0.42, 0.67] | – | 3,884 |
| L3 | Ten cards, lexical retrieval | 0.51 [0.42, 0.63] | 0.52 [0.42, 0.65] | – | 710 |
| L3E | Ten cards, dense retrieval | 0.56 [0.45, 0.69] | 0.58 [0.50, 0.69] | 0.53 [0.45, 0.63] | 726 |
| XBR | Brick documentation | 0.42 [0.27, 0.61] | 0.35 [0.22, 0.53] | – | 1,123 |
| XBE | BEDES documentation | 0.47 [0.32, 0.63] | 0.43 [0.30, 0.60] | – | 1,976 |
| XEA | Energy ADE documentation | 0.46 [0.34, 0.63] | 0.42 [0.29, 0.60] | – | 762 |
| Baselines | TF-IDF ranking 0.27; embedding ranking 0.29 | | | | |

![Fig. 5. Top-1 mapping accuracy by schema condition, with 95% intervals that resample concepts. (a) What the
concept documentation contains. (b) Full cards in shuffled order, with open output, and with ten retrieved
cards.](figures/fig_design_conditions.png)

### 6.2 E2: closed vocabulary

With the full vocabulary in context, open output did not change accuracy (Qwen3 0.59 against 0.59, p_Holm = 1.00;
Llama 3.1 0.53 against 0.55, p_Holm = 1.00) but produced 5 of 300 identifiers per model that do not exist in the
schema, such as `garage_size` and `outage`. A constrained decoder excludes such answers by construction, as would
validating the output against the enumeration afterwards; the guarantee costs no accuracy.

### 6.3 E3: stated conventions

Without the dataset card, both models detected what a codebook entry announces: the 2 final weights, the 30
replicate weights and the 60 imputation flags were all recognized, with 1 false weight among the 358 other
variables and no false imputation flag (Table 6), and units were right for 97–98% of the 65 variables that have
one. Their errors concern what the entry does not state. CBECS gives an imputation flag the same label as the
variable it flags, and the link (ZMONUSE flags MONUSE) is a naming convention stated only in the user guide.
Without the card, neither model identified the flagged variable for any of the 30 CBECS flags; with it, both
identified all 30 (p < 0.001 for each model). With the card, Qwen3's exact missing-code accuracy rose from 0.32 to
0.50 (CBECS 0.25 to 0.52; p < 0.001). The card also introduced errors: Qwen3 no longer recognized 3 of the 30 RECS
replicate weights, and Llama 3.1 did not apply the missing-code conventions (0.26 with and without the card,
p = 1.00). Sections 7.2 and 7.3 show further card-induced errors.

Table 6. Code and unit normalization with and without the dataset card (T = 0). Detection rows give recall on the
positives and the number of false alarms among the other items (390 items in total).

| Field (number of positives) | Qwen3, entry only | Qwen3, with card | Llama 3.1, entry only | Llama 3.1, with card |
|---|---|---|---|---|
| Final weight (2): recall / false alarms (of 358) | 1.00 / 1 | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 |
| Replicate weight (30): recall | 1.00 | 0.90 | 1.00 | 1.00 |
| Imputation flag (60): recall / false alarms (of 330) | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 |
| Flagged variable, CBECS (30) / RECS (30) | 0.00 / 1.00 | 1.00 / 1.00 | 0.00 / 1.00 | 1.00 / 1.00 |
| Unit (65) / multiplier (31 scaled units) | 0.97 / 0.94 | 0.97 / 1.00 | 0.98 / 0.97 | 0.98 / 0.97 |
| Missing codes, exact (390; CBECS / RECS) | 0.32 (0.25 / 0.38) | 0.50 (0.52 / 0.48) | 0.26 (0.24 / 0.27) | 0.26 (0.28 / 0.24) |
| Code list, Jaccard | 0.74 | 0.79 | 0.71 | 0.73 |

### 6.4 E4 and E5: checks on mappings and retrieval

With full concept cards, the quantity-kind checks flagged 20 of Qwen3's 122 wrong mappings (16%) and 7 of Llama
3.1's 134 (5%), and 4 correct mappings of each model (2%), so 83% and 64% of the flags marked real errors (S11).
They catch one recurring confusion, a variable recording whether a fuel is used mapped to a consumption quantity;
most wrong mappings stay within one quantity kind, so these checks are an inexpensive filter, not a test of
correctness. Ten retrieved cards instead of all 73 cut the prompt from about 3,880 to 720 tokens. Accuracy changed
by −0.08 (Qwen3; p_Holm = 0.36) and −0.02 with lexical retrieval (L3), and by −0.02 and +0.04 with dense retrieval
(L3E; p_Holm = 1.00). The retriever bounds the result: the gold concept was among the ten candidates for 76%
(lexical) and 82% (dense) of variables, and then accuracy was 0.68–0.69, against 0.63–0.66 with all cards.

### 6.5 E6: documentation from existing standards

Documenting UBEM-Link's concepts with the matching terms of Brick, BEDES or the Energy ADE (a documentation
transplant; 34, 57 and 35 of the 73 concepts covered) gave accuracies of 0.35–0.48: for neither model better than
identifiers alone (largest gain: BEDES for Qwen3, +0.06, p_Holm = 0.21), worse for Llama 3.1 with Brick (−0.08,
p_Holm = 0.009), and 0.11–0.20 below UBEM-Link's cards (p_Holm ≤ 0.002; Fig. 6a). Coverage explains part of this,
since uncovered concepts appear as identifiers only. On the variables whose gold concept a standard documents
(Fig. 6b), BEDES terms (54 of 57 defined) improved on identifiers by 0.02 and 0.06 but stayed 0.12–0.13 below
UBEM-Link's cards (p < 0.001), also for exact and close matches only (S10); Energy ADE terms (10 of 35 defined) did
no better than identifiers; and on the Brick subset the three conditions did not differ significantly. The
transplant cannot separate the purpose of a definition from its wording and length.

![Fig. 6. Mapping accuracy when the same concepts are documented by UBEM-Link or by the matching terms of existing
standards. (a) All 295 mappable variables; in parentheses, the share of concepts each standard documents. (b)
Only the variables whose gold concept the standard documents, with the number of matched terms that carry a
definition. Bars show the mean of the two models, markers each model.](figures/fig_standards.png)

### 6.6 Consistency, confidence and label sensitivity

At T = 0.7, accuracy varied little across four runs (standard deviation 0.002–0.014; S8), but Llama 3.1's answers
did: two of its runs agreed on 70–96% of variables, against 96–100% for Qwen3. Confidence was weakly informative
(Fig. 7): accepting Qwen3's answers with confidence of at least 0.9 kept 67% of variables at 0.77 accuracy, whereas
Llama 3.1 gave such confidence for 17% and was no more accurate there. Where both models agreed under both full and
retrieved cards (36% of variables), 83% of answers were correct. Re-scored against each annotator alone and against
the keyword rules (S7), no significant difference changed direction, and the gain of definitions over labels
remained significant under all four label sets (p_Holm ≤ 0.035).

![Fig. 7. Coverage and accuracy when only some mappings are accepted automatically (full concept cards). Lines:
threshold on the model's own confidence; markers: unanimous runs at T = 0.7, agreement between L2 and L3, and
agreement of both models under both.](figures/fig_t2_coverage.png)

## 7. From AI-built inputs to energy indicators

### 7.1 National survey pipeline and its uncertainty

A reference pipeline built on the schema reproduces EIA's public-use-microdata versions of Tables B1 and C1 for
CBECS 2018 within 0.01% (5,918 thousand buildings, 96,527 million ft², 6,789 trillion Btu of major fuel use); EIA's
main tables, built from the confidential full file, differ by up to 0.11%. Design-based relative standard errors
from the replicate weights [@eia2023cbecsmicrodata; @eia2023recsmicrodata] are 1.8–3.9% for the CBECS indicators
and 0.4–0.9% for the RECS ones, except for the share of buildings in hot or very hot climate zones (18%; S15).
Injecting single errors shows their size (S18): ignoring the survey weights reports 6.4 thousand buildings
instead of 5.9 million and biases floor-area-weighted energy use intensity (EUI) by −16% to +102% across 16 building
activities (Fig. 8), a dropped multiplier divides EUI by 1,000, and reading the floor top-codes 994 (10 to 14
floors) and 995 (15 or more) as numbers overstates the mean number of floors by 175–179% (S17).

![Fig. 8. Error in floor-area-weighted energy use intensity by principal building activity if the CBECS 2018 survey
weights are ignored (the 16 activities that each account for at least 0.5% of
buildings).](figures/fig_weights_eui_error.png)

### 7.2 AI-built profiles in the national pipeline (E7)

The pipeline, extended to RECS 2020, reads only the profiles of the 11 variables it needs (weight, unit,
multiplier, missing codes); replacing the gold profiles by each model's makes every change in the results an effect
of the AI-built profiles. At T = 0 most indicators were reproduced exactly (Table 7). Without the card, Qwen3 gave
CBECS electricity a multiplier of one million instead of one thousand, which multiplied commercial electricity
intensity by 1,000; Llama 3.1 declared zero a missing code for residential natural gas, which dropped the
households that use none and raised gas use per household by 65%, and wrote the withheld climate-zone code as
"7=Withheld for confidentiality" (−2.5% in the hot-zone share, within its 18% standard error). With the card, no
Qwen3 profile changed an indicator. Llama 3.1 fixed both of its errors but applied the CBECS rule "code 5 means
Don't know", which the card states for yes/no questions, to the climate-zone variable, where code 5 means hot or
very hot; no building remained in a hot zone. At T = 0.7, Llama 3.1's residential site energy was off by +241% in
one run and by a factor of 3,412 in the other (S16).

Of the 88 AI-built profiles (two models; entry only and with the card at T = 0; two runs at T = 0.7 without the
card; 11 variables), 51 deviated from the gold profile and 11 changed an indicator (S13). Profile checks written
after inspecting these outputs (version 1) flagged all 11, 28 of the 40 harmless deviations and none of the 37
exact profiles (S12). Applied unchanged to the 766 other benchmark profiles per model and temperature, they flagged
15–80% of unit or multiplier errors and 14–28% of correct profiles (S14). Version 2 corrects the causes; in-sample,
it flags 25–89% of those errors without false alarms, and 10 of the 11 indicator-changing national profiles.

Table 7. National indicators from gold and from AI-built variable profiles (relative error, T = 0; 0 means within
0.01%). Reference values with design-based standard errors from the surveys' replicate weights.

| Survey | Indicator | Reference ± standard error | Qwen3, entry only | Qwen3, with card | Llama 3.1, entry only | Llama 3.1, with card |
|---|---|---|---|---|---|---|
| CBECS 2018 | Buildings (thousand) | 5,918 ± 233 | 0 | 0 | 0 | 0 |
| | Floor area (million m²) | 8,968 ± 273 | 0 | 0 | 0 | 0 |
| | Site EUI, major fuels (kWh/(m²·yr)) | 221.9 ± 4.0 | 0 | 0 | 0 | 0 |
| | Electricity intensity (kWh/(m²·yr)) | 133.4 ± 2.8 | ×1,000 | 0 | 0 | 0 |
| | Natural gas intensity (kWh/(m²·yr)) | 75.2 ± 2.2 | 0 | 0 | 0 | 0 |
| | Share in hot or very hot zones (%) | 13.8 ± 2.5 | 0 | 0 | −2.5% | −100% |
| RECS 2020 | Households (million) | 123.5^a^ | 0 | 0 | 0 | 0 |
| | Site energy per household (MWh) | 22.49 ± 0.09 | 0 | 0 | 0 | 0 |
| | Electricity per household (MWh) | 10.57 ± 0.04 | 0 | 0 | 0 | 0 |
| | Natural gas per household (MWh) | 10.06 ± 0.09 | 0 | 0 | +65% | 0 |
| | Site EUI (kWh/(m²·yr)) | 133.1 ± 0.6 | 0 | 0 | 0 | 0 |

^a^ The RECS weights are calibrated to the household total, so its replicate standard error is zero.

### 7.3 City-scale benchmarking in New York City (E8)

New York City's 2023 benchmarking disclosures (LL84) [@nycdob2023ll84] list 33,684 properties in 265 columns, and
PLUTO [@nycdcp2026pluto] lists 858,284 tax lots with their community district. Neither was consulted when the
vocabulary was written. A reference pipeline joins the first tax lot of each property's BBL to PLUTO, converts
floor area and energy to SI units, discards records with a site EUI outside 5–3,000 kWh/(m²·yr) and reports
floor-area-weighted EUI by district: 30,046 properties (89%) link to 66 districts, city-wide site EUI is 259
kWh/(m²·yr), and the 60 districts with at least 20 properties range from 168 to 402 (Fig. 9a).

The models performed both integration steps. For each quantity the pipeline needs (tax-lot key, floor area, site
energy, electricity, natural gas) they chose one of the 265 columns, given the schema element as an identifier (L0)
or with its definition (L2) and the purpose; they then built each chosen column's profile from its name,
description and a summary of its values, without and with the LL84 dataset card. The tax-lot key is described by
UBEM-Link's join-key type `parcel_id`. In a first run we described it by the concept `record_identifier`, defined as
an identifier "within the dataset"; both models then chose the internal Property ID and nothing could be joined.
The models followed the definition; the specification error was ours (S21).

Definitions improved column choice (Table 8): from two to five acceptable columns for Qwen3 and from one to three
for Llama 3.1. With identifiers only, Qwen3 took the building identification number for the tax-lot key, Llama 3.1
took the floor area of the largest use and the site EUI for site energy, and both took weather-normalized values for
electricity and gas, as Llama 3.1 did even with definitions. Both models chose the floor area that includes
parking. With gold profiles, this plausible choice lowers city-wide EUI by 2.0% and district EUI by 0.3–21% (median
1.7%), by each district's share of parking (Fig. 9b): small city-wide, large locally.

Normalization failed on the unit that matters most. Both models wrote kBtu as kilowatt-hours: without the card with
multiplier 1, overstating city-wide site EUI by 215%, and with the card, which states that kBtu means thousand Btu,
with multiplier 1,000, a 3,412-fold overstatement after which the plausibility filter kept 43 properties. Post hoc,
we added kBtu and therms to the closed unit vocabulary: without the card, both models then reproduced the reference
exactly, so the error came from having to express kBtu as Btu times a multiplier; with the card, they applied the
multiplier on top of kBtu (+417%), again applying a convention where it did not belong. Of the 27 distinct profiles
of these runs, 17 had a wrong unit or would drop valid values (S20). Version 1 of the checks flagged all 17 and 9 of
the 10 others (precision 65%); version 2 flagged 13 of the 17 and 2 of the 10 others (precision 87%), but three of
its terms ("Not Available", kBtu, ft²) were written with the LL84 entry, and without them it behaves like version 1.
Its precision thus came from knowing the source's missing-value label, which the dataset card states. These lessons,
source units in the vocabulary and conventions with a machine-readable scope applied by software, were built into
the tool before the test of Section 7.4.

Table 8. City-scale benchmarking: LL84 with PLUTO tax lots (T = 0). Errors are relative to the reference pipeline
(30,046 linked properties, 259 kWh/(m²·yr)).

| Columns chosen by | Profiles built by | Acceptable columns (of 5) | Linked properties, entry only / with card | City site EUI error, entry only / with card |
|---|---|---|---|---|
| Qwen3, identifiers | Qwen3 | 2 | 1 / 0 | – / – |
| Qwen3, definitions | Qwen3 | 5 | 29,794 / 43 | +210% / +553% |
| Llama 3.1, identifiers | Llama 3.1 | 1 | 67 / 67 | −81% / −81% |
| Llama 3.1, definitions | Llama 3.1 | 3 | 29,794 / 43 | +210% / +553% |
| Reference | Each model (same result) | 5 | 29,778 / 43 | +215% / +554% |
| Reference | Each model, kBtu and therms offered (post hoc) | 5 | 30,046 / 105 | 0 / +417% |
| Either model, definitions | Gold | 3–5 | 30,044 | −2.0% |

![Fig. 9. New York City, calendar year 2023. (a) Reference site EUI of benchmarked properties by community district
(districts with at least 20 properties). (b) Error of district EUI when floor area is taken from the column both
models chose with definitions (including parking), with gold profiles.](figures/fig_city_map.png)

### 7.4 Four-source integration with the tool (E8b)

Section 7.3 joined two sources, and PLUTO contributed only a district. A physics-based UBEM needs inputs from four
data categories, so the second city test integrates one source from each: LL84 (microscopic energy for calibration),
PLUTO (characteristics: construction year, floors, coordinates), the city's building footprints (geometry: polygons
and roof heights) [@nycoti2026footprints] and TMYx weather files of four stations (weather) [@climateonebuilding].
A reference pipeline joins the properties' tax lots by BBL and all their buildings by BIN (11% of properties list
several BINs), assigns each property the nearest station, and computes footprint areas from the polygons: 29,077 of
the 33,684 properties (86%) receive complete inputs (floor area, footprint, roof height, floors, construction year,
weather file and measured energy). Two cross-source quantities confirm the join and the units: median roof height
per floor is 3.5 m, and LL84 floor area divided by footprint area times floors has a median of 1.04.

The tool, frozen before any model saw PLUTO or the footprints, performed the integration steps: column selection with
definitions (16 inputs), then profiles under four contexts: the portal's column description and a summary of values
only (entry); all dataset conventions as prose (card); only the conventions whose scope covers the column (scoped);
and scoped, with the tool applying the conventions' stated values (tool, its default). Qwen3 chose 15 of the 16
columns; for footprint area it chose the system-generated area, which the footprint entry marks as not to be used
because it is computed in Web Mercator (1.74 times the true area). Used as square metres, it would have overstated
building volume by 75%; the tool refused it and flagged it for review. Llama 3.1 chose 13: weather-normalized
electricity and gas, as in Section 7.3, and the tax-lot number instead of the building number as the footprint key,
so no footprint could be joined. Qwen3 14B, run afterwards with the same frozen prompts, chose all 16 columns
correctly.

Context decided the profiles (Table 9). Without the conventions, both 8B models gave roof heights no unit; read as
metres, feet overstated height per floor and building volume by 228%, and Llama 3.1 also read gas in kBtu as kWh
(+241% in gas use per degree day). With all conventions as prose, Qwen3's profiles were right, but Llama 3.1 gave
floor area no unit, so square feet became square metres and the floor-area ratio rose from 1.04 to 11.2. With only
the matching conventions, both 8B models again applied "multiplier 1,000 on Btu" to kBtu, and the plausibility filter
left 94 and 647 properties. Qwen3 14B also read feet as metres without the conventions, but with them, as prose or
scoped, its remaining errors changed no indicator. With the tool, every indicator was reproduced exactly for all three models: the tool overwrote
the units and missing codes that the conventions state, and 1 of 14 profiles per model remained wrong
(placeholder building numbers in LL84, which no LL84 documentation declares and which matched nothing, because the
footprint side's placeholders were removed). On the models' own answers, the fixed review checks flagged all
errors that changed an indicator and no exact profile; the checks as frozen also matched unit words inside other
words ("wh" in "which") and flagged 9 of the 12 exact profiles (S22). The cross-source quantities exposed every
unit error that changed the geometry: a height per floor of 11.6 m or a floor-area ratio of 11 cannot be right,
although heights with a median of 68 "metres" or floor areas in the wrong unit pass any single-source range check.

Table 9. Four-source integration (LL84, PLUTO, footprints, weather) with the reference columns and AI-built profiles
(T = 0). Profile errors: of the 14 profiles the pipeline uses, in the model's answer and, for the tool, after it
applied the conventions.

| Model | Context | Profile errors | Properties with complete inputs | Height per floor (m) | Floor-area ratio | EUI before 1940 | Gas per m² and degree day |
|---|---|---|---|---|---|---|---|
| Reference | – | – | 29,077 | 3.5 | 1.04 | 244 kWh/(m²·yr) | 0.062 kWh/(m²·K·d) |
| Qwen3 8B | entry | 3 | 29,077 | 11.6 | 1.04 | 0 | 0 |
| | card | 2 | 29,077 | 3.5 | 1.04 | 0 | 0 |
| | scoped | 4 | 94 | 4.0 | 1.03 | +553% | +868% |
| | tool | 4 → 1 | 29,077 | 3.5 | 1.04 | 0 | 0 |
| Llama 3.1 8B | entry | 5 | 29,132 | 11.6 | 1.04 | +1.6% | +241% |
| | card | 7 | 28,951 | 11.6 | 11.2 | −67% | −68% |
| | scoped | 6 | 647 | 12.9 | 11.2 | +389% | +288% |
| | tool | 6 → 1 | 29,077 | 3.5 | 1.04 | 0 | 0 |
| Qwen3 14B | entry | 2 | 29,118 | 11.6 | 1.04 | 0 | 0 |
| | card | 2 | 29,077 | 3.5 | 1.04 | 0 | 0 |
| | scoped | 1 | 29,077 | 3.5 | 1.04 | 0 | 0 |
| | tool | 1 → 1 | 29,077 | 3.5 | 1.04 | 0 | 0 |

## 8. Discussion

### 8.1 What makes a schema AI-ready for these models

Table 3 gives a verdict for each principle; four results bear on schema design. First, a model maps by meaning only
when the schema describes its terms beyond a name: opaque codes defeated both 8B models, labels added nothing
significant, and definitions or the other descriptive fields of a card raised accuracy by 0.08–0.18. Because
definitions alone matched full cards and the gains held on variables without lexical overlap, the effect is not
only shared wording. Qwen3 14B kept the pattern and was most accurate with definitions alone, so within the tested range the effect does not depend on model size; the larger model was more cautious rather than better informed, and its abstentions go to the tool's review queue. The models also follow definitions literally: an identifier "within the dataset" led
them to an internal identifier, a join key defined as a shared parcel identifier to the tax-lot key. Definitions
should be written for the integration task, and linking keys should be defined elements of a schema.

Second, conventions help where they state what an entry does not (all 30 CBECS flags linked) but, given as prose,
were applied beyond their scope: a missing-code rule for yes/no questions applied to a climate zone, a multiplier
applied on top of a unit that already contains it. Machine-readable scopes alone did not solve this: shown only the conventions that concern a column, both 8B models still applied "multiplier 1,000 on Btu" to kBtu (Section 7.4); Qwen3 14B did not, so a larger model may need the tool less, but the tool makes the result independent of the model. What worked was to let the schema carry the value and software apply it: with the tool, both models' profiles reproduced every indicator of the four-source integration. A convention should therefore be a typed statement (this unit, these missing codes, for these variables), not only a sentence for a model to read. Third, a closed vocabulary guarantees valid output
at no accuracy cost, but its content steers the answer: lacking kBtu, both models chose kilowatt-hours. Unit
vocabularies should include the units in which sources publish and leave conversion to QUDT factors downstream.
Fourth, profile checks must be validated on data they were not written on: version 1 was perfect on its own errors
and raised false alarms on most held-out profiles, and on the city data generic rules were precise only when they
knew the source's missing-value label. Two kinds of check complement each other: rules on single profiles, which became precise once they read conventions from the profile, and quantities that combine sources, such as height per floor or floor area against footprint area times floors, which exposed unit errors that no single dataset reveals. The checks frozen for the four-source test still contained a word-matching bug that only the held-out test revealed; checks are code, and need tests on data they were not written on.

Documentation borrowed from Brick, BEDES and the Energy ADE did not help, which says less about those standards than
about purpose: they describe equipment, points and objects, whereas integration needs definitions of what a column
measures. Their value for UBEM-Link lies in the mappings into their ecosystems, now published as SSSOM, which were
not tested here.

### 8.2 Implications for urban data integration

The taxonomy and category profiles turn the question "can these data be combined?" into queries. Only 4 of 49
non-geometric building datasets in the catalog share an identifier with footprints or parcels, so most integration
of characteristics, operation and energy data with geometry has to go through area codes or statistical matching.
The facts that decide whether an integration is right are often outside the data and its column descriptions: in
New York City, the units of roof heights, the placeholder identifiers and the warning against the system-generated
area are stated only in the publisher's metadata page. Recording such facts once, in a category profile and in
scoped conventions, lets every later user and every model apply them. Once these facts were in the entries, a small local model with the tool reproduced an integration of benchmarking, tax lots, footprints and weather for 29,077 buildings exactly when given the right columns; the remaining failures were in column choice, where they were either visible (a footprint key that joined nothing) or refused by the tool (an area field the publisher marks as unusable). Identifier systems such
as UBID [@wang2019ubid] and GERS [@overture2025gers] and exchange schemas between urban models [@luo2025schema]
address linkage; UBEM-Link complements them by describing in one machine-readable profile what a dataset contains,
how it is coded and through which keys it links, so that integrations such as that of @rehmann2025enhancing can be
repeated by a person or a model.

### 8.3 Limitations

The mapping gold was produced by LLM annotators who read the concept definitions that some conditions show the
models; four label sets, including keyword rules that do not use the definitions, agree, but expert annotation
remains the stronger test. Three open-weight models of 8B and 14B parameters were tested, the largest only on the core conditions and the city integration; larger or proprietary models may behave differently. The survey normalization gold comes from a parser that solves the task by
construction; the city cases avoid this but cover one city and one year, and several design decisions were taken
after seeing results (the description of the tax-lot key and the unit variant in Section 7.3; the tool's design in
Section 7.4 follows from them and was frozen before its test). The catalog, its category profiles, the concept
definitions and the mappings to other standards were produced with AI assistance and not reviewed by an independent
expert; most category profiles were drafted from the catalog entries rather than from publisher pages. The
integrated New York City table holds the inputs of a physics-based UBEM, but no building was simulated.

## 9. Conclusions

This paper built on an earlier seven-category taxonomy of open UBEM data to define UBEM-Link: six facets, seven
typed category profiles, a variable-level schema and a concept vocabulary compiled for people and AI systems,
applied to 93 datasets and released with a tool and tutorials. Experiments with local open-weight models showed
that descriptions of each term beyond its name made concept mapping possible, a closed vocabulary made output valid
at no cost, retrieval kept accuracy at a fifth of the context, and documentation borrowed from other standards did
not help. Qwen3 14B showed the same pattern, trading coverage for precision. Conventions supplied what codebook entries leave out but, given as prose, were applied beyond
their scope, and a unit missing from the vocabulary made both models overstate New York City's energy intensity by
215%. Built into the tool, these lessons held on new data: with the source's units in the vocabulary and
conventions applied by software, all three models reproduced a four-source integration of benchmarking, tax lots,
footprints and weather for 29,077 buildings exactly, and quantities combining sources exposed the geometry errors
that remained without them. AI-assisted integration of urban building data is feasible with small local models
when the schema defines its terms and keys for the task, records publishers' conventions as typed statements that
software applies, and offers the source's own units, and when a person reviews column choices and flagged profiles.
Expert-labeled benchmarks, more cities, and simulation on the integrated inputs are the next steps.

## Acknowledgement

This material is based upon work supported by the U.S. National Science Foundation under Grant No. 2623038.
Any opinions, findings, and conclusions or recommendations expressed in this material are those of the
author(s) and do not necessarily reflect the views of the National Science Foundation.

## Data availability

All code, the schema and its generated artifacts (including the AI documentation layer), the catalog and its
verification record, gold labels with annotations and rationales, prompts, cached model outputs, and the
scripts that produce every table and figure are openly available at
https://github.com/TensorBuildLab/UBEM-schema [@zhang2026ubemlinkrepo] (code under the MIT License; schema,
catalog and benchmark under CC BY 4.0). The CBECS 2018, RECS 2020, LL84, PLUTO, building footprint and weather source data are public
[@eia2018cbecs; @eia2020recs; @nycdob2023ll84; @nycdcp2026pluto; @nycoti2026footprints; @climateonebuilding] and are downloaded by scripts that record
SHA-256 checksums.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

Large language models are the object of study in Sections 5 to 7, and their use in the research is described
in Section 5.5. In addition, during the preparation of this work the authors used Claude (Anthropic) to draft
and edit text. After using this tool, the authors reviewed and edited the content as needed and take full
responsibility for the content of the published article.

## References
