[Date]

Dear Editor,

We submit the manuscript "Meta-Urban: an AI-ready semantic schema for integrating open data in urban building
energy modeling" for consideration as a research article in *Computers, Environment and Urban Systems*.

Computational models of cities depend on integrating heterogeneous open data, and urban building energy
modeling (UBEM), which supports city decarbonization plans, building performance standards and grid planning,
is among the most demanding cases: it combines weather, geometry, survey and meter data. That integration is
still largely manual and is increasingly delegated to generative artificial intelligence (AI), yet the schemas
describing urban data are written for human readers, and there is little evidence on whether AI-assisted
integration gets the results right. The paper asks which properties of a data schema help locally run language
models integrate open building energy data, and whether the errors that remain reach national and city-scale
energy indicators.

The work fits *Computers, Environment and Urban Systems* because it contributes a computational method for
urban data infrastructure and tests it on a city-scale integration task. It defines AI-ready schemas, states
six design principles with measurable criteria and tests them in controlled experiments on two national
building energy surveys; it applies the schema to a catalog of 91 open datasets, in which only 3 of 48
non-geometric building datasets share an identifier with building footprints or parcels; and it lets the
models integrate New York City's energy benchmarking disclosures with tax-lot data, choosing the columns and
building the unit and missing-code profiles themselves, and maps the effect on energy use intensity by
community district. With the schema's definitions the models chose the right columns more often, yet both read kBtu as kilowatt-hours, overstating city-wide energy use intensity by 215%, and a plausible floor-area choice biased district intensity by up to 21% while changing the city-wide value by only 2%. Profile checks derived from the schema caught most of these errors but were precise only when they knew the source's missing-value convention.

The manuscript is not under consideration elsewhere, and the authors declare that they have no known competing
financial interests or personal relationships that could have appeared to influence the work reported in this
paper.

Sincerely,

Liang Zhang\
Assistant Professor\
University of Arizona\
liangzhang1@arizona.edu
