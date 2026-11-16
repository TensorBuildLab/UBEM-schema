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

- An AI-ready schema for open urban building energy data, tested with local models
- Concept definitions alone matched full concept cards for variable mapping
- Only 3 of 48 cataloged building datasets share a key with footprints or parcels
- In New York City, models read kBtu as kWh and overstated energy intensity by 215%
- Dataset conventions were also applied where they did not belong

## Abstract {.unnumbered}

Urban building energy modeling (UBEM) integrates heterogeneous open data, a task increasingly
delegated to language models that read data schemas written for people. We define AI-ready schemas, state six
design principles with measurable criteria, implement them in UBEM-Link, a LinkML schema for open UBEM data
applied to a catalog of 91 datasets, and test them with two locally run 8-billion-parameter models. Mapping 295
survey variables to concepts, opaque codes alone gave near-zero accuracy, definitions alone reached 0.55–0.62,
labels added nothing significant, and documentation transplanted from Brick, BEDES and the CityGML Energy ADE was
no better than identifiers. Ten retrieved concept cards kept accuracy at a fifth of the tokens. Stated dataset
conventions linked all imputation flags to their variables but were also applied where they did not belong. In
a national survey pipeline, AI-built profiles multiplied one indicator by 1,000. In a city-scale integration of 33,684 New York City benchmarked properties with tax lots, definitions
improved column selection, yet both models read kBtu as kilowatt-hours, overstating site energy use intensity by
215%, and a plausible column choice biased district intensity by up to 21%. Profile checks caught most such
errors but were precise only when they knew the source's conventions.

**Keywords:** Urban building energy modeling; Open data; Data schema; Generative artificial intelligence; Large
language models; Semantic interoperability

## Nomenclature {.unnumbered}

| Abbreviation or symbol | Meaning |
|---|---|
| acc@1 | Top-1 accuracy: share of variables whose first-ranked concept is the gold concept |
| ADE | Application Domain Extension (of CityGML) |
| BBL | Borough, block and lot: the tax-lot identifier of New York City |
| BEDES | Building Energy Data Exchange Specification |
| CBECS, RECS | Commercial Buildings and Residential Energy Consumption Surveys (U.S.) |
| CSVW | CSV on the Web (W3C metadata vocabulary for tabular data) |
| DCAT | Data Catalog Vocabulary |
| DDI | Data Documentation Initiative (metadata standard for survey data) |
| EUI | Energy use intensity, site energy per floor area and year (kWh/(m²·yr)) |
| LinkML | Linked data Modeling Language |
| LL84 | New York City Local Law 84 energy benchmarking disclosures |
| LLM | Large language model |
| PLUTO | Primary Land Use Tax Lot Output (New York City tax-lot data) |
| QUDT | Quantities, Units, Dimensions and Types ontology |
| SHACL | Shapes Constraint Language |
| SKOS | Simple Knowledge Organization System |
| UBEM | Urban building energy modeling |
| L0–L3, L2D, L2N, L2S, L2U, L3E, O0, O2D, XBR, XBE, XEA | Schema conditions of the mapping experiments (Section 5.4) |
| T | Sampling temperature of the language model |
| κ | Cohen's kappa (agreement between annotators) |

## 1. Introduction

Computational models of cities depend on integrating heterogeneous open data, and urban building energy
modeling (UBEM) is among the most data-hungry of them. Buildings and construction account for 32% of global
energy use and 34% of energy-related CO₂ emissions [@unep2025gsr]. UBEM estimates how policies, technologies
and climate change will affect the energy use of a building stock and supports city decarbonization plans,
building performance standards and grid planning [@reinhart2016urban; @ferrando2020urban; @johari2020urban;
@hong2020ten]. It combines weather, building geometry and characteristics, operating assumptions and measured
energy use [@cerezodavila2016modeling; @wang2022data; @malhotra2022information]. Most of these inputs now have open
sources, and the difficulty lies in combining them. A national survey of commercial buildings reports energy
in thousand Btu, codes regions as numbers, releases 151 replicate weights next to the data and marks imputed
values with separate flag variables; a footprint dataset has geometry but no attributes; a benchmarking
disclosure lists several tax lots for one property. Cities usually have enough public data for UBEM, but the
data lack common formats and keys [@chen2019development], and most UBEM studies cannot be reproduced
[@malhotra2022information]. A missed convention of this kind changes the numbers that a model produces.

Generative artificial intelligence (AI) is beginning to take over this integration work. Large language models
(LLMs) match schemas [@narayan2022foundation; @sheetrit2024rematch; @liu2025magneto], generate building energy
models from text [@jiang2024eplusllm; @zhang2025agentic], extract building data into exchange schemas
[@jia2026bemeval] and act as agents that read documentation and write data pipelines through standard
interfaces [@anthropic2024mcp; @hou2025mcp]. They read the same schemas and codebooks that modelers read, with
different limitations: they cannot ask what a code means, they see only what fits in their context window,
they produce fluent answers where the documentation is silent, and their output is only as checkable as the
format it is requested in. Building and urban data schemas are written for human readers: identifiers are
terse, definitions are missing or scattered, conventions are stated in user guides, and constraints target
database engines. Mapping real BACnet point names to Brick classes with LLMs reached 27% to 36% accuracy
[@jain2025bacnetbrick], and benchmark results overestimate LLMs on real data [@kayali2025goby].

Criteria for AI-ready data have been proposed for machine-learning datasets [@clark2024aireadiness;
@hiniduma2025datareadiness], but not for the domain schemas through which engineering data are integrated,
and there is little evidence on which schema properties help a generative AI system or on whether its
remaining errors matter for urban energy results. This paper asks **which properties of a UBEM data schema
help small, locally run language models integrate open building energy data, and whether the errors that
remain reach national and city-scale energy indicators.** The contributions, in the order of the paper, are:

1. UBEM-Link, a LinkML schema for open UBEM data with a dataset level, a variable level and an 81-concept
   vocabulary linked to Brick, BEDES and the CityGML Energy ADE, compiled into artifacts for people and for AI
   and applied to a catalog of 91 open datasets (Section 4).
2. A definition of AI-ready schemas and six design principles with measurable criteria and a verdict on each
   (Sections 3 and 8).
3. Controlled experiments with two open-weight models, including a factorial ablation of concept
   documentation and a documentation transplant from three standards (Sections 5 and 6).
4. Two end-to-end tests: AI-built profiles in a national survey pipeline, and an AI-assisted integration of
   33,684 New York City properties with tax lots, mapped by community district (Section 7).
5. An open repository that regenerates every number and figure (link withheld for anonymized review).

## 2. Related work

### 2.1 Open data, data schemas and semantic models for UBEM

