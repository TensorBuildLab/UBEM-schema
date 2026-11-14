---
title: "Meta-Urban: an AI-ready semantic schema for integrating open data in urban building energy modeling"
bibliography: references.bib
---

<!-- Drafting conventions: American spelling; "Fig. N"; "38%" without space; no em-dashes. -->

Liang Zhang^a,b,\*^, Jianli Chen^c^, Jia Zou^d^

^a^ University of Arizona, Tucson, AZ 85721, USA

^b^ National Laboratory of the Rockies, Golden, CO 80401, USA

^c^ Tongji University, Shanghai 200092, China

^d^ Arizona State University, Tempe, AZ 85281, USA

^\*^ Corresponding author. Email: liangzhang1@arizona.edu

## Abstract {.unnumbered}

Urban building energy modeling (UBEM) depends on integrating open weather, geometry, survey and meter data, a
task still done largely by hand and increasingly delegated to generative artificial intelligence (AI). We
define an AI-ready schema, one whose machine-readable artifacts let an AI system understand, produce and check
data descriptions without human explanation while remaining faithful to domain knowledge, and derive six
design principles. By them we build Meta-Urban, a schema for open UBEM data with a dataset level, a variable
level and an 81-concept vocabulary linked to Brick, BEDES and the CityGML Energy ADE, compiled into
documentation for people and into context cards, JSON Schema and SHACL shapes for AI. On two national
building energy surveys with two locally run language models, concept definitions raised mapping accuracy
from 0.42-0.43 to 0.53-0.55 (p < 0.001), and stated conventions let both models link every imputation flag
to its variable. Fed into a national building-stock pipeline, AI-built variable profiles either reproduced
the reference results or changed them by 2.5% to a factor of 1,000, as for electricity use intensity.
Schema-derived checks flagged all 12 such profiles and no correct one. AI-ready schemas make AI-assisted UBEM
data integration both more accurate and checkable.

**Keywords:** Urban building energy modeling; Building stock; Open data; Data schema; Generative artificial
intelligence; Large language models; Semantic interoperability

## Nomenclature {.unnumbered}

| Abbreviation or symbol | Meaning |
|---|---|
| acc@1 | Top-1 accuracy: share of variables whose first-ranked concept is the gold concept |
| ADE | Application Domain Extension (of CityGML) |
| AI | Artificial intelligence |
| BEDES | Building Energy Data Exchange Specification |
| CBECS | Commercial Buildings Energy Consumption Survey |
| DCAT | Data Catalog Vocabulary |
| EUI | Energy use intensity (kWh/m2) |
| LinkML | Linked data Modeling Language |
| LLM | Large language model |
| QUDT | Quantities, Units, Dimensions and Types ontology |
| RECS | Residential Energy Consumption Survey |
| SHACL | Shapes Constraint Language |
| SKOS | Simple Knowledge Organization System |
| UBEM | Urban building energy modeling |
| L0-L3, L2D, L2U, XBR, XBE, XEA | Schema conditions of the mapping experiments (Section 5.4) |
| p | p-value of the exact McNemar test |
| T | Sampling temperature of the language model |
| kappa | Cohen's kappa (inter-annotator agreement) |

## 1. Introduction

Buildings and construction account for 32% of global energy use and 34% of energy-related CO2 emissions
[@unep2025gsr]. Urban building energy modeling (UBEM) estimates how policies, technologies and climate change
will affect the energy use of a whole building stock, and it underpins city decarbonization plans, building
performance standards and grid planning [@reinhart2016urban; @ferrando2020urban; @johari2020urban;
@hong2020ten]. It depends on combining many datasets: weather, the location and shape of every building,
non-geometric characteristics such as use type, vintage and systems, assumptions on how buildings are
operated, and measured energy use for calibration [@cerezodavila2016modeling; @wang2022data;
@malhotra2022information]. Almost every one of these inputs now has an open source. Combining them is the
hard part. A national survey of commercial buildings reports energy in thousand Btu, codes regions as numbers,
releases 151 replicate weights next to the data and marks imputed values with separate flag variables; a
footprint dataset has geometry but no attributes; a smart-meter dataset has loads but no location. Cities
usually have enough public data for UBEM, but the data lack common formats and keys [@chen2019development],
and most UBEM studies cannot be reproduced [@malhotra2022information]. Each of these details, if missed,
changes the energy numbers that a model produces.

Generative AI is changing who does this integration. Large language models (LLMs) now match schemas
[@narayan2022foundation; @sheetrit2024rematch; @liu2025magneto], generate building energy models from text
[@jiang2024eplusllm; @zhang2025agentic], and act as agents that read documentation, call tools and write
data pipelines through standard interfaces for data access [@anthropic2024mcp; @hou2025mcp]. These systems
read the same schemas and codebooks that modelers read, but differently. They cannot ask a colleague what a
code means, they forget whatever does not fit in their context window, they produce fluent answers when the
documentation is silent, and their output is only as checkable as the format it is asked for. Building and
urban data schemas, meanwhile, are written for human readers: identifiers are terse, definitions are missing
or scattered, conventions live in user guides, and constraints are written for database engines rather than
for the systems that now generate the data. In buildings, mapping real BACnet point names to Brick classes
with LLMs reaches only 27% to 36% accuracy [@jain2025bacnetbrick], and benchmark results overestimate LLMs on
real data [@kayali2025goby].

Criteria for AI-ready data are being proposed for machine-learning datasets [@clark2024aireadiness;
@hiniduma2025datareadiness], but not for the domain schemas through which engineering data are integrated,
and there is no evidence on which schema properties help a generative AI system, or on whether its remaining
errors matter for energy results. This paper therefore asks one question: **can a UBEM data schema be designed
to be AI-ready, so that generative AI integrates open building energy data correctly without a person
explaining it while the schema remains a faithful encoding of domain knowledge, and does the difference reach
the energy results that UBEM produces?** We define AI-readiness and derive six design principles (Section 3),
build Meta-Urban 2.0 by them and show it concretely, including a verified catalog of 91 open UBEM datasets
(Section 4), test each principle with controlled experiments on two national building energy surveys using
two open-weight LLMs that a city or utility can run on its own hardware (Sections 5 and 6), and feed the
AI-built inputs into a national building-stock pipeline (Section 7).

The contributions are:

1. Meta-Urban 2.0, an AI-ready schema for open UBEM data: a LinkML source with a dataset level (a DCAT 3
   profile with six UBEM facets and explicit conventions), a variable level (concept, unit, codes, weights and
   imputation flags) and an 81-concept vocabulary with 168 verified links to Brick, BEDES and the CityGML
   Energy ADE, compiled into documentation for people and into context cards, JSON Schema and SHACL shapes
   for AI, and applied to a verified catalog of 91 open datasets (Section 4).
2. A definition of AI-ready schemas and six design principles that make a schema usable by generative AI
   without giving up domain fidelity, with a checklist for schema designers (Sections 3 and 8).
3. Controlled experiments that isolate each principle and compare the schema with Brick, BEDES, the CityGML
   Energy ADE, DCAT 3 and schema.org, with significance tests and a label-sensitivity analysis (Sections 5
   and 6).
4. End-to-end evidence for UBEM: AI-built variable profiles drive a building-stock pipeline that reproduces
   the published national totals; the errors that remain are rare but change national energy indicators by
   up to three orders of magnitude, and rules derived from the schema catch them (Section 7).
5. An open repository from which every artifact, number and figure is regenerated
   (https://github.com/TensorBuildLab/UBEM-schema).

## 2. Related work

### 2.1 Open data and semantic models for UBEM

UBEM reviews agree that data are the main bottleneck [@reinhart2016urban; @johari2020urban; @ali2021review;
@kamel2022systematic; @hong2025ten]. Inventories relate data availability to modeling approach [@goy2020data],
classify geometric, non-geometric, weather and calibration data [@wang2022data], and review open city-level
and multi-domain urban energy data [@jin2023review; @bishop2024review; @anselmo2026urban]. Open footprints
and heights now cover most of the world [@heris2020rasterized; @sirko2021continental;
@milojevicdupont2023eubucco; @esch2022world; @pesaresi2024advances], with known gaps in crowdsourced data
[@haklay2008openstreetmap], and data quality measurably changes UBEM results [@nouvel2017influence]. These
works are written for people; none releases a machine-actionable profile of each dataset.

Semantic models describe the objects that the data are about. At building scale, Brick, Haystack,
RealEstateCore, BOT, SAREF4BLDG, BuildingSync, BEDES and the proposed ASHRAE 223P standardize equipment, points
and building descriptions [@balaji2018brick; @haystack4; @hammar2019realestatecore; @rasmussen2021bot;
@etsi2025saref4bldg; @long2021buildingsync; @bedes; @ashrae223p; @pritoni2021metadata]. At city scale,
CityGML and its Energy ADE model buildings, zones and energy systems [@groger2012citygml; @kutzner2020citygml;
@agugiaro2018energy; @agugiaro2026further], and urban energy ontologies support specific workflows
[@corrado2015data; @allan2020linked; @chadzynski2021semantic; @ma2024ontology]. Dataset-level metadata is
the domain of DCAT 3 and schema.org [@w3c2024dcat3; @schemaorgDataset]. None describes what UBEM integration
needs to know about a dataset (which workflow step it feeds, how it was generated, how fine and how linkable
its records are) or, at variable level, which columns are weights, imputation flags or top-coded values.

### 2.2 AI-ready data and grounding language models in schemas

The FAIR principles ask that data be reusable by machines as well as people [@wilkinson2016fair;
@jacobsen2020fair; @desmedt2020fdo]. For machine learning, datasheets [@gebru2021datasheets], data cards
[@pushkarna2022datacards], nutrition labels [@holland2018nutrition] and Croissant [@akhtar2024croissant]
document how a dataset was made, criteria for AI-ready data are emerging [@clark2024aireadiness;
@hiniduma2025datareadiness], and documentation written for language models is being proposed
[@howard2024llmstxt]. These efforts prepare data for AI training, not a schema that an AI system must read,
apply and be checked against while it integrates data.

Schema matching has a long history [@rahm2001survey; @do2002coma; @melnik2002similarity;
@koutras2021valentine]; with LLMs the dominant design is retrieve-then-rerank [@sheetrit2024rematch;
@liu2025magneto; @seedat2024matchmaker], an instance of retrieval-augmented generation [@lewis2020rag].
Context matters but more is not always better [@parciak2024schema; @gan2026lessismore]; outputs vary across
runs [@buss2025scalable]; and confidence needs calibration [@wang2023selfconsistency; @xiong2024uncertainty].
Knowledge graphs ground LLM answers [@pan2024llmkg], and a semantic layer over an enterprise database raised
question-answering accuracy substantially [@sequeda2023benchmark; @sequeda2025trust]. Constrained decoding
guarantees that outputs follow a grammar or JSON Schema [@willard2023guided; @geng2023grammar;
@geng2025jsonschemabench]. In buildings, language models have been applied to energy-data schema matching
[@pan2022semantic], data transformation [@sharma2023sqlmorpher; @sharma2025datamorpher], Brick metadata
[@mulayim2024llmontologies; @zheng2025bmstagging; @wang2026point2brick; @jain2025bacnetbrick], energy model
generation [@jiang2024eplusllm; @jiang2025prompt; @zhang2025agentic; @zhang2025agentschema] and UBEM
[@choi2024gpt].

**Gap.** Each of these strands treats one property in isolation: definitions as retrieval context, a
semantic layer as grounding, a grammar as an output constraint. No study has designed a UBEM schema so that
all of them come from one source, measured which schema properties help a generative AI system integrate
building energy data, or traced the remaining errors to energy results. Table 1 summarizes the position of this paper.

Table 1. Position of this work. Y: yes; P: partly; -: no.

| Work | Domain semantics for UBEM | Dataset-level profile | Variable-level semantics | Designed for AI use | Output constraints | Experiments on schema properties |
|---|---|---|---|---|---|---|
| UBEM data reviews [@wang2022data; @jin2023review; @bishop2024review] | P | - | - | - | - | - |
| Brick, BEDES, CityGML Energy ADE | P (objects) | - | P | - | P | - |
| DCAT 3, schema.org Dataset | - | Y | - | - | - | - |
| Croissant, datasheets, data cards | - | Y | P | P (training) | P | - |
| LLM schema matching [@sheetrit2024rematch; @liu2025magneto] | - | - | P | - | P | P (context size) |
| Zhang et al. 2023 preprint [@zhang2023taxonomy] | P | P | P | - | - | - |
| This paper | Y | Y | Y | Y | Y | Y |

## 3. AI-ready schemas

### 3.1 Definition

A schema is AI-ready when its machine-readable artifacts are sufficient for an AI system to (i) understand
what every element means, (ii) produce instances that conform to it, and (iii) check those instances, without
a person explaining the schema, while the same artifacts remain a faithful and reviewable encoding of domain
knowledge for people. The last clause matters. A schema that is easy for a model but loses the domain's
distinctions (for example, between a survey weight and an observation) would make AI integration fluent and
wrong. AI-readiness is therefore a property of the schema, not of the model, and it can be designed and tested.

### 3.2 Design principles

Six principles follow from the ways generative AI systems differ from human readers (Section 1). Each has a
domain-knowledge counterpart that the schema must preserve, and each is tested by an experiment (Table 2).

Table 2. Design principles of an AI-ready schema, how Meta-Urban implements them, the domain knowledge they
preserve, and the experiment that tests them.

| Principle | Why AI needs it | Mechanism in Meta-Urban | Domain knowledge preserved | Test |
|---|---|---|---|---|
| P1 Define every term | A model cannot ask what an identifier means | A definition for every class, field, value and concept, written to be applied without other context | UBEM workflow roles, survey methodology, concept hierarchy | E1 |
| P2 Close the vocabulary | Free text invites invented terms | Enumerations compiled to JSON Schema, used for constrained output | Controlled facets and concept ids | E2 |
| P3 State the conventions | Rules stated once in a user guide are invisible in each record | `Convention` class at dataset level; weights and flags explicit at variable level | Publisher conventions for flags, codes, units, weights | E3 |
| P4 Make output checkable | Fluent answers can be wrong | Types, patterns, rules and quantity kinds, compiled to JSON Schema and SHACL | Units and quantity kinds (QUDT), survey rules | E4, E7 |
| P5 Fit the context window | Context is finite and costly | Self-contained cards: schema card, concept cards (~60 tokens), dataset cards | Same content, modular | E5 |
| P6 Ground in domain standards | Shared terms let AI reuse what it knows | Verified SKOS links to Brick, BEDES, CityGML Energy ADE; DCAT, QUDT, SKOS reuse | Existing standards remain authoritative | E6 |

P1 and P6 are the classical virtues of a good vocabulary, made complete; P2 and P4 make the schema a
contract that output can be held to; P3 targets conventions written once in a user guide and never in the
codebook entry a model reads; P5 makes the schema divisible into self-contained parts.

## 4. Meta-Urban 2.0

### 4.1 Architecture

Meta-Urban is written once, in LinkML [@moxon2025linkml], and compiled for two audiences (Fig. 1). The
source has three parts. The dataset level profiles `dcat:Dataset` [@w3c2024dcat3] with six UBEM facets
(Table 3), coverage, license, access, sampling weights, conventions and the provenance of the profile
itself. The variable level profiles `csvw:Column`: each variable is linked to a concept with a SKOS relation
and carries its QUDT unit and multiplier, code list, missing codes, aggregation over time, and whether it is
a sampling weight or an imputation flag for another variable. The concept vocabulary holds the targets of
those links. From this source, people get YAML, documentation and an OWL ontology; AI systems get a schema
card, concept cards and dataset cards for their context, JSON Schema for constrained output, and SHACL
shapes to check what they produce. Because both audiences are served from one source, an improvement made
for one reaches the other.

![Fig. 1. Architecture of Meta-Urban 2.0: domain knowledge is encoded once in a LinkML source with three
parts and compiled into artifacts for people and for AI systems; AI output is checked against the same
schema. Drawn with code written with AI assistance (see the generative AI declaration).](figures/fig_architecture.png)

### 4.2 Classes and facets

Fig. 2 shows the classes, their key fields and relations. The dataset level separates six facets that the
2023 version of this work mixed in one list of categories [@zhang2023taxonomy], so that each dataset is a
point in a six-dimensional space and gaps can be counted along each (Table 3). A schema rule requires every
weighted sample survey to name its weights, because a pipeline that ignores them is wrong even when every
value is transcribed correctly (Section 7). The `Convention` class (P3) records rules that the publisher
applies to many variables at once, each with the variables it applies to, the rule and an example.

![Fig. 2. Classes, key fields and relations of Meta-Urban 2.0. Every class, field and enumeration value
carries a definition. Drawn with code written with AI assistance (see the generative AI declaration).](figures/fig_class_diagram.png)

Table 3. Facets of the dataset level (all values defined in `schema/meta_urban.yaml`).

| Facet | Values |
|---|---|
| UBEM workflow role | boundary conditions; geometry and inventory; building characteristics; operation and use; calibration and validation; reference simulation; context and coupling |
| Statistical nature | census; weighted sample survey; administrative record; measured monitoring; remote-sensing derived; crowdsourced; reanalysis; typical year; climate projection; simulation; standard or code; compilation |
| Spatial granularity (finest public) | 17 ranked levels from building or station to nation, plus none and unknown |
| Temporal resolution | ISO 8601 duration, static, or irregular |
| Access | open download; open API; free registration; request or agreement; restricted or commercial |
| Join keys | 24 key types, from building and parcel identifiers and addresses to census geographies, grid cells, climate zones and timestamps |

### 4.3 Concept vocabulary

The vocabulary has 81 SKOS concepts: 8 groups and 73 mapping targets (Table 4). Each target has a
definition, the entity it describes, a quantity kind and canonical unit where applicable, and generic
synonyms that deliberately avoid the variable names of the benchmark surveys, so that the evaluation is not
inflated by leakage. Sixty-four targets have 168 SKOS links to Brick 1.4.4, BEDES 2.5 and the CityGML Energy ADE 1.0, each
checked verbatim against the release files. Only 4 are exact matches, a difference of purpose rather than of
quality: the standards describe equipment, points and objects, whereas Meta-Urban concepts describe what a
dataset column measures. Ten concepts, including survey and replicate weights, have no counterpart.

Table 4. Concept groups of the vocabulary.

| Group | Concepts | Linked to other standards | Examples |
|---|---|---|---|
| Building characteristics | 21 | 20 | use type, gross floor area, wall construction, heating system |
| Weather and climate | 11 | 11 | dry-bulb temperature, global horizontal irradiance, degree days |
| Energy use | 10 | 10 | total energy, electricity, end-use energy, energy use intensity |
| Operation and use | 9 | 5 | occupants, operating hours, thermostat setpoint, comfort response |
| Building geometry | 8 | 8 | footprint, height, floors above ground, window-to-wall ratio |
| Record bookkeeping | 6 | 4 | record identifier, survey weight, replicate weight, imputation flag |
| Location | 4 | 4 | coordinates, administrative region, climate zone |
| Context and coupling | 3 | 2 | grid emission factor, energy price, land use |

### 4.4 AI documentation layer

The documentation layer (`schema/ai/`) is generated from the source by one command, so it can never drift
from the schema. The schema card (about 4,200 tokens) states what the schema is for, every class and field
with its definition and allowed values, and the validation rules, and ends with a worked example; it is the
system prompt for profiling a dataset. Each of the 73 concept cards is a self-contained retrieval unit of
about 60 tokens; all of them together take about 4,300 tokens, small enough to give a small model the whole
vocabulary at once. Each of the 91 dataset cards states a dataset's facets, weights and conventions. JSON
Schema constrains output; SHACL shapes and quantity-kind rules check it. Fig. 3 shows these artifacts for the
2018 Commercial Buildings Energy Consumption Survey (CBECS).

![Fig. 3. Meta-Urban applied to CBECS 2018. (a) Excerpt of the dataset card, including conventions that the
publisher states only in its user guide. (b) Three variable profiles: an energy total with its unit and
multiplier, a top-coded count, and an imputation flag linked to the variable it flags. (c) The concept cards
an AI system receives for these variables. Drawn with code written with AI assistance (see the generative AI
declaration).](figures/fig_worked_example.png)

### 4.5 How the schema compares with existing standards

Table 5 compares the machine-readable releases of Meta-Urban and five standards on properties that an AI
system needs (`meta_urban.standards`). All terms of Meta-Urban carry a definition, against 74% for Brick, 45%
for BEDES and 22% for the Energy ADE; all of its enumeration values are defined, against 58% and 51% for
BEDES and the Energy ADE. It is the only one that publishes a JSON Schema usable for constrained output, and
the only one with terms for a survey's statistical design. Its whole vocabulary fits in about 5,300 tokens,
whereas Brick needs about 32,000 and BEDES about 158,000, more than the context window of the models used
here. These are not judgments of the standards, which were designed for other purposes; they show which
properties a schema built for AI use must add.

Table 5. AI-readiness audit of the released term files (generated: `paper/tables/ai_readiness_audit.csv`).
Tokens: approximate size of all labels and definitions.

| Standard | Terms | Defined (%) | Enum values defined (%) | Statistical-design terms | Tokens (thousands) | JSON Schema | Validation |
|---|---|---|---|---|---|---|---|
| Meta-Urban 2.0 | 271 | 100 | 100 | 7 | 5.3 | yes | JSON Schema, SHACL |
| Brick 1.4.4 | 1,434 | 74 | - | 0 | 32.0 | no | SHACL |
| BEDES 2.5 | 6,217 | 45 | 58 | 0 | 157.6 | no | none |
| CityGML Energy ADE 1.0 | 665 | 22 | 51 | 0 | 6.4 | no | XML Schema |
| DCAT 3 | 52 | 87 | - | 0 | 1.1 | no | none in the namespace file |
| schema.org (Dataset-related) | 163 | 100 | - | 0 | 7.6 | no | none |

### 4.6 A verified catalog as a demonstration

To show that the schema describes real data, we profiled 91 open UBEM datasets: 15 boundary-condition, 23
geometry, 15 characteristics, 7 operation, 21 calibration, 5 reference-simulation and 5 context datasets.
Entries were drafted by an LLM research agent restricted to publisher pages and peer-reviewed descriptors and
validated against the schema; a random sample of 20 was re-verified field by field by two separate agents
(213 settled checks: 82% correct, 16% partly correct, 2% wrong, all corrected;
`catalog/verification_2026-11-13.csv`).

Because the profiles are machine-actionable, gap analysis becomes a query. Of the 91 datasets, 93% can be
obtained without an agreement, but only 66% state a license we could verify and 27% have a persistent
identifier. Geometry is well served (18 of 23 datasets release individual buildings), while building
characteristics are not (the main U.S. surveys stop at census division; Fig. 4). Linkage is the most
consequential gap: of 48 datasets whose primary role is characteristics, operation, calibration or reference
simulation, only 3 share an identifier with building footprints (all administrative: energy certificates and
benchmarking disclosure), 23 link only through area codes and 21 have no usable key. For most of open UBEM,
characteristics and energy can be joined to geometry only statistically, through weighted surveys whose
conventions an integrator, human or AI, must get right.

![Fig. 4. Catalog datasets by primary UBEM workflow role and the finest spatial granularity they release
publicly. Plotted from the released catalog with code written with AI assistance (see the generative AI
declaration).](figures/fig_role_by_granularity.png)

## 5. Evaluation design

### 5.1 Data and tasks

The experiments use the public codebooks of the 2018 CBECS [@eia2018cbecs] (1,249 variables) and the 2020
Residential Energy Consumption Survey (RECS) [@eia2020recs] (799 variables), which differ in format, units
and conventions and together contain 733 imputation flags and 213 sampling weights. Two tasks mirror what an
AI system must do to integrate them.

- **Variable mapping.** Given a variable (name, label, section, up to eight codes), choose the most specific
  concept it measures, or `none`, with two alternatives and a confidence. Evaluation sample: 300 substantive
  variables (150 per survey), stratified by concept with a fixed seed.
- **Code and unit normalization.** Given the verbatim codebook entry, return whether it is a weight, a
  replicate weight or an imputation flag, the variable it flags, its unit and multiplier, its missing codes
  and its code list. Items: the 300 variables plus a fixed supplement of 60 imputation flags and 30
  replicate weights, so that detection is scored on positives as well as negatives.

### 5.2 Gold labels

Normalization gold is derived deterministically from the codebooks and unit-tested. Mapping gold was produced
in three blind steps. Two annotators labeled all 300 variables independently, seeing neither the rule-based labels used for
stratification nor any model output, and recorded alternatives only for variables that fit two concepts; a
separate adjudicator resolved disagreements. Because qualified human annotators were not available, these were
LLM agents in fresh contexts (Claude Opus 5.5 and Claude Sonnet 5.5 as annotators, Claude Opus 5.5 as
adjudicator), from a developer other than those of the evaluated models; all labels and rationales are
released, and every result is re-scored against four label sets (Section 6.7). Agreement was high (Cohen's kappa = 0.91; 276 of 300
variables). The adjudicated gold uses 45 concepts; 5 variables have no applicable concept and 80 (27%) have
an accepted alternative. Strict accuracy scores against the adjudicated concept, lenient accuracy also
accepts the alternatives.

### 5.3 Models and protocol

We evaluate two open-weight models from different developers, Qwen3 8B [@yang2025qwen3] and Llama 3.1 8B
[@grattafiori2024llama3], run locally through Ollama 0.40.16 on a laptop GPU (4-bit quantization, thinking
disabled, 8,192-token context). We chose small local models deliberately. Survey microdata, utility records
and building registers are often held under agreements that rule out sending records to a commercial
service, and small models are the harder test: if schema properties help anywhere, they should help where
the model knows least. The harness also runs API-hosted models. The task instructions and the schema
artifacts form the system prompt; the variable is the only per-call content. Each condition is run at
temperature 0 for the point estimate; the base mapping conditions were also repeated four times, and
normalization twice, at temperature 0.7 to measure run-to-run consistency. Every prompt and raw response is cached and released.

### 5.4 Experiments

Each experiment changes one property of the schema and holds everything else fixed (Table 2).

- **E1 Define every term (P1).** The vocabulary is given as concept ids only (L0), ids and labels (L1), ids,
  labels and definitions (L2D), or full concept cards with definitions, group, entity, unit and synonyms
  (L2).
- **E2 Close the vocabulary (P2).** Full concept cards with the output constrained to the enumeration of
  concept ids (L2) or to any string (L2U).
- **E3 State the conventions (P3).** Normalization with the codebook entry only, or with the dataset card,
  which states the publisher's conventions for flags, codes, units and weights.
- **E4 Make output checkable (P4).** Mappings are checked against the schema's quantity kinds: a variable
  with a unit mapped to a concept of another dimension or to a categorical concept, or a categorical
  variable mapped to a unit-bearing quantity, is flagged. No model call is needed.
- **E5 Fit the context window (P5).** A lexical retriever over concept cards proposes ten candidates and the
  model chooses among them (L3), against the full vocabulary (L2).
- **E6 Ground in domain standards (P6).** The same concept ids are documented with the label and definition
  of the matching Brick, BEDES or Energy ADE term instead of Meta-Urban's card (concepts a standard does not
  cover appear as ids only), and compared with L0 and L2.
