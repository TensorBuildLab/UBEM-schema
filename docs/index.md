# UBEM-Link

UBEM-Link is an open, AI-ready schema for the open data used in urban building energy modeling (UBEM), with a
catalog of open datasets and a tool that turns a dataset and its codebook into a checked, joinable UBEM input.
It plays for open UBEM data the role that Brick and Project Haystack play for building operational data: a
shared vocabulary with definitions, machine-readable constraints and tooling around it.

## What it describes

| Layer | Describes | Where |
|---|---|---|
| Taxonomy and facets | which UBEM input a dataset serves, how it was generated, how fine and how linkable it is | [Taxonomy](taxonomy.md) |
| Category profiles | the facts a modeler needs about weather, geometry, operation, characteristics, energy, simulation and context data | [Category profiles](category-profiles.md) |
| Variable profiles | what each column means: concept, unit, multiplier, missing codes, code list, weight or flag, join key | [Reference](reference/index.md) |
| Concept vocabulary | 73 concepts with definitions, canonical units and links to Brick, BEDES and the CityGML Energy ADE | [Vocabulary](vocabulary.md) |
| Conventions | rules a publisher states once for many columns, with a machine-readable scope | [Reference: Convention](reference/Convention.md) |
| Catalog | 93 open datasets profiled with the schema | [Catalog](catalog.md) |

## What it gives you

- **For people:** the schema in YAML, generated documentation, an OWL ontology, and SSSOM mappings to other
  standards (`schema/mappings/ubem_link.sssom.tsv`).
- **For software:** JSON Schema and SHACL shapes to validate profiles, a QUDT unit vocabulary with conversion
  factors (`schema/vocab/units.yaml`), and a Python package.
- **For AI systems:** a schema card, one card per concept and one card per dataset, each sized for a context
  window (`schema/ai/`), and JSON Schemas that constrain a model's output to valid values.
- **The `ubem-link` tool:** describe a new dataset with a local or hosted language model, review the flagged
  columns, apply the profile to the data, and integrate several datasets into one table. See [The tool](tool.md).

## Start here

1. [Quickstart](tutorials/01-quickstart.md): profile New York City building footprints with a local model.
2. [Survey microdata and codebooks](tutorials/02-survey-codebook.md): weights, imputation flags and conventions.
3. [Integrate city data](tutorials/03-integrate-city-data.md): benchmarking, tax lots, footprints and weather.
4. [Assistants and APIs](tutorials/04-assistants-and-apis.md): Claude Code, chat assistants, hosted models.
5. [Extend the schema](tutorials/05-extend-the-schema.md): add a concept, a dataset or a convention.