UBEM reviews agree that data are the main bottleneck [@reinhart2016urban; @johari2020urban; @ali2021review;
@kamel2022systematic; @hong2025ten]. Inventories relate data availability to modeling approach [@goy2020data],
classify geometric, non-geometric, weather and calibration data [@wang2022data], and review open city-level
and multi-domain urban energy data [@jin2023review; @bishop2024review; @anselmo2026urban]. Open footprints
and heights now cover most of the world [@heris2020rasterized; @sirko2021continental;
@milojevicdupont2023eubucco; @esch2022world; @pesaresi2024advances], but footprint products differ in
completeness [@chamberlain2024building], crowdsourced building attributes are sparse and uneven
[@biljecki2023quality; @herfort2023spatio], missing attributes are increasingly predicted
[@biljecki2022global; @lei2024predicting], and data quality measurably changes UBEM results
[@nouvel2017influence]. City-scale studies document how much effort acquiring and enriching such data takes
[@rehmann2025enhancing], and open archetype templates make UBEM scalable once the inputs are assembled
[@lyu2026buildingscity].

Schemas exist at several levels. Building semantic models (Brick, Haystack, RealEstateCore, BOT, SAREF4BLDG,
BuildingSync, BEDES, HPXML and the proposed ASHRAE 223P) standardize equipment, points and building
descriptions [@balaji2018brick; @haystack4; @hammar2019realestatecore; @rasmussen2021bot;
@etsi2025saref4bldg; @long2021buildingsync; @bedes; @bpi2026hpxml; @ashrae223p; @pritoni2021metadata]. At
city scale, CityGML and its Energy ADE model buildings, zones and energy systems [@groger2012citygml;
@kutzner2020citygml; @agugiaro2018energy; @agugiaro2026further], urban energy ontologies support specific
workflows [@corrado2015data; @allan2020linked; @chadzynski2021semantic; @ma2024ontology], and exchange
schemas couple UBEM with urban microclimate models [@luo2025schema]. For datasets, DCAT 3 and schema.org describe catalog entries [@w3c2024dcat3;
@schemaorgDataset]. For variables, survey-metadata standards are mature: DDI-Codebook marks weight variables,
imputation and invalid ranges [@ddi2025codebook], and CSVW and Frictionless Table Schema declare datatypes
and missing values of tabular columns [@w3c2015tabularmetadata; @walsh2021tableschema]. What none of these
provides is a description of open datasets in UBEM terms (which workflow step a dataset feeds, how it was
generated, how fine and how linkable its records are) combined with variable-level semantics mapped to UBEM
concepts and compiled into artifacts designed for language models.

### 2.2 AI-ready data and language models over schemas

The FAIR principles ask that data be reusable by machines [@wilkinson2016fair; @jacobsen2020fair;
@desmedt2020fdo]. Datasheets [@gebru2021datasheets], data cards [@pushkarna2022datacards], nutrition labels
[@holland2018nutrition], Croissant [@akhtar2024croissant], AI-readiness criteria [@clark2024aireadiness;
@hiniduma2025datareadiness] and documentation for language models [@howard2024llmstxt] prepare data for AI
training or use, not a schema that an AI system applies and is checked against while integrating data.

Mapping a column to a concept is the column-type-annotation task of matching tables to knowledge graphs
[@jimenezruiz2020semtab] and a form of schema matching [@rahm2001survey; @do2002coma; @melnik2002similarity;
@koutras2021valentine]. With LLMs, the dominant design is retrieve-then-rerank [@sheetrit2024rematch;
@liu2025magneto; @seedat2024matchmaker], an instance of retrieval-augmented generation [@lewis2020rag].
More context is not always better [@parciak2024schema; @gan2026lessismore]; outputs vary across runs and can be
aggregated [@buss2025scalable; @wang2023selfconsistency]; and verbalized confidence is poorly calibrated
[@xiong2024uncertainty]. Knowledge graphs ground LLM answers [@pan2024llmkg], a semantic layer over an
enterprise database raised question-answering accuracy [@sequeda2023benchmark; @sequeda2025trust], and
constrained decoding guarantees that outputs follow a grammar or JSON Schema [@willard2023guided;
@geng2023grammar; @geng2025jsonschemabench]. In buildings, LLMs have been applied to energy-data schema
matching [@pan2022semantic], data transformation [@sharma2023sqlmorpher; @sharma2025datamorpher], Brick
metadata [@mulayim2024llmontologies; @zheng2025bmstagging; @wang2026point2brick; @jain2025bacnetbrick],
extraction into exchange schemas [@jia2026bemeval], energy model generation [@jiang2024eplusllm;
@jiang2025prompt; @zhang2025agentic; @zhang2025agentschema] and UBEM [@choi2024gpt]. LLMs are also used to
produce evaluation labels, which then need validation against people [@gilardi2023chatgpt; @ziems2024css].

**Gap.** These strands treat schema properties one at a time: definitions as retrieval context, a semantic
layer as grounding, a grammar as an output constraint. We found no study that compiles all of them from one
UBEM schema, measures which of them help a language model integrate building energy data, or follows the
remaining errors into urban energy indicators. Table 1 positions this paper.

Table 1. Position of this work. Columns: domain semantics for UBEM; dataset-level profile; variable-level
semantics (units, codes, weights, flags); artifacts designed for language models; machine-checkable output
constraints; controlled experiments on schema properties. Y: provided; P: partly; –: not provided.

| Work | UBEM semantics | Dataset profile | Variable semantics | For LLMs | Output constraints | Experiments |
|---|---|---|---|---|---|---|
| UBEM data reviews [@wang2022data; @jin2023review; @bishop2024review] | P | – | – | – | – | – |
| Brick, BEDES, CityGML Energy ADE | P | – | P | – | P | – |
| UBEM exchange schema [@luo2025schema] | Y | – | P | – | P | – |
| DCAT 3, schema.org, Croissant | – | Y | P | P | P | – |
| DDI-Codebook, CSVW, Table Schema | – | P | Y | – | Y | – |
| LLM schema matching [@sheetrit2024rematch; @liu2025magneto] | – | – | P | – | P | P |
| This paper | Y | Y | Y | Y | Y | Y |

## 3. AI-ready schemas

### 3.1 Definition

We call a schema AI-ready when its machine-readable artifacts are sufficient for an AI system to (i) understand
what every element means, (ii) produce instances that conform to it, and (iii) check those instances, without a
person explaining the schema, while the same artifacts remain a faithful and reviewable encoding of domain
knowledge for people. The last condition excludes schemas that are easy for a model but drop the domain's
distinctions, for example between a survey weight and an observation. Readiness is designed into the schema's
artifacts but can only be measured for a given model and task, so all results below are reported per model.

### 3.2 Design principles

