---
title: "Meta-Urban: an AI-ready semantic schema for integrating open urban building energy data with generative artificial intelligence"
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

Generative artificial intelligence (AI) is increasingly used to find, interpret and join data, yet data
schemas are still written for human readers. We define an AI-ready schema as one whose machine-readable
artifacts let an AI system understand, produce and check data descriptions without human explanation, while
remaining a faithful encoding of domain knowledge, and we derive six design principles for it. We apply them
to urban building energy modeling, where integrating open weather, geometry, survey and meter data is still
manual, and build Meta-Urban, a schema with a dataset level, a variable level and an 81-concept vocabulary
linked to building standards, compiled from one source into documentation for people and into context
cards, JSON Schema and SHACL shapes for AI. On two national building energy surveys, with two locally run
language models, concept cards raised top-1 mapping accuracy from 0.42-0.43 to 0.55-0.59 (p < 0.001), about
four-fifths of it from definitions alone. A dataset card stating the publisher's conventions let both models
identify the variable each imputation flag refers to (0% to 100% on the commercial survey), a closed
vocabulary removed invented identifiers, and schema constraints flagged wrong mappings automatically. The
same concepts documented by Brick, BEDES or the CityGML Energy ADE matched Meta-Urban only where those
standards define their terms, and did no better than bare identifiers where they give labels alone.
AI-readiness is thus a designable property of a schema, and definitions are its core. All resources are
open.

**Keywords:** AI-ready data; Data schema; Generative artificial intelligence; Large language models; Urban
building energy modeling; Open data; Semantic interoperability

## 1. Introduction

Buildings and construction account for 32% of global energy use and 34% of energy-related CO2 emissions
[@unep2025gsr]. Urban building energy modeling (UBEM) estimates how policies, technologies and climate change
will affect the energy use of a whole building stock [@reinhart2016urban; @ferrando2020urban;
@johari2020urban; @hong2020ten], and it depends on combining many datasets: weather, the location and shape
of every building, non-geometric characteristics such as use type, vintage and systems, assumptions on how
buildings are operated, and measured energy use for calibration [@cerezodavila2016modeling; @wang2022data;
@malhotra2022information]. Almost every one of these inputs now has an open source. Combining them is the
hard part. A national survey of commercial buildings reports energy in thousand Btu, codes regions as
numbers, releases 151 replicate weights next to the data and marks imputed values with separate flag
variables; a footprint dataset has geometry but no attributes; a smart-meter dataset has loads but no
location. Cities usually have enough public data for UBEM, but the data lack common formats and keys
[@chen2019development], and most UBEM studies cannot be reproduced [@malhotra2022information].

Generative AI changes who does this integration. Large language models (LLMs) now match schemas
[@narayan2022foundation; @sheetrit2024rematch; @liu2025magneto], generate building energy models from text
[@jiang2024eplusllm; @zhang2025agentic], and act as agents that read documentation, call tools and write
data pipelines, increasingly through standard interfaces for data access [@anthropic2024mcp;
@hou2025mcp]. These systems read the same schemas, codebooks and documentation that people read, but they
read them differently. They cannot ask a colleague what a code means, they forget whatever does not fit in
their context window, they produce fluent answers when the documentation is silent, and their output is
only as checkable as the format it is asked for. Schemas, meanwhile, are still written for human readers:
identifiers are terse, definitions are missing or scattered, conventions live in user guides, and
constraints, where they exist, are written for database engines rather than for the systems that now
generate the data.

This gap has been recognized for machine-learning datasets, where metadata formats such as Croissant
[@akhtar2024croissant], datasheets [@gebru2021datasheets] and data cards [@pushkarna2022datacards] describe
data for training and evaluation, and criteria for AI-ready data are being proposed [@clark2024aireadiness;
@hiniduma2025datareadiness]. It has not been addressed for the domain schemas through which engineering data
are integrated, and there is no evidence on which properties of such a schema actually help a generative AI
system. In buildings, mapping real BACnet point names to Brick classes with LLMs reaches only 27% to 36%
accuracy [@jain2025bacnetbrick], and benchmark results overestimate LLMs on real data [@kayali2025goby].

