[Date]

Editor-in-Chief
*Advanced Engineering Informatics*

Dear Editor,

We submit the manuscript "Does domain semantics help large language models integrate open data for urban
building energy modeling? The Meta-Urban schema, a verified open-data catalog, and a reproducible alignment
benchmark" for consideration as a research article in *Advanced Engineering Informatics*.

Urban building energy modeling (UBEM) combines weather, building geometry, building characteristics, operation
and measured energy from many open sources, and integrating them is still largely manual. LLMs are an obvious
way to automate it, but there is no machine-actionable target to align to and no evidence that a domain
schema, rather than the model, drives accuracy. The paper addresses both, which we believe fits the journal's
focus on knowledge representation and AI for engineering data:

1. **A schema and vocabulary.** Meta-Urban 2.0 is a LinkML schema (compiled to JSON Schema, SHACL and OWL)
   with a dataset level that profiles DCAT 3 using six UBEM facets, and a variable level that records concept,
   unit, code list, survey weights and imputation flags. It comes with an 81-concept SKOS vocabulary with verified
   mappings to Brick, BEDES and the CityGML Energy ADE.
2. **A verified catalog and a new linkage indicator.** Of 91 open datasets, only 3 of 48 that carry
   characteristics, operation, energy or simulation data share an identifier with building footprints.
3. **A controlled benchmark.** On 2,048 variables of two national surveys, we vary the schema context given
   to two locally run LLMs over five repeats, with blind double-annotated gold labels. Concept definitions,
   not labels, raise top-1 accuracy by 12 to 17 points; retrieval cuts cost by 82%; and agreement between
   runs is a better routing signal for human review than self-consistency.
4. **Downstream consequences.** A reference pipeline reproduces the publisher's totals within 0.01%, and
   each class of alignment error is traced to its effect on UBEM quantities; ignoring survey weights biases
   energy use intensity by -16% to +102% across building types.

All code, the schema, the catalog, gold labels, prompts and every model output are openly available, and every
number in the paper is regenerated from the repository.

An earlier and substantially different version of this work was posted as a preprint (arXiv:2311.08535).
The present manuscript replaces it: the taxonomy, schema, catalog, benchmark and downstream analysis are new,
and the preprint's demonstrations are re-examined in Section 6.4. The manuscript is not under consideration
elsewhere. As required by the journal, the use of generative AI in the research and writing process is
declared in the manuscript.

[Optional: suggested reviewers with affiliations and emails.]

Sincerely,

Liang Zhang, on behalf of all authors
University of Arizona