The principles follow from four documented limitations of language models reading documentation: they cannot
resolve undefined identifiers, they generate plausible but invalid values when the output is unconstrained
[@geng2025jsonschemabench], they miss context outside the record they are given [@gan2026lessismore], and they
are limited by context length [@parciak2024schema]; and from the practice of reusing established standards.
Each principle has a domain-knowledge counterpart and a measurable criterion (Table 2). The experiments test
selected operationalizations of them; the last column gives the verdict reached in Section 8.

Table 2. Design principles, their mechanism in UBEM-Link, the criterion by which they are measured, the
experiment, and the verdict for the tested models and tasks.

| Principle | Mechanism in UBEM-Link | Measured by | Test | Verdict |
|---|---|---|---|---|
| P1 Define every term | A definition for every class, field, value and concept | Share of terms defined; mapping accuracy with and without definitions | E1, E6 | Supported: descriptive content beyond labels raised accuracy by 0.08–0.18; definitions alone matched full cards; on new data they improved column choice |
| P2 Close the vocabulary | Enumerations compiled to JSON Schema for constrained output | Share of invalid identifiers; accuracy | E2 | Supported as a guarantee at no accuracy cost (5 of 300 invented identifiers without it); the closed unit list must include the source's own units (E8) |
| P3 State the conventions | `Convention` class at dataset level; weights and flags at variable level | Normalization accuracy with and without the dataset card | E3, E7, E8 | Mixed: conventions fixed what entries do not state (flag links 0 to 100%) but were applied beyond their scope (E7, E8) |
| P4 Make output checkable | Types and enumerations (JSON Schema, SHACL); units and quantity kinds; profile checks | Share of wrong outputs flagged; false alarms | E4, E7, E8 | Partly: mapping checks catch 5–16% of wrong mappings; profile checks caught 13–17 of 17 city errors but were precise only with the source's missing-value label |
| P5 Fit the context window | Self-contained cards (concept cards of about 60 tokens) | Token budget; accuracy with retrieved cards | E5 | Supported when retrieval recall is high: ten cards kept accuracy at a fifth of the tokens |
| P6 Ground in domain standards | Links to Brick, BEDES and the Energy ADE; reuse of DCAT, QUDT, SKOS | Accuracy with other standards' documentation | E6 | Not supported for reusing documentation: transplanted definitions were no better than identifiers; the links themselves were not tested |

## 4. UBEM-Link

### 4.1 Architecture

UBEM-Link is written once, in LinkML [@moxon2025linkml], and compiled for two audiences (Fig. 1). The
dataset level profiles `dcat:Dataset` [@w3c2024dcat3] with six UBEM facets (Table 3), coverage, license,
access, sampling weights, conventions and the provenance of the profile. The variable level profiles
`csvw:Column`: each variable is linked to a concept and carries its QUDT unit and multiplier, code list,
missing codes, aggregation over time, and whether it is a sampling weight or an imputation flag for another
variable. The concept vocabulary holds the targets of those links. People receive YAML, documentation and an
OWL ontology; AI systems receive a schema card, concept cards and dataset cards for their context, JSON Schema
for constrained output, and SHACL shapes. The generated JSON Schema and SHACL check structure (types,
required fields, closed enumerations). Checks of meaning, such as whether a unit agrees with a variable's label,
are separate Python functions that use the schema's unit vocabulary (Section 7.2).

![Fig. 1. Architecture of UBEM-Link: domain knowledge is encoded once in a LinkML source with three parts and
compiled into artifacts for people and for AI systems.](figures/fig_architecture.png)

### 4.2 Classes and facets

Fig. 2 shows the classes, their key fields and relations. The dataset level records six independent facets,
so that each dataset is a point in a six-dimensional space and gaps can be counted along each (Table 3). A
schema rule requires every weighted sample survey to name its weights. The `Convention` class (P3) records a
rule that a publisher applies to many variables, with the variables it applies to and an example.

![Fig. 2. Classes, key fields and relations of UBEM-Link. Every class, field and enumeration value carries a
definition.](figures/fig_class_diagram.png)

Table 3. Facets of the dataset level.

| Facet | Values |
|---|---|
| UBEM workflow role | boundary conditions; geometry and inventory; building characteristics; operation and use; calibration and validation; reference simulation; context and coupling |
| Statistical nature | census; weighted sample survey; administrative record; measured monitoring; remote-sensing derived; crowdsourced; reanalysis; typical year; climate projection; simulation; standard or code; compilation |
| Spatial granularity (finest public) | 15 ranked levels from point or building to nation, plus none and unknown |
| Temporal resolution | ISO 8601 duration, static, or irregular |
| Access | open download; open API; free registration; request or agreement; restricted or commercial |
| Join keys | 24 key types, from building and parcel identifiers and addresses to census geographies, grid cells, climate zones and timestamps |

### 4.3 Concept vocabulary

The vocabulary has 81 SKOS concepts: 8 groups and 73 mapping targets (Table 4). Each target has a definition,
the entity it describes, a quantity kind and canonical unit where applicable, and generic synonyms. The
definitions and synonyms were drafted with AI assistance from general UBEM knowledge, with the CBECS and RECS
codebooks in view; synonyms avoid the surveys' variable names, and Section 6.1 tests how much the remaining
lexical overlap with survey labels matters. Sixty-three targets and two groups have 168 SKOS links to Brick 1.4.4,
BEDES 2.5 and the CityGML Energy ADE 1.0 (the latest released version; version 3.0 exists as a beta
[@agugiaro2025energyade3]); each linked term was checked to exist in the release files, and the relation type
was assigned with AI assistance and has not been audited by an independent expert. Only 4 links are exact
matches, because those standards describe equipment, points and objects while UBEM-Link concepts describe
what a dataset column measures. Ten targets have no counterpart, among them survey and replicate weights.
Further links go to CityGML 2.0 building attributes and EnergyPlus weather fields.

Table 4. Concept groups of the vocabulary (73 mapping targets; links counted to Brick, BEDES or the Energy ADE).

| Group | Targets | Linked | Examples |
|---|---|---|---|
| Building characteristics | 22 | 20 | use type, gross floor area, floor-area category, heating system |
| Weather and climate | 11 | 11 | dry-bulb temperature, global horizontal irradiance, degree days |
| Energy use | 10 | 10 | total energy, electricity, end-use energy, energy use intensity |
| Operation and use | 9 | 5 | occupants, operating hours, thermostat setpoint, comfort response |
| Building geometry | 8 | 7 | footprint, height, floors above ground, window-to-wall ratio |
| Record bookkeeping | 6 | 4 | record identifier, survey weight, replicate weight, imputation flag |
| Location | 4 | 4 | coordinates, administrative region, climate zone |
| Context and coupling | 3 | 2 | grid emission factor, energy price, land use |

### 4.4 AI documentation layer