- **E7 End-to-end effect on energy results (P3, P4).** The normalization outputs for the 11 variables that a
  national building-stock pipeline needs (weights, floor area, energy by fuel, climate zone) replace the gold
  profiles in that pipeline (Section 7.2), with and without the dataset card, and four profile checks derived
  from the schema are applied to them.

A lexical baseline (TF-IDF over word and character n-grams) provides a floor. Differences between paired
conditions are tested with exact McNemar tests; intervals are bootstrap 95% intervals.

## 6. Results

### 6.1 E1: definitions, not labels, carry the gain

Definitions carry most of the gain (Table 6, Fig. 5). Labels alone help one model and hurt the
other (Qwen3 +0.05, p = 0.005; Llama 3.1 -0.03, p = 0.22): a label such as "Gross floor area" adds little to
the identifier `gross_floor_area`. Adding a definition to each label raised accuracy to 0.55 (Qwen3) and 0.53
(Llama 3.1), +0.13 and +0.10 over identifiers only (p < 0.001 for both). Full concept cards, which add the
group, entity, unit and synonyms, added a further 0.04 and 0.02, which is not significant for either model
(p = 0.17 and 0.48). Definitions therefore account for 78% (Qwen3) and 83% (Llama 3.1) of the gain of full
cards, at 47% of their token cost (about 1,820 instead of 3,880 input tokens per call). P1 is the most
effective principle and the easiest to audit: a schema either defines a term or it does not (Table 5).