This paper asks one question: **can a domain data schema be designed to be AI-ready, so that generative AI
can use it to integrate data correctly without a person explaining it, while it remains a faithful encoding
of domain knowledge, and which design properties make the difference?** We answer it for open UBEM data in
three steps. First, we define AI-readiness and derive six design principles, each paired with the domain
knowledge it must preserve (Section 3). Second, we design Meta-Urban 2.0 by these principles and show it
concretely: its structure, its AI documentation layer, a worked example and a verified catalog of 91 open
datasets described with it (Section 4). Third, we test each principle with controlled experiments on variables
sampled from the 2,048 of two national building energy surveys, using two open-weight LLMs that a city or utility can run
on its own hardware, compare the schema with five existing standards, and trace the remaining errors to
their effect on UBEM results (Sections 5 to 7).

The contributions are:

1. A definition of AI-ready schemas and six design principles that make a schema usable by generative AI
   without giving up domain fidelity, with a checklist for schema designers (Sections 3 and 8).
2. Meta-Urban 2.0, an AI-ready schema for open UBEM data: a LinkML source with a dataset level (a DCAT 3
   profile with six UBEM facets and explicit conventions), a variable level (concept, unit, codes, weights
   and imputation flags) and an 81-concept vocabulary with 168 verified links to Brick, BEDES and the CityGML
   Energy ADE, compiled into documentation for people and into context cards, JSON Schema and SHACL shapes
   for AI (Section 4).
3. An evaluation that isolates each design principle and compares the schema with Brick, BEDES, the CityGML
   Energy ADE, DCAT 3 and schema.org, on blind double-annotated labels, with significance tests and a
   label-sensitivity analysis (Sections 5 and 6).
4. Evidence that the errors that remain matter: a verified catalog shows that only 3 of 48 non-geometric
   building datasets can be linked to individual buildings, and a reference pipeline shows how each class of
   AI error changes UBEM quantities (Sections 4.6 and 7).