The documentation layer is generated from the source by one command, so it cannot drift from the schema. The
schema card (about 4,200 tokens) states what the schema is for, every class and field with its definition and
allowed values, and the validation rules, and ends with a worked example. Each of the 73 concept cards is a
self-contained unit of about 60 tokens, and all of them take about 4,300 tokens (estimated at four characters
per token, as in Section 4.5; Table 6 gives the models' own counts). Each of the 91 dataset cards states a dataset's facets, weights and
conventions. Fig. 3 shows these artifacts for the 2018 Commercial Buildings Energy Consumption Survey (CBECS).

![Fig. 3. UBEM-Link applied to CBECS 2018. (a) Excerpt of the dataset card, including conventions that the
publisher states only in its user guide. (b) Three variable profiles: an energy total with its unit and
multiplier, a top-coded count, and an imputation flag linked to the variable it flags. (c) The concept cards an
AI system receives for these variables.](figures/fig_worked_example.png)

### 4.5 Audit of machine-readable releases

Table 5 compares the released term files of UBEM-Link and five standards on properties a language model needs.
A term is a class, property, enumeration value or concept; it counts as defined when it carries a
natural-language definition (`skos:definition`, `rdfs:comment`, `xs:documentation` or the BEDES definition
field). UBEM-Link defines all 271 of its terms, against 74% for Brick, 55% for BEDES and 22% for the
Energy ADE. It is the only one of the six with a JSON Schema usable for constrained output and with terms for
a survey's statistical design; survey-metadata standards such as DDI-Codebook also have such terms
[@ddi2025codebook] but no UBEM vocabulary. Its vocabulary fits in about 5,300 tokens, against about 32,000 for
Brick and about 174,000 for BEDES. The audit reflects the authors' choice of properties, on which UBEM-Link was
designed to score well; it shows what a schema built for language models must add, not the quality of
standards designed for other purposes.

Table 5. Audit of the released term files (tokens: all labels and definitions, at four characters per token).

| Standard | Terms | Defined (%) | Enum values defined (%) | Statistical-design terms | Tokens (thousands) | JSON Schema | Validation artifact |
|---|---|---|---|---|---|---|---|
| UBEM-Link | 271 | 100 | 100 | 7 | 5.3 | yes | JSON Schema, SHACL |
| Brick 1.4.4 | 1,434 | 74 | – | 0 | 32.0 | no | SHACL |
| BEDES 2.5 | 6,217 | 55 | 58 | 0 | 174.1 | no | none |
| CityGML Energy ADE 1.0 | 665 | 22 | 51 | 0 | 6.4 | no | XML Schema |
| DCAT 3 | 52 | 87 | – | 0 | 1.1 | no | none in the namespace file |
| schema.org (Dataset-related) | 163 | 100 | – | 0 | 7.6 | no | none |

### 4.6 A catalog of open UBEM datasets

To show that the schema describes real data, we profiled 91 open UBEM datasets selected by four criteria: free
access, at least one UBEM workflow role, national or wider scope (or a city dataset used as a reference, such
as New York City's benchmarking disclosures), and fields verifiable from the publisher or a peer-reviewed
descriptor. Entries were drafted by an LLM agent restricted to publisher pages and peer-reviewed descriptors,
validated against the schema, and a random sample of 20 was re-checked field by field by two further agents
(213 settled checks: 82% correct, 16% partly correct, 2% wrong, all corrected). No entry was verified by a
person, so the catalog is a purposive sample with an agent-based audit, and statistics below describe this
catalog rather than open UBEM data in general.

Because the profiles are machine-readable, gap analysis becomes a query. Of the 91 datasets, 93% can be
obtained without an agreement, 66% state a license we could verify and 27% have a persistent identifier.
Geometry is well served (18 of 23 datasets release individual buildings), building characteristics less so
(the main U.S. surveys stop at census division; Fig. 4). Linkage is the most consequential gap. Of the 48
datasets whose primary role is characteristics, operation, calibration or reference simulation, 3 share an
identifier with a footprint or parcel dataset of the same jurisdiction (energy certificates and benchmarking
disclosures), 23 can be linked only through an area code, 1 describes individual buildings only by attributes,
and 21 have no usable key. Five of the eight building-level datasets in Fig. 4 belong to the last two groups:
anonymized collections of metered or surveyed buildings without location. Section 7.3 uses one of the three
linkable datasets.

![Fig. 4. Catalog datasets by primary UBEM workflow role and the finest spatial granularity they release
publicly.](figures/fig_role_by_granularity.png)

## 5. Evaluation design

### 5.1 Data and tasks

The experiments use the public codebooks of CBECS 2018 [@eia2018cbecs] (1,249 variables) and the 2020
Residential Energy Consumption Survey (RECS) [@eia2020recs] (799 variables), which together contain 733
imputation flags and 213 sampling weights.

- **Variable mapping.** Given a variable (name, label, section, up to eight codes), the model chooses the most
  specific concept it measures, or `none`, with two alternatives and a confidence. The sampling frame is the
  1,104 substantive variables (621 CBECS, 483 RECS; imputation flags and replicate weights excluded). It was
  stratified by survey and by a rule-based draft concept assigned from codebook structure (48 strata,
  including a stratum of 68 variables matching no concept), and 300 variables (150 per survey) were drawn with
  proportional allocation, at least one per stratum and a fixed seed.
- **Code and unit normalization.** Given the verbatim codebook entry, the model returns whether the variable
  is a weight, a replicate weight or an imputation flag, the variable it flags, its unit and multiplier, its
  missing codes and its code list. Items: the 300 variables plus a fixed supplement of 60 imputation flags
  and 30 replicate weights.

### 5.2 Gold labels

Normalization gold is derived from the codebooks by a unit-tested parser written for these two surveys; it
solves normalization for them by construction but does not transfer, so Section 7.3 tests normalization without
one. Mapping gold was produced in three blind steps. Two annotators labeled all 300 variables independently,
seeing the variable and the full concept cards but neither the draft labels nor any model output, and recorded
alternatives for variables fitting two concepts; a separate adjudicator resolved disagreements. No qualified domain expert was available to annotate, so the annotators and the
adjudicator were LLM agents in fresh contexts (Claude Opus 5.5 and Claude Sonnet 5.5 as annotators, Claude
Opus 5.5 as adjudicator), from a developer other than those of the evaluated models. Agreement was high
(κ = 0.91; 276 of 300 variables), but agreement between related models is not evidence of correctness
[@ziems2024css]. Because the annotators read UBEM-Link's definitions, the gold encodes one reading of them,
and conditions that show a model the same definitions may be favored. We therefore re-score every comparison
against three further label sets, including deterministic keyword rules that were fixed before any model ran
and do not use the definitions (Section 6.7). The adjudicated gold uses 44 concepts; 5 variables have no
applicable concept and 80 have an accepted alternative. Strict accuracy scores against the adjudicated concept;
lenient accuracy also accepts the alternatives.

### 5.3 Models and protocol

We evaluate two open-weight models from different developers, Qwen3 8B [@yang2025qwen3] and Llama 3.1 8B
[@grattafiori2024llama3], run locally through Ollama 0.40.16 on one 8 GB laptop GPU (Q4_K_M quantization,
thinking disabled, 8,192-token context, output constrained by JSON Schema; model digests and all prompts in
Supplement S1 and S2). Small local models are what a city or utility can run on its own hardware at no
per-call cost, and the harder test of the schema. Larger models did not fit the available hardware. Each condition is run at temperature T = 0
for the point estimate; the base mapping conditions were repeated four times and normalization twice at
T = 0.7 to measure run-to-run variation. Every prompt and raw response is cached and released.

### 5.4 Experiments and statistics

Each experiment changes one property of the schema and holds the rest fixed (Table 2).

- **E1 Definitions (P1).** A factorial on what the concept list contains: opaque codes (O0), identifiers (L0),
  identifiers and labels (L1), opaque codes with definitions (O2D), identifiers, labels and definitions (L2D),
  full cards without definitions (L2N: labels, group, entity, unit, synonyms) and full cards (L2). Full cards in
  a shuffled order (L2S) test order sensitivity.
- **E2 Closed vocabulary (P2).** Full cards with output constrained to the concept enumeration (L2) or to any
  string (L2U).
- **E3 Conventions (P3).** Normalization with the codebook entry only, or with the dataset card stating the
  publisher's conventions.
- **E4 Checks on mappings (P4).** A variable with a unit mapped to a concept of another dimension or to a
  categorical concept, or a categorical variable mapped to a unit-bearing concept, is flagged.
- **E5 Context budget (P5).** Ten retrieved concept cards, from a lexical (L3) or a dense embedding retriever
  (L3E, nomic-embed-text), against all cards (L2).
- **E6 Standards' documentation (P6).** The same concept identifiers documented with the label and definition
  of the matching Brick, BEDES or Energy ADE term (the closest relation where several exist; uncovered
  concepts appear as identifiers only), compared with L0 and L2.
- **E7 and E8** feed AI-built inputs into pipelines (Section 7).

Baselines: TF-IDF over word and character n-grams, and dense embeddings (nomic-embed-text), both ranking
concept cards. Paired conditions are compared with exact McNemar tests, Holm-adjusted over all comparisons and
both models. Because variables of one concept are correlated, 95% intervals of accuracies and of differences
resample whole concepts (cluster bootstrap).

### 5.5 Use of AI in this study

AI was used in the research in five places: drafting and auditing catalog entries (Claude Opus 5.5 agents,
Section 4.6); drafting concept definitions and synonyms and assigning link relations (Section 4.3); producing
and adjudicating the mapping gold (Section 5.2); verifying references; and writing the analysis and plotting
code, which reads only released data and outputs. The evaluated models are the object of study. No step was
repeated by an independent domain expert; Section 8 discusses this limitation.

## 6. Results

### 6.1 E1: concept documentation

Concept documentation decided whether the models could map at all (Table 6, Fig. 5a). With opaque
codes and nothing else, both scored near zero (0.01 and 0.02), so neither had a hidden key to the concepts.
Meaningful identifiers alone gave 0.42 and 0.43, and labels did not change this significantly (Qwen3 +0.05,
p_Holm = 0.10; Llama 3.1 −0.03, p_Holm = 1.00). Adding definitions to labels raised accuracy by 0.08 for Qwen3
(p_Holm = 0.028) and 0.13 for Llama 3.1 (p_Holm < 0.001), although the concept-clustered intervals of both
differences reach just below zero. Definitions were sufficient: with opaque codes and definitions (O2D), Qwen3
reached 0.62, its highest accuracy, and Llama 3.1 0.55, equal to its full cards. They were not necessary: cards
without definitions (L2N) improved on labels by a similar amount (+0.08 and +0.18; p_Holm = 0.015 and < 0.001),
and adding definitions to them changed nothing significant (+0.03 and −0.03). Descriptive content beyond a label
therefore helps, and the definition and the other card fields largely substitute for each other; that opaque
codes with definitions did at least as well as full cards suggests that readable names invite surface matching.
On the 224 variables whose label contains neither the gold concept's label nor a synonym, the ordering is the
same (labels, definitions with opaque codes, full cards: Qwen3 0.41, 0.59, 0.52; Llama 3.1 0.29, 0.50, 0.48; S8).
Shuffling the cards left accuracy unchanged in aggregate (p_Holm = 1.00) but changed correctness for 20% and 28%
of variables, so single answers depend on prompt order. Ranking cards by TF-IDF or embedding similarity, without
a language model, reached 0.27 and 0.29.

Table 6. Variable mapping by schema condition (top-1 accuracy on 295 mappable variables, T = 0; intervals
resample concepts; tokens are mean input tokens per call as counted by Qwen3).

| Condition | Concept list shown to the model | Qwen3 8B | Llama 3.1 8B | Tokens |
|---|---|---|---|---|
| O0 | Opaque codes | 0.01 [0.00, 0.03] | 0.02 [0.00, 0.04] | 545 |
| L0 | Identifiers | 0.42 [0.29, 0.59] | 0.43 [0.28, 0.60] | 486 |
| L1 | Identifiers and labels | 0.47 [0.32, 0.66] | 0.40 [0.27, 0.58] | 809 |
| O2D | Opaque codes and definitions | 0.62 [0.52, 0.73] | 0.55 [0.42, 0.68] | 1,559 |
| L2D | Identifiers, labels and definitions | 0.55 [0.39, 0.71] | 0.53 [0.37, 0.69] | 1,823 |
| L2N | Full cards without definitions | 0.55 [0.40, 0.74] | 0.58 [0.47, 0.70] | 2,871 |
| L2 | Full concept cards | 0.59 [0.44, 0.74] | 0.55 [0.43, 0.70] | 3,884 |
| L2S | Full cards, shuffled order | 0.55 [0.42, 0.70] | 0.55 [0.44, 0.68] | 3,884 |
| L2U | Full cards, open output | 0.59 [0.44, 0.74] | 0.53 [0.42, 0.67] | 3,884 |
| L3 | Ten cards, lexical retrieval | 0.51 [0.42, 0.63] | 0.52 [0.42, 0.65] | 710 |
| L3E | Ten cards, dense retrieval | 0.56 [0.45, 0.69] | 0.58 [0.50, 0.69] | 726 |
| XBR | Brick documentation | 0.42 [0.27, 0.61] | 0.35 [0.22, 0.53] | 1,123 |
| XBE | BEDES documentation | 0.47 [0.32, 0.63] | 0.43 [0.30, 0.60] | 1,976 |
| XEA | Energy ADE documentation | 0.46 [0.34, 0.63] | 0.42 [0.29, 0.60] | 762 |
| Baselines | TF-IDF ranking 0.27; embedding ranking 0.29 | | | |

![Fig. 5. Top-1 mapping accuracy by schema condition, with 95% intervals that resample concepts. (a) What the
concept documentation contains. (b) Full cards in shuffled order, with open output, and with ten retrieved
cards.](figures/fig_design_conditions.png)

### 6.2 E2: closed vocabulary

With the full vocabulary in context, open output did not change accuracy (Qwen3 0.59 against 0.59, p_Holm =
1.00; Llama 3.1 0.53 against 0.55, p_Holm = 1.00) but produced 5 of 300 identifiers per model that do not exist
in the schema, such as `garage_size`, `refrigerated_cases` and `outage`. A constrained decoder excludes such
answers by construction, as would validating the output against the enumeration afterwards; the experiment
shows that the guarantee costs no accuracy.

### 6.3 E3: stated conventions

Without the dataset card, both models detected what a codebook entry announces: the 2 final
weights, the 30 replicate weights and the 60 imputation flags were all recognized, with 1 false weight among the 358
other variables and no false imputation flag (Table 7), and units were right for 97–99% of the 65 variables that have one.
Their errors concern what the entry does not state. CBECS gives an imputation flag the same label as the
variable it flags, and the link (ZMONUSE flags MONUSE) is a naming convention stated only in the user guide.
Without the card, neither model identified the flagged variable for any of the 30 CBECS flags; with it, both
identified all 30 (p < 0.001 for each model). With the card, Qwen3's exact missing-code accuracy rose from
0.32 to 0.50 (CBECS 0.25 to 0.52; p < 0.001) and its multiplier accuracy on the 31 scaled units from 0.94 to
1.00. The card also introduced errors: Qwen3 no longer recognized 3 of the 30 RECS replicate weights, and Llama
3.1 did not apply the missing-code conventions (0.26 with and without the card, p = 1.00). Sections 7.2 and 7.3 show further
card-induced errors.

Table 7. Code and unit normalization with and without the dataset card (T = 0). Detection rows give recall on
the positives and the number of false alarms among the other items (390 items in total).

| Field (number of positives) | Qwen3, entry only | Qwen3, with card | Llama 3.1, entry only | Llama 3.1, with card |
|---|---|---|---|---|
| Final weight (2): recall / false alarms (of 358) | 1.00 / 1 | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 |
| Replicate weight (30): recall | 1.00 | 0.90 | 1.00 | 1.00 |
| Imputation flag (60): recall / false alarms (of 330) | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 |
| Flagged variable, CBECS (30) | 0.00 | 1.00 | 0.00 | 1.00 |
| Flagged variable, RECS (30) | 1.00 | 1.00 | 1.00 | 1.00 |
| Unit (65 variables with a unit) | 0.97 | 0.97 | 0.98 | 0.98 |
| Multiplier (31 scaled units) | 0.94 | 1.00 | 0.97 | 0.97 |
| Missing codes, exact (390; CBECS / RECS) | 0.32 (0.25 / 0.38) | 0.50 (0.52 / 0.48) | 0.26 (0.24 / 0.27) | 0.26 (0.28 / 0.24) |
| Missing codes, ignoring blank codes | 0.57 | 0.74 | 0.28 | 0.31 |
| Code list, Jaccard | 0.74 | 0.79 | 0.71 | 0.73 |

### 6.4 E4: checks on mappings

With full concept cards, the quantity-kind checks flagged 20 of Qwen3's 122 wrong mappings (16%) and 7 of
Llama 3.1's 134 (5%), and 4 correct mappings of each model (2%), so 83% and 64% of the flags marked real
errors (Supplement S10). They catch one recurring confusion: a variable recording whether a fuel is used (for
example, propane for cooking) mapped to a consumption quantity. Most wrong mappings stay within one quantity
kind and pass, so these checks are an inexpensive filter, not a test of correctness.

### 6.5 E5: retrieval

Ten retrieved cards instead of all 73 cut the prompt from about 3,880 to 720 tokens. Accuracy changed by −0.08
(Qwen3; p = 0.021, p_Holm = 0.36) and −0.02 with lexical retrieval (L3), and by −0.02 and +0.04 with dense
retrieval (L3E; p_Holm = 1.00). The retriever bounds the result: the gold concept was among the ten candidates for
76% (lexical) and 82% (dense) of variables, and then accuracy was 0.68–0.69, against 0.63–0.66 with all cards.

### 6.6 E6: documentation from existing standards

Documenting UBEM-Link's concepts with the matching terms of Brick, BEDES or the Energy ADE (a
documentation transplant; 34, 57 and 35 of the 73 concepts covered) gave accuracies of 0.35–0.48: for neither
model better than identifiers alone (largest gain: BEDES for Qwen3, +0.06, p_Holm = 0.21), worse for Llama 3.1
with Brick (−0.08, p_Holm = 0.009), and 0.11–0.20 below UBEM-Link's cards (p_Holm ≤ 0.002; Fig. 6a). Coverage
explains part of this, since uncovered concepts appear as identifiers only. On the variables whose gold concept
a standard documents (Fig. 6b), BEDES terms (54 of 57 defined) improved on identifiers by 0.02 and 0.06 but stayed
0.12–0.13 below UBEM-Link's cards (p < 0.001), also for exact and close matches only (S9); Energy ADE terms (10 of
35 defined) did no better than identifiers; and on the Brick subset the three conditions did not differ
significantly. The transplant cannot separate the purpose of a definition from its wording and length.

