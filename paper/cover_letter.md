[Date]

Editor-in-Chief
*Engineering Applications of Artificial Intelligence*

Dear Editor,

We submit the manuscript "Meta-Urban: an AI-ready semantic schema for integrating open urban building energy
data with generative artificial intelligence" for consideration as an original research paper in
*Engineering Applications of Artificial Intelligence*.

Generative AI is now used to find, interpret and join engineering data, but the schemas through which such
data are described are still written for human readers. The paper asks whether a domain schema can be
designed to be AI-ready, so that a generative AI system can use it to integrate data correctly without a
person explaining it, while it remains a faithful encoding of domain knowledge, and which design properties
make the difference.

**AI contribution.** We define an AI-ready schema and derive six design principles: define every term, close
the vocabulary, state the conventions, make output checkable, fit the context window, and ground in domain
standards. Each principle is tested by a controlled experiment that changes one property of the schema and
holds everything else fixed, with two locally run open-weight language models, blind double-annotated labels,
exact significance tests and a label-sensitivity analysis. The experiments show that concept definitions
account for about four-fifths of the gain in mapping accuracy (0.42-0.43 to 0.55-0.59, p < 0.001); that
stated conventions supply knowledge no model can infer from a record (the variable an imputation flag
refers to: 0% to 100% correct); that a closed vocabulary removes invented identifiers without costing
accuracy; and that documentation borrowed from Brick, BEDES or the CityGML Energy ADE helps only where those
standards define their terms. The result is a checklist for designing domain schemas for AI use.

**Engineering application.** The principles are applied to urban building energy modeling, where combining
open weather, geometry, survey and meter data is still manual. Meta-Urban is a LinkML schema compiled from
one source into documentation for people and into context cards, JSON Schema and SHACL shapes for AI, with an
81-concept vocabulary linked to building standards. Applied to a verified catalog of 91 open datasets, it
shows that only 3 of 48 non-geometric building datasets can be linked to individual buildings, and a
reference pipeline shows that the AI errors that remain, such as a dropped unit multiplier or ignored survey
weights, change UBEM results by up to three orders of magnitude.

All code, the schema and its AI documentation layer, the catalog, gold labels, prompts and every model output
are openly available, and every number in the paper is regenerated from the repository.

An earlier and substantially different version of this work was posted as a preprint (arXiv:2311.08535).
The present manuscript replaces it: the AI-readiness framework, the schema, the catalog, the experiments and
the downstream analysis are new. The manuscript is not under consideration elsewhere. The use of generative
AI in the research and writing process is declared in the manuscript.

[Optional: suggested reviewers with affiliations and emails.]

Sincerely,

Liang Zhang, on behalf of all authors
University of Arizona