5. An open repository from which every artifact, number and figure is regenerated
   (https://github.com/TensorBuildLab/UBEM-schema).

## 2. Related work

### 2.1 Open data and semantic models for UBEM

UBEM reviews agree that data are the main bottleneck [@reinhart2016urban; @johari2020urban; @ali2021review;
@kamel2022systematic; @hong2025ten]. Inventories of UBEM inputs relate data availability to modeling
approach [@goy2020data], classify geometric, non-geometric, weather and calibration data [@wang2022data],
review open city-level energy datasets [@jin2023review] and organize multi-domain urban energy data
[@bishop2024review; @anselmo2026urban]. Open footprints and heights now cover most of the world
[@heris2020rasterized; @sirko2021continental; @milojevicdupont2023eubucco; @esch2022world;
@pesaresi2024advances], with known gaps in crowdsourced data [@haklay2008openstreetmap], and data quality
measurably changes UBEM results [@nouvel2017influence]. These works are written for people; none releases
a machine-actionable profile of each dataset.

Semantic models describe the objects that the data are about. At building scale, Brick, Haystack,
RealEstateCore, BOT, SAREF4BLDG, BuildingSync, BEDES and the proposed ASHRAE 223P standardize equipment,
points and building descriptions [@balaji2018brick; @haystack4; @hammar2019realestatecore;
@rasmussen2021bot; @etsi2025saref4bldg; @long2021buildingsync; @bedes; @ashrae223p; @pritoni2021metadata].
At city scale, CityGML and its Energy ADE model buildings, thermal zones and energy systems
[@groger2012citygml; @kutzner2020citygml; @agugiaro2018energy; @agugiaro2026further], and urban energy
ontologies support specific workflows [@corrado2015data; @allan2020linked; @chadzynski2021semantic;
@ma2024ontology]. Dataset-level metadata is the domain of DCAT 3 and schema.org [@w3c2024dcat3;
@schemaorgDataset]. None of these describes what UBEM integration needs to know about a dataset: which
workflow step it feeds, how it was generated, how fine its locations are and how its records can be linked;
nor, at variable level, which columns are weights, imputation flags or top-coded values.

### 2.2 AI-ready data and machine-actionable metadata

The FAIR principles ask that data be findable, accessible, interoperable and reusable by machines as well as
people [@wilkinson2016fair; @jacobsen2020fair], and FAIR Digital Objects package data with machine-actionable
metadata [@desmedt2020fdo]. For machine learning, datasheets [@gebru2021datasheets], data cards
[@pushkarna2022datacards] and nutrition labels [@holland2018nutrition] document how a dataset was made, and
Croissant gives a machine-readable format that training frameworks can load directly
[@akhtar2024croissant]. Recent work defines AI-readiness of data by criteria such as provenance,
characterization and standardized formats [@clark2024aireadiness; @hiniduma2025datareadiness]. A related
practice publishes documentation written for language models, such as the llms.txt proposal
[@howard2024llmstxt]. These efforts make data ready to be consumed by AI training. They do not address a
schema that a generative AI system must read, apply and be checked against while it integrates data, and
they report no experiments on which schema properties help.

### 2.3 Grounding language models in schemas

Schema matching has a long history [@rahm2001survey; @do2002coma; @melnik2002similarity] and a standard
benchmark suite [@koutras2021valentine]. With LLMs the dominant design is retrieve-then-rerank
[@sheetrit2024rematch; @liu2025magneto; @seedat2024matchmaker], an instance of retrieval-augmented
generation [@lewis2020rag]. Context matters but more is not always better [@parciak2024schema;
@gan2026lessismore]; outputs vary across runs [@buss2025scalable]; and confidence needs calibration
[@wang2023selfconsistency; @xiong2024uncertainty]. Knowledge graphs and ontologies ground LLM answers
[@pan2024llmkg]: adding a semantic layer over an enterprise database raised question-answering accuracy
substantially [@sequeda2023benchmark; @sequeda2025trust]. Constrained decoding with grammars or JSON Schema
guarantees that outputs follow a format [@willard2023guided; @geng2023grammar; @geng2025jsonschemabench]. In
buildings, language models have been applied to schema matching of energy data [@pan2022semantic],
data transformation [@sharma2023sqlmorpher; @sharma2025datamorpher], Brick metadata
[@mulayim2024llmontologies; @zheng2025bmstagging; @wang2026point2brick; @jain2025bacnetbrick], energy model
generation [@jiang2024eplusllm; @jiang2025prompt; @zhang2025agentic; @zhang2025agentschema] and UBEM
[@choi2024gpt].

**Gap.** Each of these strands treats one property in isolation: definitions as retrieval context, a
semantic layer as grounding, a grammar as an output constraint. No study has designed a domain schema so that
all of them come from one source, and none has measured which schema properties help a generative AI system
integrate engineering data. Table 1 summarizes the position of this paper.

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
| P4 Make output checkable | Fluent answers can be wrong | Types, patterns, rules and quantity kinds, compiled to JSON Schema and SHACL | Units and quantity kinds (QUDT), survey rules | E4 |
| P5 Fit the context window | Context is finite and costly | Self-contained cards: schema card, concept cards (~60 tokens), dataset cards | Same content, modular | E5 |
| P6 Ground in domain standards | Shared terms let AI reuse what it knows | Verified SKOS links to Brick, BEDES, CityGML Energy ADE; DCAT, QUDT, SKOS reuse | Existing standards remain authoritative | E6 |

P1 and P6 are the classical virtues of a good vocabulary, made complete and explicit. P2 and P4 turn the
schema into a contract that generated output can be held to. P3 addresses a failure that is specific to
data integration: conventions that apply to hundreds of variables are written once in a user guide and never
in the codebook entry that a model reads. P5 recognizes that an AI system reads the schema through a
context window, so the schema must be divisible into self-contained parts.

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
inflated by leakage. Sixty-four targets have at least one link to another standard: 168 SKOS links to Brick
1.4.4, BEDES 2.5 and the CityGML Energy ADE 1.0, each checked verbatim against the release files, plus
CityGML building attributes and EnergyPlus weather fields. Only 4 of the 168 links are exact matches, which
reflects a difference of purpose rather than of quality: Brick and the Energy ADE describe equipment, points
and objects; BEDES composes characteristics from terms and qualifiers; Meta-Urban concepts describe what a
dataset column measures. Ten concepts have no counterpart in any of the three, including survey and
replicate weights, appliance use, time use, thermal comfort responses and land use.

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

To show that the schema can describe real data and answer practical questions, we profiled 91 open datasets
that feed UBEM: 15 boundary-condition, 23 geometry, 15 characteristics, 7 operation, 21 calibration, 5
reference-simulation and 5 context datasets (by primary role). Each entry was drafted by an LLM research
agent instructed to fill fields only from publisher pages or peer-reviewed descriptors, to resolve every DOI
and to write null rather than guess, then validated against the schema. A random sample of 20 entries was
re-verified field by field by two separate agents against publisher pages (230 checks; record in
`catalog/verification_2026-11-13.csv`): of the 213 checks that could be settled, 82% were correct, 16% partly
correct (mostly incomplete or out of date) and 2% wrong, and all were corrected.

Because the profiles are machine-actionable, gap analysis becomes a query. Of the 91 datasets, 93% can be
obtained without an agreement, but only 66% state a license we could verify and 27% have a persistent
identifier. Geometry is well served (18 of 23 datasets release individual buildings), while building
characteristics are not (the two main U.S. surveys stop at census division and state; Fig. 4). The most
consequential finding concerns linkage. Classifying each dataset by its best way of linking to building
footprints shows that, of 48 datasets whose primary role is characteristics, operation, calibration or
reference simulation, only 3 share an identifier with footprints (all administrative: energy certificates
and benchmarking disclosure), 23 can be linked only through area codes and 21 have no usable key. For most
of open UBEM, characteristics and energy can be joined to geometry only statistically. This is the setting
in which AI-assisted integration operates, and it is why the variable-level semantics tested next matter.

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
in three blind steps. Two annotators labeled all 300 variables independently, seeing the variable and the
vocabulary but neither the rule-based labels used to stratify the sample nor any model output, and recorded
alternatives only for variables that genuinely fit two concepts. A third, separate adjudicator resolved the
disagreements. The annotators and the adjudicator were LLM agents in fresh contexts restricted to the
annotation files (Claude Opus 5.5 and Claude Sonnet 5.5 as annotators, Claude Opus 5.5 as adjudicator),
because qualified human annotators were not available. The evaluated models come from other developers and
were never used to build the gold; all labels, alternatives and rationales are released; and every result is
re-scored against four label sets (Section 6.7). Agreement was high (Cohen's kappa = 0.91; 276 of 300
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
cards over identifiers, at 47% of their token cost (about 1,820 instead of 3,880 input tokens per call).
Lenient accuracy follows the same pattern. Of the six principles, P1 is the most effective, and it is also
the easiest to audit: a schema either defines a term or it does not (Table 5).

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

Without the dataset card, both models already handle what a codebook entry announces. They detect
survey weights, replicate weights and imputation flags with recall 1.00 and at most 0.3% false alarms
(Table 7), and they get units right for 96-98% of the variables that have one. Their errors are about what
the entry does not say. CBECS gives an imputation flag the same label as the variable it flags; the link
(ZMONUSE flags MONUSE) is a naming convention stated only in the user guide. Without the card, neither model
identified the flagged variable for any of the 30 CBECS flags, typically naming the flag itself. With the
card's convention, both identified it for all 30 (30 gained, none lost; p < 0.001 for each model).

Missing codes follow the same logic, because which codes mean "not applicable", "don't know" or "withheld",
and which are top-codes, is fixed per survey. With the card, Qwen3's exact missing-code accuracy rose from
0.32 to 0.49 (CBECS 0.25 to 0.52; 119 items gained, 50 lost; p < 0.001), and its multiplier accuracy on
scaled units rose from 0.94 to 1.00. Llama 3.1 used the convention for flags but not for missing codes (0.26
against 0.24, p = 0.34). One regression appeared: with the card, Qwen3 no longer recognized 4 of the 30 RECS
replicate weights. Stated conventions supply knowledge that no model can infer from a single record. How much
of it a model applies depends on the model, so a convention should be stated in the schema and also enforced
by a check, not only offered as context.

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

Documenting the same concept identifiers with the definitions of existing standards did not reproduce
the effect of Meta-Urban's cards (Fig. 6a). Over all 295 variables, Brick, BEDES and Energy ADE
documentation gave 0.42-0.46 (Qwen3) and 0.35-0.42 (Llama 3.1). That is no better than identifiers only
(0.42-0.43), worse for Llama 3.1 with Brick (0.35, p < 0.001), and 0.13-0.20 below Meta-Urban's cards in all
six comparisons (p < 0.001). Part of the gap is coverage: the standards have a matching term for 47% (Brick),
78% (BEDES) and 48% (Energy ADE) of the concepts.

The more telling comparison restricts each standard to the variables whose gold concept it documents
(Fig. 6b; `paper/tables/bench_design_transplant_subset.csv`). There the result splits by whether the
documentation contains definitions. Brick defines 31 of its 34 matched terms, and on its 111 variables its
documentation did as well as Meta-Urban's cards (Qwen3 0.66 against 0.67, p = 1.00; Llama 3.1 0.58 against
0.60, p = 0.66). BEDES and the Energy ADE define only 12 of 57 and 10 of 35 matched terms; the others are
bare labels such as "Derivation Method" or "WeatherData". On their variables, their documentation stayed at
the identifiers-only level (BEDES 0.43 and 0.41 against 0.40 and 0.43; Energy ADE 0.32 and 0.36 against 0.28
and 0.36) and 0.14-0.16 below Meta-Urban's cards (p <= 0.001). Documentation helps an AI system because it
defines its terms, not because of the standard it comes from. This confirms E1 from an independent direction,
and it shows that P1 and P6 are complementary: linking to a standard lets a schema reuse good definitions,
and where the standard has none, the schema must write its own.

![Fig. 6. Mapping accuracy when the same concepts are documented by Meta-Urban or by the matching terms of
existing standards. (a) All 295 mappable variables; in parentheses, the share of concepts each standard
documents. (b) Only the variables whose gold concept the standard documents, with the number of matched terms
that carry a definition. Bars show the mean of the two models, markers each model. Plotted from the released model
outputs with code written with AI assistance (see the generative AI declaration).](figures/fig_standards.png)

### 6.7 Consistency, confidence and label sensitivity

Repeated runs are stable: across five repeats the standard deviation of accuracy is at most 0.013, and Qwen3's
repeats agree pairwise on 98% of variables (Llama 3.1: 79-91%). Self-consistency is therefore no signal of
correctness, but agreement across conditions is: when both models agree under both L2 and L3, 36% of
variables are mapped at 0.83 accuracy, and Qwen3's own confidence of at least 0.95 maps 51% at 0.84 (Fig. 7).
The conclusions do not depend on the labels. Re-scored against each annotator alone and against
deterministic keyword rules fixed before any model was run, L2 beats L0 for both models under all four
label sets (p <= 0.001), and accuracies at a given condition differ by at most 0.04
(`paper/tables/bench_t2_label_sensitivity.csv`).

![Fig. 7. Coverage and accuracy when only some mappings are accepted automatically (full concept cards).
Lines: threshold on the model's own confidence; markers: unanimous repeats, agreement between L2 and L3,
and agreement of both models under both. Plotted from the released model outputs with code written with AI
assistance (see the generative AI declaration).](figures/fig_t2_coverage.png)

## 7. Why the remaining errors matter

A reference pipeline built on the schema reproduces the published totals of CBECS 2018 within 0.01% (5,918
thousand buildings, 96,527 million square feet, 6,789 trillion Btu of major fuel use), which validates it
as the reference. Table 8 injects each class of normalization error into it. Ignoring the survey weights
reports 6.4 thousand buildings instead of 5.9 million and, less obviously, biases floor-area-weighted energy
use intensity by -16% (food sales) to +102% (other) across the 16 main building activities, with 12 of 16
overestimated (Fig. 8). A dropped multiplier changes national energy use intensity by three orders of
magnitude, and top-codes read as numbers nearly triple the mean number of floors. Set against the
experiments, the risks rank differently from the raw sensitivities. Weights and flags were detected without
error, so the largest effect is also the least likely. At temperature 0, units and multipliers were right for
94-98% of variables, and the dataset card brought Qwen3's multipliers to 100%. Sampling changes this: at
temperature 0.7, Llama 3.1's unit accuracy fell to 0.71 and its multiplier accuracy on scaled units to 0.69,
while Qwen3 stayed at 0.96 and 0.97. A pipeline should therefore decode deterministically and check units
against the schema's quantity kinds. Top-codes and missing codes are the silent risk: they are wrong for half
of the variables or more even with the card (Table 7), and only a stated convention enforced by a check
prevents them.

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

## 8. Discussion

**What makes a schema AI-ready.** Three results generalize beyond this case. First, definitions are the active
ingredient. They produced about four-fifths of the gain of full concept cards at half the tokens (E1), and
documentation borrowed from other standards helped exactly as far as it contained definitions (E6). Second,
some knowledge cannot be inferred from a record however capable the model is. Which variable an imputation
flag refers to, or which codes mean "not applicable", are publisher conventions, and only stating them in the
schema made them available (E3). Third, structural properties act as guarantees rather than as accuracy
gains. A closed vocabulary did not change accuracy but removed invented identifiers (E2), and quantity kinds
caught up to a fifth of wrong mappings at no cost (E4). Retrieval (E5) is a necessity for large vocabularies
rather than an improvement, and its recall bounds what the model can achieve. Taken together, the experiments suggest a checklist for
anyone designing a domain schema that AI systems will use:

1. Write a definition for every class, field, value and concept that can be applied without other context;
   labels are not enough.
2. Publish the closed vocabularies as a JSON Schema that can constrain generation.
3. Move conventions out of user guides into the schema, as structured rules with examples.
4. Give quantities their units and quantity kinds so that inconsistent output can be detected automatically.
5. Keep each unit of documentation self-contained and small, and measure the token cost of the whole.
6. Link to the domain's standards rather than replacing them, and verify every link.
7. Generate all of the above from one source, so that what people review is what AI systems read.

**Domain fidelity is not traded for AI-readiness.** Every artifact the models received is generated from the
same source that people review, and every property that helped the models (definitions, closed facets,
stated conventions, quantity kinds) is also something a careful human reader needs. The schema encodes
distinctions that a generic dataset vocabulary lacks, such as survey weights, imputation flags and
top-codes, and these are precisely the distinctions whose loss is most expensive downstream (Section 7).
AI-readiness, in this sense, is domain knowledge written down completely enough that a reader without
context can apply it.

**Implications for UBEM.** Data publishers can make their releases far easier to integrate, by people or by
AI, by stating conventions and weights in machine-readable profiles; one profile per dataset removes errors
that no model can avoid. Modelers can run small local models for a first pass and route disagreements to a
person. And the field needs identifiers more than more datasets: without them, characteristics and energy
can be joined to buildings only statistically.

**Limitations.** (1) The mapping gold was built by LLM annotators and was not audited by domain experts. Their
agreement was high, and the conclusions hold under four label sets, but absolute accuracies could change
under expert labels; the rationales and an audit sheet are released for that check. (2) Only two small
open-weight models were tested; larger models will likely score higher, and our claims concern the relative
value of schema properties, which held for both. (3) The experiments use two U.S. surveys; codebooks in
other languages and administrative registers may behave differently. (4) The documentation transplant gives
other standards the same concept ids and therefore measures their documentation, not their structure. (5)
The catalog is a purposive sample drafted with an LLM; its verified error rate is 2% wrong and 16% partly
correct fields. (6) The vocabulary is version 0.1; annotators found topics it lacks (energy insecurity,
electric vehicles, outages, internet access), which version 0.2 should add.

## 9. Conclusions

Generative AI now reads schemas, but schemas are still written for people. We defined an AI-ready schema as
one whose artifacts let an AI system understand, produce and check data descriptions without human
explanation while remaining a faithful encoding of domain knowledge, derived six design principles, and
built Meta-Urban 2.0 for open urban building energy data by them. Tested on two national building energy
surveys with two local language models, definitions were the property that mattered most. They raised top-1 mapping accuracy from
0.42-0.43 to 0.53-0.55, and full concept cards to 0.55-0.59, while documentation borrowed from standards that
give labels without definitions did no better than bare identifiers. Stated conventions supplied what no model
could infer from a record: the variable each commercial-survey imputation flag refers to went from 0% to 100%
correct. A closed vocabulary removed invented identifiers without costing accuracy, and quantity-kind rules
flagged up to a fifth of wrong mappings without a model call. The same schema, applied to a
verified catalog of 91 open datasets, shows that only 3 of 48 non-geometric building datasets can be linked
to individual buildings, and a reference pipeline shows that the errors AI systems still make, such as a
dropped unit multiplier or ignored survey weights, change UBEM results by up to three orders of magnitude.
The recommendation is to design domain schemas for both audiences from one source: define every term, close
the vocabularies, state the conventions, make output checkable, keep the documentation modular, and link to
existing standards. The schema, its AI documentation layer, the catalog, the benchmark and all model outputs
are open.

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