![Fig. 6. Mapping accuracy when the same concepts are documented by UBEM-Link or by the matching terms of
existing standards. (a) All 295 mappable variables; in parentheses, the share of concepts each standard
documents. (b) Only the variables whose gold concept the standard documents, with the number of matched terms
that carry a definition. Bars show the mean of the two models, markers each model.](figures/fig_standards.png)

### 6.7 Consistency, confidence and label sensitivity

At T = 0.7, accuracy varied little across four runs (standard deviation 0.002–0.003 for Qwen3 and
0.010–0.014 for Llama 3.1; S7), but Llama 3.1's answers did: two of its runs agreed on 70–96% of variables, against
96–100% for Qwen3. Confidence was weakly informative (Fig. 7): accepting Qwen3's answers with confidence of at
least 0.9 kept 67% of variables at 0.77 accuracy, whereas Llama 3.1 gave such confidence for 17% and was no more
accurate there. Agreement filtered better: unanimity across Llama 3.1's runs (81% of variables) raised accuracy
from 0.54 to 0.60, and where both models agreed under both full and retrieved cards (36% of variables), 83% of
answers were correct. Re-scored against each annotator alone and against the keyword rules (S6), no significant
difference changed direction. The gain of definitions over labels remained significant under all four label sets
(p_Holm ≤ 0.035); two other results lost significance under one label set each (S6).

