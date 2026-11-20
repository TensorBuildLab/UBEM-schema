[Date]

Dear Editor,

We submit the manuscript "UBEM-Link: an AI-ready semantic schema for integrating open data in urban building
energy modeling" for consideration as a research article in *Computers, Environment and Urban Systems*.

Computational models of cities depend on integrating heterogeneous open data, and urban building energy modeling (UBEM), which supports city decarbonization plans, building performance standards and grid planning, is among the most demanding cases: it combines weather, building geometry, building characteristics, occupant behavior and measured energy use. That integration is still largely manual and is increasingly delegated to generative artificial intelligence (AI), yet the schemas describing urban data are written for human readers, and there is little evidence on whether AI-assisted integration gets the results right. The paper asks which properties of a data schema help locally run language models integrate open building energy data, and whether the errors that remain reach national and city-scale energy indicators.

The work fits *Computers, Environment and Urban Systems* because it contributes a computational method and open infrastructure for urban data and tests them on city-scale integration. It refines a taxonomy of open UBEM data into six facets and seven typed category profiles, implements them in a LinkML schema with a concept vocabulary and an open tool, and applies them to a catalog of 93 datasets, in which only 4 of 49 non-geometric building datasets share an identifier with footprints or parcels. Controlled experiments with local open-weight models show that concept definitions, not labels, make mapping possible, and that publisher conventions given to a model as prose are applied beyond their scope: in New York City, two models read kBtu as kilowatt-hours and overstated energy use intensity by 215%. With the source's units in the vocabulary and conventions applied by software, the same models reproduced an integration of benchmarking disclosures, tax lots, building footprints and weather files for 29,077 buildings exactly.

The taxonomy refined in Section 2 was first proposed in a preprint by the authors (arXiv:2311.08535), which is cited in the third person for anonymized review; the schema, tool, catalog, experiments and city-scale tests are new. The manuscript is not under consideration elsewhere, and the authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

Sincerely,

Liang Zhang\
Assistant Professor\
University of Arizona\
liangzhang1@arizona.edu