Table 6. Variable mapping by schema condition (top-1 accuracy on 295 mappable variables, temperature 0;
lenient accuracy counts accepted alternatives; tokens are mean input tokens per call). Generated:
`paper/tables/bench_design_conditions.csv`.

| Condition | Exp. | Qwen3 8B acc@1 [95% CI] | Qwen3 lenient | Llama 3.1 8B acc@1 [95% CI] | Llama lenient | Out of vocabulary (%) | Input tokens |
|---|---|---|---|---|---|---|---|
| L0 identifiers only | E1 | 0.42 [0.36, 0.47] | 0.52 | 0.43 [0.37, 0.48] | 0.55 | 0 | 480 |
| L1 identifiers and labels | E1 | 0.47 [0.41, 0.53] | 0.58 | 0.40 [0.34, 0.45] | 0.50 | 0 | 800 |
| L2D + definitions | E1 | 0.55 [0.49, 0.61] | 0.67 | 0.53 [0.47, 0.58] | 0.63 | 0 | 1,820 |
| L2 full concept cards | E1 | 0.59 [0.53, 0.64] | 0.69 | 0.55 [0.49, 0.60] | 0.64 | 0 | 3,880 |
| L2U full cards, open output | E2 | 0.59 [0.54, 0.65] | 0.69 | 0.53 [0.48, 0.59] | 0.63 | 1.7 | 3,880 |
| L3 ten retrieved cards | E5 | 0.51 [0.46, 0.57] | 0.60 | 0.52 [0.46, 0.58] | 0.61 | 0 | 705 |
| XBR Brick documentation | E6 | 0.42 [0.37, 0.48] | 0.52 | 0.35 [0.30, 0.41] | 0.44 | 0 | 1,120 |
| XBE BEDES documentation | E6 | 0.45 [0.39, 0.50] | 0.53 | 0.40 [0.34, 0.46] | 0.51 | 0 | 1,070 |
| XEA Energy ADE documentation | E6 | 0.46 [0.40, 0.52] | 0.55 | 0.42 [0.37, 0.48] | 0.51 | 0 | 760 |