![Fig. 7. Coverage and accuracy when only some mappings are accepted automatically (full concept cards).
Lines: threshold on the model's own confidence; markers: unanimous runs at T = 0.7, agreement between L2 and
L3, and agreement of both models under both.](figures/fig_t2_coverage.png)

## 7. From AI-built inputs to energy indicators

### 7.1 National survey pipeline and its uncertainty

A reference pipeline built on the schema reproduces EIA's public-use-microdata versions of Tables B1
and C1 for CBECS 2018 within 0.01% (5,918 thousand buildings, 96,527 million ft², 6,789 trillion Btu of major
fuel use); EIA's main tables, built from the confidential full file, differ by up to 0.11%. Design-based relative standard
errors from the replicate weights [@eia2023cbecsmicrodata; @eia2023recsmicrodata] are 1.8–3.9% for the CBECS
indicators and 0.4–0.9% for the RECS ones, except for the share of buildings in hot or very hot climate zones
(weighted share of buildings, withheld records excluded), at 18% (Supplement S14). Injecting single errors
shows their size (S17): ignoring the survey weights reports 6.4 thousand buildings instead of 5.9 million and
biases floor-area-weighted EUI by −16% (food sales) to +102% (other) across 16 building activities (Fig. 8), a
dropped multiplier divides EUI by 1,000, and reading the floor top-codes 994 (10 to 14 floors) and 995 (15 or
more) as numbers overstates the mean number of floors by 175–179% whatever values are assumed for the coded
ranges (S16).

