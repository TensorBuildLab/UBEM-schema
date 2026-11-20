# Tutorial 5: extend the schema, the vocabulary or the catalog

UBEM-Link is versioned and open to contributions in the same way as Brick or BuildingSync: propose a change in an
issue or a pull request, keep the generated artifacts in sync, and keep the tests passing.

## Add a dataset to the catalog

1. Copy `catalog/TEMPLATE.yaml` to `catalog/datasets/<role prefix>-<name>.yaml` (prefixes: `wx`, `geo`, `chr`,
   `occ`, `nrg`, `sim`, `ctx`).
2. Fill the dataset-level facts from the publisher's pages only; write `null` where a fact is not stated.
3. Add one category profile per role (`weather_profile`, `geometry_profile`, ...; see
   [Category profiles](../category-profiles.md)).
4. State the publisher's conventions with a scope (`applies_to_variables` or `applies_to_pattern`) and, where
   they fix a value, the value (`missing_codes`, `unit`, `unit_multiplier`). `ubem-link conventions` can draft them
   from a user guide.
5. Run `python -m ubem_link.validate` and `python -m ubem_link.ai_docs` (regenerates the dataset cards).

## Add a concept

1. Add it to `schema/vocab/ubem_concepts.yaml` under its group, with a definition written so that a person or a
   model can apply it without other context, the entity it describes, its quantity kind and canonical unit, and
   generic synonyms.
2. Write the definition for the integration task. In the paper a key described as an identifier "within the
   dataset" led both models to an internal row identifier; describing it as a shared parcel identifier led them to
   the tax-lot key.
3. Add mappings to other standards in `schema/vocab/mappings_*.csv` (check that each target exists in the release
   file) and run `python scripts/make_sssom.py`.
4. Run `python -m ubem_link.ai_docs` and `python scripts/make_docs.py`.

## Add a field or a value to the schema

1. Edit `schema/ubem_link.yaml`; every class, field and value needs a description.
2. Regenerate the artifacts:

```bash
pip install -e ".[schema]"
gen-json-schema schema/ubem_link.yaml > schema/generated/ubem_link.schema.json
gen-shacl schema/ubem_link.yaml > schema/generated/ubem_link.shacl.ttl
gen-owl schema/ubem_link.yaml > schema/generated/ubem_link.owl.ttl
gen-python schema/ubem_link.yaml > src/ubem_link/datamodel.py
gen-doc schema/ubem_link.yaml -d docs/reference
python -m ubem_link.ai_docs && python scripts/make_docs.py && pytest -q
```

3. Add a line to `CHANGELOG.md`. Changes that remove or rename a field or value need a major version.

## Add a unit

Add it to `schema/vocab/units.yaml` with its QUDT id, quantity kind, factor (and offset) to the canonical unit,
and the words that name it in documentation. The tool offers every unit of this file to the model, so a source's
own unit can be recorded as published.