Lexical baseline (TF-IDF): acc@1 0.27, lenient 0.35. Paired tests: `paper/tables/bench_design_tests.csv`.

![Fig. 5. Top-1 mapping accuracy by schema condition for both models, with bootstrap 95% intervals.
Plotted from the released model outputs with code written with AI assistance (see the generative AI
declaration).](figures/fig_design_conditions.png)

### 6.2 E2: a closed vocabulary keeps answers inside the schema

With the full vocabulary in context, freeing the output barely changed accuracy (Qwen3 0.59 against 0.59,
p = 0.50; Llama 3.1 0.53 against 0.55, p = 0.13). It did change what the answers were. Five of 300 answers of
each model (1.7%) were identifiers that do not exist in the schema, such as `basement`, `garage_size`,
`refrigerated_cases`, `outage` and `location_of_main_water_heating_equipment`. Each is a plausible name that
would pass a casual review, and each would break a join or silently create a new category downstream. Some
also point at real gaps: the power-outage variable has no concept in the vocabulary (Section 8). A closed
vocabulary therefore turns "usually valid" into "always valid" at no cost in accuracy. The invented terms,
collected from an unconstrained run rather than accepted, are useful as candidates for the next version of
the vocabulary.

### 6.3 E3: stated conventions remove the errors a model cannot avoid

