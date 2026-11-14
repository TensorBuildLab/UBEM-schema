[Date]

Editor-in-Chief
*Energy*

Dear Editor,

We submit the manuscript "Meta-Urban: an AI-ready semantic schema for integrating open data in urban building
energy modeling" for consideration as a research article in *Energy*.

Urban building energy modeling (UBEM) supports city decarbonization plans, building performance standards
and grid planning, and it depends on combining open weather, geometry, survey and meter data. That
integration is still largely manual and is increasingly delegated to generative artificial intelligence (AI),
yet the schemas describing building energy data are written for human readers, and nobody has shown whether
AI-assisted integration gets the energy numbers right. The paper asks whether a UBEM data schema can be
designed so that generative AI integrates open building energy data correctly, and whether the difference
reaches the energy results.

The main findings are:

1. **Meta-Urban 2.0**, an AI-ready schema for open UBEM data: a dataset level, a variable level (units,
   codes, survey weights, imputation flags) and an 81-concept vocabulary with 168 verified links to Brick,
   BEDES and the CityGML Energy ADE, compiled from one source into documentation for people and into context
   cards, JSON Schema and SHACL shapes for AI. Applied to a verified catalog of 91 open datasets, it shows
   that only 3 of 48 non-geometric building datasets can be linked to individual buildings.
2. **Which schema properties matter**, from controlled experiments on the 2018 CBECS and 2020 RECS with two
   locally run language models: concept definitions raise mapping accuracy from 0.42-0.43 to 0.53-0.55
   (p < 0.001); stated publisher conventions supply what no model can infer from a record; and documentation
   borrowed from Brick, BEDES or the Energy ADE helps only where those standards define their terms.
3. **Effect on energy results.** AI-built variable profiles drive a national building-stock pipeline that
   reproduces EIA's published totals. Most indicators are reproduced exactly, but the remaining errors change
   indicators such as commercial electricity use intensity by up to a factor of 1,000 and residential gas use
   per household by 65%. Simple rules derived from the schema flag every such error, with no false alarms.

All code, the schema and its AI documentation layer, the catalog, gold labels, prompts and every model output
are openly available, and every number in the paper is regenerated from the repository.

An earlier and substantially different version of this work was posted as a preprint (arXiv:2311.08535). The
present manuscript replaces it: the schema, the catalog, the experiments and the energy analysis are new. The
manuscript is not under consideration elsewhere. The use of generative AI in the research and writing
process is declared in the manuscript.

[Optional: suggested reviewers with affiliations and emails.]

Sincerely,

Liang Zhang, on behalf of all authors
University of Arizona
