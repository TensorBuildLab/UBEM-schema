# Changelog

UBEM-Link follows semantic versioning: a release that removes or renames a class, slot or enum value is a major
version; additions are minor versions.

## 1.0.0 (unreleased)

First release.

- Schema: dataset profile (DCAT 3 application profile with six UBEM facets), category profiles for weather,
  geometry, operation, characteristics, energy, simulation and context data, variable profile (CSVW column with
  concept, QUDT unit, multiplier, missing codes, code list, weight and flag roles, join key, provenance),
  conventions with machine-readable scopes (`applies_to_variables`, `applies_to_pattern`, `applies_to_codes`).
  The roles and category profiles refine the seven-category taxonomy of open UBEM data of Zhang, Chen and Zou
  (2023, arXiv:2311.08535).
- Vocabulary: 81 concepts (8 groups, 73 mapping targets) with definitions; 168 mappings to Brick 1.4.4, BEDES 2.5
  and the CityGML Energy ADE 1.0, published as SSSOM; unit vocabulary of 45 QUDT units with conversion factors.
- Catalog: 93 open datasets.
- Tool: `ubem-link` (describe, conventions, validate, apply, integrate, select, catalog, cards, pending) with
  Ollama, OpenAI-compatible, Anthropic and files backends.
- Generated artifacts: JSON Schema, SHACL, OWL, Python data model, documentation, AI documentation layer.

### Tool changes found in testing (before 1.0.0)

- Profile checks match unit words as whole words ("wh" no longer matches "which"); found in the four-source test of
  the paper, which reports the frozen and the fixed checks.
- New checks: a key column with few distinct values; a quantitative concept on a column without numeric values.
- Conventions can be scoped by code list (`applies_to_codes`), for rules that apply to, say, yes/no questions.