Without the dataset card, both models already handle what a codebook entry announces: they detect weights,
replicate weights and imputation flags with recall 1.00 and at most 0.3% false alarms (Table 7) and get units
right for 96-98% of the variables that have one. Their errors concern what the entry does not say. CBECS gives
an imputation flag the same label as the variable it flags, and the link (ZMONUSE flags MONUSE) is a naming
convention stated only in the user guide. Without the card, neither model identified the flagged variable for
any of the 30 CBECS flags; with it, both identified all 30 (p < 0.001 for each model).

Missing codes follow the same logic. With the card, Qwen3's exact missing-code accuracy rose from 0.32 to 0.49
(CBECS 0.25 to 0.52; 119 items gained, 50 lost; p < 0.001) and its multiplier accuracy on scaled units from
0.94 to 1.00. Llama 3.1 used the convention for flags but not for missing codes (0.26 against 0.24, p = 0.34),
and with the card Qwen3 missed 4 of the 30 RECS replicate weights. Stated conventions supply knowledge that no
model can infer from a record, but how much of it a model applies varies, so a convention should also be
enforced by a check (Section 7.2).

Table 7. Code and unit normalization with and without the dataset card (temperature 0). Detection rows give
recall on positives and false alarms on the 300 substantive variables. Generated:
`paper/tables/bench_t3_conventions.csv`.

| Field | Qwen3, entry only | Qwen3, with card | Llama 3.1, entry only | Llama 3.1, with card |
|---|---|---|---|---|
| Survey weight: recall / false alarm (%) | 1.00 / 0.3 | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 |
| Replicate weight: recall | 1.00 | 0.87 | 1.00 | 1.00 |
| Imputation flag: recall / false alarm (%) | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 |
| Flagged variable, CBECS (30 flags) | 0.00 | 1.00 | 0.00 | 1.00 |
| Flagged variable, RECS (30 flags) | 1.00 | 1.00 | 1.00 | 1.00 |
| Unit (52 variables with a unit) | 0.96 | 0.96 | 0.98 | 0.98 |
| Multiplier (31 scaled units) | 0.94 | 1.00 | 0.97 | 0.97 |
| Missing codes, exact (CBECS / RECS) | 0.32 (0.25 / 0.38) | 0.49 (0.52 / 0.47) | 0.26 (0.24 / 0.27) | 0.24 (0.25 / 0.23) |
| Missing codes, ignoring blank codes | 0.57 | 0.73 | 0.28 | 0.29 |
| Code list, Jaccard | 0.74 | 0.78 | 0.71 | 0.73 |

### 6.4 E4: the schema catches a share of wrong answers by itself

With full concept cards, the quantity-kind rules flag 18 of Qwen3's 96 wrong mappings (19%) and 7 of Llama
3.1's 110 (6%), while flagging only 2% of correct mappings (`paper/tables/bench_t2_verification.csv`). The
rules catch exactly the confusion that is most common for both models: a variable that records whether a
fuel is used (for example, propane used for cooking) mapped to a consumption quantity. The check costs
nothing and needs no second model; in a pipeline, flagged mappings go to review.

### 6.5 E5: retrieval cuts the context but inherits the retriever's misses

Choosing among ten retrieved concept cards uses 18% of the input tokens of the full vocabulary (about 705
instead of 3,880 per call). It does not match the full vocabulary: -0.02 for Llama 3.1 (p = 0.51) and -0.08
for Qwen3 (p = 0.02). The loss comes from the retriever: the gold concept is among the ten candidates for
223 of 295 variables (76%); on those, retrieval is as accurate as the full vocabulary or better (0.68-0.69
against 0.63-0.66), and on the other 72 it cannot be right. For a vocabulary of this size, the whole set of
cards fits in context and should be given; for vocabularies the size of Brick or BEDES (Table 5), retrieval
is unavoidable and its recall becomes the ceiling.

### 6.6 E6: documentation from existing standards

Documenting the same concept identifiers with the terms of existing standards did not reproduce the effect of
Meta-Urban's cards (Fig. 6a). Over all 295 variables, Brick, BEDES and Energy ADE documentation gave 0.42-0.46
(Qwen3) and 0.35-0.42 (Llama 3.1): no better than identifiers only (0.42-0.43), worse for Llama 3.1 with Brick
(p < 0.001), and 0.13-0.20 below Meta-Urban's cards in all six comparisons (p < 0.001). Part of the gap is
coverage: the standards match 47% (Brick), 78% (BEDES) and 48% (Energy ADE) of the concepts.

Restricted to the variables whose gold concept a standard documents (Fig. 6b;
`paper/tables/bench_design_transplant_subset.csv`), the result splits by whether the documentation defines
its terms. Brick defines 31 of its 34 matched terms, and on its 111 variables it did as well as Meta-Urban
(Qwen3 0.66 against 0.67, p = 1.00; Llama 3.1 0.58 against 0.60, p = 0.66). BEDES and the Energy ADE define
only 12 of 57 and 10 of 35; the rest are bare labels such as "Derivation Method" or "WeatherData". On their
variables they stayed at the identifiers-only level and 0.14-0.16 below Meta-Urban (p <= 0.001). Documentation
helps an AI system because it defines its terms, not because of its source. This confirms E1 independently and
shows that P1 and P6 are complementary: linking to a standard reuses its definitions, and where it has none,
the schema must write its own.

![Fig. 6. Mapping accuracy when the same concepts are documented by Meta-Urban or by the matching terms of
existing standards. (a) All 295 mappable variables; in parentheses, the share of concepts each standard
documents. (b) Only the variables whose gold concept the standard documents, with the number of matched terms
that carry a definition. Bars show the mean of the two models, markers each model. Plotted from the released model
outputs with code written with AI assistance (see the generative AI declaration).](figures/fig_standards.png)

### 6.7 Consistency, confidence and label sensitivity

Across five repeats the standard deviation of accuracy is at most 0.013, and Qwen3's repeats agree pairwise on
98% of variables (Llama 3.1: 79-91%), so self-consistency is no signal of correctness. Agreement across
conditions is: when both models agree under both L2 and L3, 36% of variables are mapped at 0.83 accuracy, and
Qwen3's confidence of at least 0.95 maps 51% at 0.84 (Fig. 7). The conclusions do not depend on the labels:
re-scored against each annotator alone and against deterministic keyword rules fixed before any model was run,
L2 beats L0 for both models under all four label sets (p <= 0.001)
(`paper/tables/bench_t2_label_sensitivity.csv`).

