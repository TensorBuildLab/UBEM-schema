# Taxonomy of open UBEM data

UBEM-Link classifies open data by the input of urban building energy modeling (UBEM) it serves. The
classification extends an earlier taxonomy of open data for physics-based UBEM (Zhang, Chen and Zou, 2023,
arXiv:2311.08535), which sorted open data into seven categories and listed, for each, the metadata a modeler
needs. UBEM-Link keeps those categories as the user-facing entry point and makes them machine-checkable.

## From seven categories to roles and facets

The earlier taxonomy mixed three kinds of distinction in one list: what a dataset is used for (weather,
geometry, characteristics), how fine it is (macroscopic versus microscopic energy data) and how it is assembled (a
data lake that combines sources). UBEM-Link separates them into independent facets, so that every dataset is one
point in a six-dimensional space and gaps can be counted along each facet.

| 2023 category | UBEM-Link role (`ubem_roles`) | Other facets that carry the distinction | Category profile |
|---|---|---|---|
| 1. Weather information | `boundary_conditions` | `statistical_nature` separates observations, reanalyses, typical years and projections | `WeatherProfile` |
| 2. Building stock GIS information | `geometry_inventory` | `spatial_granularity` (building, parcel, grid) | `GeometryProfile` |
| 3. Occupant behavior | `operation_use` | `unit_of_observation` (person, household, building) | `OperationProfile` |
| 4. Building characteristics | `building_characteristics` | `statistical_nature` separates surveys, administrative records and standards | `CharacteristicsProfile` |
| 5. Macroscopic energy data | `calibration_validation` | `energy_data_scale: macroscopic`; `spatial_granularity` coarser than a building | `EnergyProfile` |
| 6. Microscopic energy data | `calibration_validation` | `energy_data_scale: microscopic`; `spatial_granularity` building or finer | `EnergyProfile` |
| 7. Comprehensive data lake | (none: a collection, not a kind of data) | `statistical_nature: compilation`; a `Catalog` of profiles | (the entries it contains) |
| (added) | `reference_simulation` | synthetic building-stock outputs and prototype models | `SimulationProfile` |
| (added) | `context_coupling` | land use, socio-economic data, grid emissions, tariffs | `ContextProfile` |

The two added roles cover datasets found while cataloging that fit none of the seven categories: simulated
building stocks (ResStock, ComStock) and context data used to couple UBEM with other models.

## The six facets

| Facet | Values |
|---|---|
| UBEM workflow role | the seven roles above; the first listed is the primary role |
| Statistical nature | census; weighted sample survey; administrative record; measured monitoring; remote-sensing derived; crowdsourced; reanalysis; typical year; climate projection; simulation; standard or code; compilation |
| Spatial granularity | 15 ranked levels from point or building to nation, plus none and unknown |
| Temporal resolution | ISO 8601 duration, static, or irregular |
| Access | open download; open API; free registration; request or agreement; restricted or commercial |
| Join keys | 24 key types, from building and parcel identifiers to census geographies, grid cells, climate zones and timestamps |

## From a metadata table to category profiles

For each category, the 2023 taxonomy listed the information a modeler needs in a table of free-text notes (for
example, "Timestamp format: e.g., HH:MM:SS MM/DD/YYYY" or "AMY/TMY/Others"). UBEM-Link turns each row into a typed
field with a closed list of values, adds what integration showed to be missing, and corrects one definition:

| Category | Kept from 2023 (now typed) | Added |
|---|---|---|
| Weather | year type (AMY, TMY, others), EPW or not (now a format list), interval and timestamp format (now ISO 8601 resolution), interpolation, location, variable list (now concept ids) | timestamp convention (interval ending or beginning), clock (UTC or local standard time), grid resolution, station id scheme, climate scenarios |
| Building stock GIS | resolution (now spatial granularity), 2D or 3D (now a geometry dimension), data format, level of detail | height source and reference, coordinate reference system and its linear unit, building id scheme, capture threshold |
| Occupant behavior | building type, behavior type, control action, behavior factors (now concept ids), timestamp and interval | collection method |
| Building characteristics | sample or probability (now data form: microdata, building records, aggregate tables, dictionary, archetype library), characteristics list (now concept ids), joint distribution list (now cross-tabulations) | representativeness (probability sample, mandated subset, ...), coverage threshold |
| Macroscopic and microscopic energy | sector, time series and interval, interpolation, energy data list (now carriers and metrics), geographic information (now join keys), existing metadata schema (now `metadata_standards`) | energy data scale, metering level, measurement basis, weather-normalized values, reporting period |

The 2023 table described CityGML levels of detail as "LoD1: simple 2-D footprint, LoD2: a box shape"; UBEM-Link
uses the CityGML definitions (LoD0 footprint, LoD1 block model, LoD2 roof shapes, LoD3 openings, LoD4 interiors).

The field-by-field reference, generated from the schema, is in [Category profiles](category-profiles.md).

## Why the classification matters for integration

A category profile states the facts that decide whether two datasets can be combined and how: whether weather
timestamps mark the end or the start of an hour, whether heights are in feet above ground or metres above sea
level, whether a characteristics dataset is a probability sample or covers only buildings above a size threshold,
whether energy is metered or self-reported. In the New York City case of the paper, the footprints' heights are
in feet and their system-generated areas are computed in Web Mercator (1.74 times the true area at that
latitude); both facts are in the publisher's metadata page, not in the portal's column descriptions, and both
are recorded in the footprint entry so that tools apply them.
