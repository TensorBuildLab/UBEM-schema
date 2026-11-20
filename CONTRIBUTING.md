# Contributing to UBEM-Link

Contributions are welcome: new datasets for the catalog, corrections to existing entries, concepts, mappings to
other standards, units, codebook readers, and fixes to the tool.

1. Open an issue describing the change (for a new dataset: its publisher page; for a schema change: the use case).
2. Make the change on a branch. Follow `docs/tutorials/05-extend-the-schema.md` for schema, vocabulary and catalog
   changes, and regenerate the artifacts it lists.
3. Run `python -m ubem_link.validate` and `pytest -q`; both must pass.
4. Open a pull request; add a line to `CHANGELOG.md`.

Catalog entries state only what the publisher or a peer-reviewed descriptor states. Every new class, field, value
and concept needs a definition that a person or an AI system can apply without other context.

By contributing you agree that code is released under the MIT License and schema, vocabulary and catalog content
under CC BY 4.0.