![Fig. 7. Coverage and accuracy when only some mappings are accepted automatically (full concept cards).
Lines: threshold on the model's own confidence; markers: unanimous repeats, agreement between L2 and L3,
and agreement of both models under both. Plotted from the released model outputs with code written with AI
assistance (see the generative AI declaration).](figures/fig_t2_coverage.png)

## 7. From AI-built inputs to building-stock energy results

### 7.1 Reference pipeline and sensitivity

A reference pipeline built on the schema reproduces the published totals of CBECS 2018 within 0.01% (5,918
thousand buildings, 96,527 million square feet, 6,789 trillion Btu of major fuel use), which validates it.
Table 8 injects each class of normalization error into it. Ignoring the survey weights reports 6.4 thousand
buildings instead of 5.9 million and, less obviously, biases floor-area-weighted energy use intensity by
-16% (food sales) to +102% (other) across the 16 main building activities, with 12 of 16 overestimated
(Fig. 8). A dropped multiplier changes national energy use intensity by three orders of magnitude, and
top-codes read as numbers nearly triple the mean number of floors.

Table 8. Effect of single normalization errors on CBECS 2018 quantities (generated:
`paper/tables/downstream_d3_sensitivity.csv`).

| Error type | Quantity | Correct | With error | Relative error |
|---|---|---|---|---|
| Unit multiplier dropped (thousand Btu read as Btu) | National EUI (kWh/m2) | 221.9 | 0.22 | -99.9% |
| Wrong unit (thousand Btu read as kWh) | National EUI (kWh/m2) | 221.9 | 757.1 | +241% |
| ft2 read as m2 | Total floor area (million m2) | 8,968 | 96,527 | +976% |
| Top-codes read as values (NFLOOR 994/995) | Weighted mean floors | 1.46 | 4.08 | +179% |
| Withheld code kept (PUBCLIM 7) | Share in hot zone | 0.138 | 0.135 | -2.5% |
| Survey weights ignored | Buildings (thousand) | 5,918 | 6.4 | -99.9% |

Note: for NFLOOR the correct value assumes 12 floors for code 994 and 15 for code 995.

![Fig. 8. Error in floor-area-weighted energy use intensity by principal building activity when the CBECS
2018 survey weights are ignored. Plotted from the public microdata with code written with AI assistance (see
the generative AI declaration).](figures/fig_weights_eui_error.png)

### 7.2 End-to-end: AI-built profiles in the pipeline (E7)

Sensitivities show what an error would do; E7 shows what the models' actual errors do. The pipeline was
extended to RECS 2020 and made to read nothing but the variable profiles of the 11 variables it needs: which
column is the weight, and each column's unit, multiplier and missing codes. Each model's normalization of
those codebook entries then replaced the gold profiles, so that any change in the national results is caused
by the AI-built profile alone (`python -m meta_urban.endtoend`).

At temperature 0, the AI-built pipelines reproduced most national indicators exactly (Table 9), but not all.
Without the dataset card, Qwen3 gave CBECS electricity a multiplier of one million instead of one thousand,
multiplying commercial electricity use intensity by 1,000. Llama 3.1 declared zero a missing code for
residential natural gas, which silently dropped households without gas and raised gas use per household by
65%, and wrote the withheld climate-zone code in a form the pipeline could not match (-2.5% in the hot-zone
share). With the card, every Qwen3 profile was right; Llama 3.1 fixed both errors but read residential
electricity in thousand Btu as kWh (+241%) and declared "hot or very hot" a missing code, emptying the hot
zone. At temperature 0.7, Llama 3.1's residential site energy was off by +241% and by a factor of 3,400, and
Qwen3 dropped the zeros of natural gas in one of two runs.

Table 9. National indicators computed by the same pipeline from gold and from AI-built variable profiles
(relative error, temperature 0; 0 means within 0.01%). Generated: `paper/tables/endtoend_quantities.csv`.

| Survey | Indicator | Reference | Qwen3, entry only | Qwen3, with card | Llama 3.1, entry only | Llama 3.1, with card |
|---|---|---|---|---|---|---|
| CBECS | Buildings (thousand) | 5,918 | 0 | 0 | 0 | 0 |
| CBECS | Floor area (million m2) | 8,968 | 0 | 0 | 0 | 0 |
| CBECS | EUI, major fuels (kWh/m2) | 221.9 | 0 | 0 | 0 | 0 |
| CBECS | EUI, electricity (kWh/m2) | 133.4 | +99,900% | 0 | 0 | 0 |
| CBECS | EUI, natural gas (kWh/m2) | 75.2 | 0 | 0 | 0 | 0 |
| CBECS | Share in hot or very hot zone (%) | 13.8 | 0 | 0 | -2.5% | -100% |
| RECS | Households (million) | 123.5 | 0 | 0 | 0 | 0 |
| RECS | Site energy per household (MWh) | 22.5 | 0 | 0 | 0 | 0 |
| RECS | Electricity per household (MWh) | 10.6 | 0 | 0 | 0 | +241% |
| RECS | Natural gas per household (MWh) | 10.1 | 0 | 0 | +65% | 0 |
| RECS | Site EUI (kWh/m2) | 133.1 | 0 | 0 | 0 | 0 |

The schema makes these errors detectable before they reach a result. Four rules that need only the codebook
entry and the schema were applied to every AI-built profile: the unit must agree with the unit named in the
label; the multiplier must agree with a "thousand" or "hundred" qualifier; a missing code must be a listed code
with a non-substantive label; and a missing code of a continuous variable must lie outside its valid range.
Across all 88 AI-built profiles (two models, four runs, 11 variables), the rules flagged all 12 that changed a
national indicator and none of the 36 correct ones (`paper/tables/endtoend_summary.csv`); they also flagged 28
of 40 harmless deviations, mostly missing codes written as labels.

### 7.3 What this means for AI-assisted UBEM