![Fig. 8. Error in floor-area-weighted energy use intensity by principal building activity if the CBECS 2018
survey weights are ignored (the 16 activities that each account for at least 0.5% of buildings).](figures/fig_weights_eui_error.png)

### 7.2 AI-built profiles in the national pipeline (E7)

The pipeline, extended to RECS 2020, reads only the profiles of the 11 variables it needs (weight, unit,
multiplier, missing codes); replacing the gold profiles by each model's makes every change in the results an
effect of the AI-built profiles. At T = 0 most indicators were reproduced exactly (Table 8). Without the card, Qwen3 gave CBECS electricity a
multiplier of one million instead of one thousand, which multiplied commercial electricity intensity by 1,000;
Llama 3.1 declared zero a missing code for residential natural gas, which dropped the households that use none
and raised gas use per household by 65%, and wrote the withheld climate-zone code as "7=Withheld for
confidentiality", which the pipeline could not match (−2.5% in the hot-zone share, well within that share's
18% standard error). With the card, no Qwen3 profile changed an indicator. Llama 3.1 fixed both of its errors but applied
the CBECS rule "code 5 means Don't know", which the card states for yes/no questions, to the climate-zone
variable, where code 5 means hot or very hot; no building remained in a hot zone. At T = 0.7, Llama 3.1's residential site energy was off by +241% in
one run and by a factor of 3,412 in the other (S15).

Of the 88 AI-built profiles (two models; entry only and with the card at T = 0; two runs at T = 0.7 without the
card; 11 variables), 51 deviated from the gold profile and 11 changed an indicator (S12). Profile checks written
after inspecting these outputs (version 1) flagged all 11, 28 of the 40 harmless deviations and none of the 37
exact profiles (S11). Applied unchanged to the 766 other benchmark profiles per model and temperature, they
flagged 15–80% of unit or multiplier errors and 14–28% of correct profiles (S13), because they did not recognize
"Inapplicable" as a missing-value label, flagged binned variables whose label names a unit, and did not read
"ccf". Version 2 corrects these causes; in-sample, it flags 25–89% of those errors without false alarms, and 10
of the 11 indicator-changing national profiles. Section 7.3 tests both versions on new data.

Table 8. National indicators from gold and from AI-built variable profiles (relative error, T = 0; 0 means
within 0.01%). Reference values with design-based standard errors from the surveys' replicate weights.

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

### 7.3 City-scale integration in New York City (E8)

New York City's 2023 benchmarking disclosures (LL84) [@nycdob2023ll84] list 33,684 properties in 265
columns, and PLUTO [@nycdcp2026pluto] lists 858,284 tax lots with their community district. Neither was consulted
when the vocabulary was written. A reference pipeline joins the first tax lot of each
property's BBL to PLUTO, converts floor area and energy to SI units, discards records with a site EUI outside
5–3,000 kWh/(m²·yr) and reports floor-area-weighted EUI by district. It links 30,046 properties (89%) to 66
districts (59 community districts and 7 joint-interest areas); city-wide site EUI is 259 kWh/(m²·yr), and the 60
districts with at least 20 properties range from 168 to 402 (Fig. 9a).

The models performed both integration steps. For each quantity the pipeline needs (tax-lot key, floor area, site
energy, electricity, natural gas) they chose one of the 265 columns, given the schema element as an identifier
(L0) or with its definition (L2) and the purpose; they then built each chosen column's profile from its name,
description and a summary of its values, without and with the LL84 dataset card. The tax-lot key is described by
UBEM-Link's join-key type `parcel_id`. In a first run we described it by the concept `record_identifier`,
defined as an identifier "within the dataset"; both models then chose the internal Property ID and nothing could
be joined. The models followed the definition; the specification error was ours (S20).

Definitions improved column choice (Table 9): from two to five acceptable columns for Qwen3 and from one to three
for Llama 3.1. With identifiers only, Qwen3 took the building identification number for the tax-lot key, Llama
3.1 took the floor area of the largest use and the site EUI for site energy, and both took weather-normalized
intensities for electricity and gas, as Llama 3.1 did even with definitions. Both models chose the floor area
that includes parking. With gold profiles, this plausible choice lowers city-wide EUI by 2.0% and district EUI by
0.3–21% (median 1.7%), by each district's share of parking (Fig. 9b): small city-wide, large locally.

Normalization failed on the unit that matters most. Both models wrote kBtu as kilowatt-hours: without the card
with multiplier 1, overstating city-wide site EUI by 215%, and with the card, which states that kBtu means
thousand Btu, with multiplier 1,000, a 3,412-fold overstatement after which the plausibility filter kept 43
properties. Post hoc, we added kBtu and therms to the closed unit vocabulary: without the card, both models then
reproduced the reference exactly, so the error came from having to express kBtu as Btu times a multiplier; with
the card, they applied the multiplier on top of kBtu (+417%), again applying a convention where it did not belong.

Of the 27 distinct profiles of these runs, 17 had a wrong unit or would drop valid values (S19). Version 1 of the
checks flagged all 17 and 9 of the 10 others, mainly because it did not recognize "Not Available" (precision 65%).
Version 2 flagged 13 of the 17 and 2 of the 10 others (precision 87%), missing four profiles that gave an energy
or area unit to an intensity column. Version 2 was committed before any city profile existed but together with
the LL84 catalog entry, and three of its terms ("Not Available", kBtu, ft²) occur in LL84 and in neither survey;
without them it behaves like version 1 (17 of 17; 9 of 10). Its precision thus came from knowing the source's
missing-value label, which the dataset card states.