The errors that matter are rare, discrete and large. They are not noise that averages out across a building
stock: each one is a wrong reading of a single convention, and it shifts a national indicator by a fixed
factor. Weights and imputation flags, whose loss has the largest effect, were detected without error (Table
7). Units and multipliers were right for 94-98% of variables at temperature 0, and the rare exception moved
an indicator by a factor of 1,000; at temperature 0.7, Llama 3.1's unit accuracy fell to 0.71 and its
multiplier accuracy on scaled units to 0.69, while Qwen3 stayed at 0.96 and 0.97. Missing codes and top-codes
remain the least reliable field even with the dataset card. Three practical rules follow for AI-assisted
UBEM: decode deterministically; state the conventions of every dataset in its profile; and validate every
AI-built profile against the schema before it enters a pipeline, which here cost nothing and caught every
consequential error.

## 8. Discussion

**Implications for UBEM.** For modelers, the end-to-end results argue for a division of labor: a small local
model drafts the variable profiles, the schema checks them, and a person reviews only what is flagged, which
here was every profile that would have changed an energy result. For data publishers, one machine-readable
profile per dataset, stating its weights and conventions, removes errors that no model can avoid and serves
human analysts equally. For the field, identifiers matter more than more datasets: only 3 of 48 non-geometric
building datasets can be linked to individual buildings, so characteristics and energy are joined to
geometry statistically, and survey weights decide whether such a join is right (Fig. 8).

**What makes a schema AI-ready.** Three results generalize beyond this case. First, definitions are the active
ingredient. They produced about four-fifths of the gain of full concept cards at half the tokens (E1), and
documentation borrowed from other standards helped exactly as far as it contained definitions (E6). Second,
some knowledge cannot be inferred from a record however capable the model is. Which variable an imputation
flag refers to, or which codes mean "not applicable", are publisher conventions, and only stating them in the
schema made them available (E3). Third, structural properties act as guarantees rather than as accuracy
gains: a closed vocabulary removed invented identifiers without changing accuracy (E2), and rules derived from
units, labels and code lists caught every consequential error in the pipeline (E4, E7). Retrieval (E5) is a
necessity for large vocabularies rather than an improvement, and its recall bounds what the model can
achieve. Together, the experiments suggest a checklist for designing a domain schema that AI systems will use:

1. Write a definition for every class, field, value and concept that can be applied without other context;
   labels are not enough.
2. Publish the closed vocabularies as a JSON Schema that can constrain generation.
3. Move conventions out of user guides into the schema, as structured rules with examples.
4. Give quantities their units and quantity kinds, and codes their meanings, so that inconsistent output can
   be detected automatically.
5. Keep each unit of documentation self-contained and small, and measure the token cost of the whole.
6. Link to the domain's standards rather than replacing them, and verify every link.
7. Generate all of the above from one source, so that what people review is what AI systems read.

**Domain fidelity is not traded for AI-readiness.** Every artifact the models received is generated from the
source that people review, and every property that helped the models (definitions, closed facets, stated
conventions, quantity kinds) is also something a careful analyst needs. The distinctions a generic dataset
vocabulary lacks, such as survey weights, imputation flags and top-codes, are precisely those whose loss
changes energy results most (Section 7). AI-readiness, in this sense, is domain knowledge written down
completely enough that a reader without context can apply it.

**Limitations.** (1) The mapping gold was built by LLM annotators and was not audited by domain experts. Their
agreement was high, and the conclusions hold under four label sets, but absolute accuracies could change
under expert labels; the rationales and an audit sheet are released for that check. (2) Only two small
open-weight models were tested; larger models will likely score higher, and our claims concern the relative
value of schema properties, which held for both. (3) The experiments use two U.S. surveys; codebooks in
other languages and administrative registers may behave differently. (4) The documentation transplant gives
other standards the same concept ids and therefore measures their documentation, not their structure. (5)
The catalog is a purposive sample drafted with an LLM; its verified error rate is 2% wrong and 16% partly
correct fields. (6) The vocabulary is version 0.1; annotators found topics it lacks (energy insecurity,
electric vehicles, outages, internet access), which version 0.2 should add. (7) The end-to-end pipeline uses
11 variables and national indicators; urban-scale pipelines join more datasets and may expose other errors.

## 9. Conclusions

Urban building energy modeling depends on open data that generative AI is now asked to integrate, but the
schemas describing those data are written for people. We defined an AI-ready schema as one whose artifacts let
an AI system understand, produce and check data descriptions without human explanation while remaining a
faithful encoding of domain knowledge, derived six design principles, and built Meta-Urban 2.0 for open UBEM
data by them. Tested on two national building energy surveys with two local language models, definitions were
the property that mattered most, raising top-1 mapping accuracy from 0.42-0.43 to 0.53-0.55, while
documentation from standards that give labels without definitions did no better than bare identifiers. Stated
conventions supplied what no model could infer from a record. In a national building-stock pipeline,
AI-built inputs mostly reproduced the reference, but the remaining errors changed indicators such as
electricity use intensity by up to a factor of 1,000, and rules derived from the schema flagged every one of
them without false alarms. The recommendation for UBEM is to describe every dataset with an AI-ready profile,
generated for people and AI from one source, and to validate every AI-built input against it. The schema, its
AI documentation layer, the catalog of 91 datasets, the benchmark and all model outputs are open.

## CRediT authorship contribution statement

**Liang Zhang:** Conceptualization, Methodology, Software, Investigation, Data curation, Formal analysis,
Visualization, Writing - original draft, Writing - review and editing. **Jianli Chen:** Investigation,
Writing - review and editing. **Jia Zou:** Investigation, Writing - review and editing.

## Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that
could have appeared to influence the work reported in this paper.

## Funding

[Funding statement]

## Data availability

All code, the schema and its generated artifacts (including the AI documentation layer), the catalog and its
verification record, gold labels with annotations and rationales, prompts, cached model outputs, and the
scripts that produce every table and figure are openly available at
https://github.com/TensorBuildLab/UBEM-schema [@zhang2026metaurbanrepo] (code under the MIT License; schema,
catalog and benchmark under CC BY 4.0). The CBECS 2018 and RECS 2020 source data are public
[@eia2018cbecs; @eia2020recs] and are downloaded by `scripts/download_data.py`, which records SHA-256
checksums; the release files of the compared standards are downloaded by `scripts/download_standards.py`.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

Large language models are the object of study in Sections 5 and 6, where their use is described in full. In
addition, during the preparation of this work the authors used Claude (Anthropic) to draft and re-verify
catalog entries (Section 4.6), to produce and adjudicate the mapping gold labels (Section 5.2), to verify
references and standard mappings, to write the analysis and plotting code from which all figures are
generated, and to draft and edit text. After using this tool, the authors reviewed and edited the content as
needed and take full responsibility for the content of the published article.

## Acknowledgments

[Acknowledgments]

## References