Table 9. City-scale integration of LL84 benchmarking with PLUTO tax lots (T = 0). Errors are relative to the
reference pipeline (30,046 linked properties, 259 kWh/(m²·yr)).

| Columns chosen by | Profiles built by | Acceptable columns (of 5) | Linked properties, entry only / with card | City site EUI error, entry only / with card |
|---|---|---|---|---|
| Qwen3, identifiers | Qwen3 | 2 | 1 / 0 | – / – |
| Qwen3, definitions | Qwen3 | 5 | 29,794 / 43 | +210% / +553% |
| Llama 3.1, identifiers | Llama 3.1 | 1 | 67 / 67 | −81% / −81% |
| Llama 3.1, definitions | Llama 3.1 | 3 | 29,794 / 43 | +210% / +553% |
| Reference | Each model (same result) | 5 | 29,778 / 43 | +215% / +554% |
| Reference | Each model, kBtu and therms offered (post hoc) | 5 | 30,046 / 105 | 0 / +417% |
| Either model, definitions | Gold | 3–5 | 30,044 | −2.0% |

![Fig. 9. New York City, calendar year 2023. (a) Reference site EUI of benchmarked properties by community
district (districts with at least 20 properties). (b) Error of district EUI when floor area is taken from the
column both models chose with definitions (including parking), with gold profiles.](figures/fig_city_map.png)

## 8. Discussion

### 8.1 What makes a schema AI-ready for these models

Table 2 gives a verdict for each principle; three results bear on schema design. First, a model maps by meaning
only when the schema describes its terms beyond a name: opaque codes defeated both models, labels added nothing
significant, and definitions or the other descriptive fields of a card raised accuracy by 0.08–0.18. Because
definitions alone matched full cards and the gains held on variables without lexical overlap, the effect is not
only shared wording. The models also follow definitions literally: an identifier "within the dataset" led them to
an internal identifier, a join key defined as a shared parcel identifier to the tax-lot key. Definitions should be
written for the integration task, and linking keys should be defined elements of a schema. Second, conventions
help where they state what an entry does not (all 30 CBECS flags linked) but are applied beyond their scope: a
missing-code rule for yes/no questions applied to a climate zone, a multiplier applied on top of a unit that
already contains it. A convention should carry a machine-readable scope, such as a list of variables or a
pattern. Third, a closed vocabulary guarantees valid output at no accuracy cost, but its content steers the
answer: lacking kBtu, both models chose kilowatt-hours. Unit vocabularies should include the units in which
sources publish and leave conversion to QUDT factors downstream.

Documentation borrowed from Brick, BEDES and the Energy ADE did not help, which says less about those standards
than about purpose: they describe equipment, points and objects, whereas integration needs definitions of what a
column measures. Their value for UBEM-Link lies in the links into their ecosystems, which were not tested here.
Profile checks must be validated on data they were not written on: version 1 was perfect on its own errors and
raised false alarms on most held-out profiles. On the city data, generic rules flagged every error but also most
correct profiles, and knowing the source's missing-value label made them precise. Checks should therefore read
conventions from the dataset profile instead of hard-coding them; the card cannot replace checks, as it caused
several of the errors they caught.

### 8.2 Implications for urban data integration

A unit error is large and uniform, so it is noticed when results are compared with published values or filtered
for plausibility, as here. A plausible column choice, floor area with parking, changed city-wide EUI by 2% but
district EUI by up to 21%; it would pass a city-wide check and still distort a district analysis, for example of
where building performance standards bind. The catalog shows why integration is hard to begin with: 3 of 48
non-geometric building datasets share an identifier with footprints or parcels. Identifier systems such as UBID
[@wang2019ubid] and GERS [@overture2025gers] and exchange schemas between urban models [@luo2025schema] address
linkage; UBEM-Link complements them by describing in one machine-readable profile what a dataset contains, how
it is coded and through which keys it links, so that integration efforts such as that of @rehmann2025enhancing
can be repeated by a person or a model.

### 8.3 Limitations

The mapping gold was produced by LLM annotators who read the concept definitions that some conditions show the
models; four label sets, including keyword rules that do not use the definitions, agree, but expert annotation
remains the stronger test. Only two 8-billion-parameter models were evaluated; larger models may need less
documentation, and separating the effect of the schema from that of model size needs them. The survey
normalization gold comes from a parser that solves the task by construction; the city case avoids this but covers
one city, one year and five quantities, and three of its design decisions were taken after seeing results (the
description of the tax-lot key, the decomposition and the unit variant). The catalog, the concept definitions and
the links to other standards were produced with AI assistance and not reviewed by an independent expert. The
pipelines aggregate data; they do not simulate buildings.

## 9. Conclusions

This paper defined AI-ready schemas for integrating open UBEM data, implemented six design principles in
UBEM-Link, and tested them with two small local language models on national surveys and on New York City's
benchmarking and tax-lot data. Descriptions of each term beyond its name made concept mapping possible, a closed
vocabulary made output valid at no cost, retrieval kept accuracy at a fifth of the context, and documentation
borrowed from other standards did not help. Stated conventions supplied what codebook entries leave out but were
applied beyond their scope, and in the city case a unit missing from the vocabulary and a plausible column choice
caused errors of 215% city-wide and up to 21% by district. Schema checks caught most consequential errors on
new data but were precise only when they knew the source's conventions. AI-assisted integration of urban data is feasible with small local models when the
schema defines its terms and keys for the task, scopes its conventions and offers the source's own units, and
when the output is checked before it reaches an energy model. Expert-labeled benchmarks, larger models and more
cities are the next steps.

## Acknowledgement

This material is based upon work supported by the U.S. National Science Foundation under Grant No. 2623038.
Any opinions, findings, and conclusions or recommendations expressed in this material are those of the
author(s) and do not necessarily reflect the views of the National Science Foundation.

## Data availability

All code, the schema and its generated artifacts (including the AI documentation layer), the catalog and its
verification record, gold labels with annotations and rationales, prompts, cached model outputs, and the
scripts that produce every table and figure are openly available at
https://github.com/TensorBuildLab/UBEM-schema [@zhang2026ubemlinkrepo] (code under the MIT License; schema,
catalog and benchmark under CC BY 4.0). The CBECS 2018, RECS 2020, LL84 and PLUTO source data are public
[@eia2018cbecs; @eia2020recs; @nycdob2023ll84; @nycdcp2026pluto] and are downloaded by scripts that record
SHA-256 checksums.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

Large language models are the object of study in Sections 5 to 7, and their use in the research is described
in Section 5.5. In addition, during the preparation of this work the authors used Claude (Anthropic) to draft
and edit text. After using this tool, the authors reviewed and edited the content as needed and take full
responsibility for the content of the published article.

## References
