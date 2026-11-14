# Meta-Urban 2.0: schema card for AI systems

Purpose: describe open datasets for urban building energy modeling (UBEM) so that they can be found, judged and joined, and describe their variables so that values are interpreted correctly. Use only the fields and values defined here; write null when the source does not state a value; never guess.

## DatasetProfile
Dataset-level description of one open dataset, sufficient to decide whether and how it can feed a UBEM workflow, and to join it with other datasets.
- id (string, required): Stable lowercase identifier of the record (letters, digits, '_', '.', '-').
- title (string, required): Full title of the dataset as given by its publisher.
- short_name (string): Common short name or acronym of the dataset (for example CBECS 2018).
- publisher (string): Organization that publishes and maintains the dataset.
- landing_page (uri): Web page of the dataset maintained by the publisher.
- doi (string): DOI of the dataset itself (bare form, e.g. 10.1234/abc).
- citation (string): Citation text the publisher asks users to give.
- reference_paper_doi (string): DOI of a peer-reviewed paper that describes the dataset.
- license (string): License or terms of use, as stated by the publisher (SPDX identifier where one exists).
- access_level (AccessLevel, required): How the data can be obtained, from open download to restricted or commercial access.
    - open_download: Files can be downloaded by anyone without registration.
    - open_api: Data can be retrieved by anyone through an open programmatic interface.
    - registration_required: Free, but users must register or sign in.
    - request_or_agreement: Access requires an application, a data-use agreement or approval.
    - restricted_commercial: Access requires payment or is restricted to specific users.
- distributions (Distribution, list): The downloadable files or services through which the data are released.
- ubem_roles (UBEMRole, required, list): UBEM workflow steps the dataset feeds; first value is the primary role.
    - boundary_conditions: Weather and climate drivers (observed, reanalysis, typical-year, projections).
    - geometry_inventory: Location and shape of buildings (footprints, heights, 3D models, parcels).
    - building_characteristics: Non-geometric attributes (use type, vintage, envelope, systems, fuels, floor area).
    - operation_use: Occupancy, schedules, occupant behavior, setpoints, plug loads.
    - calibration_validation: Measured or reported energy use at any scale.
    - reference_simulation: Synthetic building-stock model outputs and model libraries.
    - context_coupling: Socio-economic, land use, grid emissions, tariffs, urban microclimate.
- content_types (string, list): Kinds of content in the dataset (for example footprints, microdata, hourly loads).
- geographic_scope (GeographicScope): Extent of the area covered, from city to global.
    - global: Covers (nearly) the whole world.
    - multinational: Covers several countries, such as the European Union.
    - national: Covers one country.
    - subnational: Covers part of a country, such as a state, province or utility territory.
    - city: Covers one city or metropolitan area.
- spatial_coverage (SpatialCoverage): Area the dataset covers, as countries and optional regions.
- unit_of_observation (string): What one record describes (building, meter, household, station, grid_cell, region, person_day, ...).
- spatial_granularity (SpatialGranularity, required): Finest location detail released publicly.
    - point_station: Individual measurement points such as weather stations.
    - building: Individual buildings or footprints.
    - parcel: Individual land parcels or lots.
    - grid_cell_fine: Raster or model grid cells of 1 km or finer.
    - census_block_group: U.S. census block groups (about 600 to 3,000 people).
    - census_tract: U.S. census tracts (about 4,000 people).
    - postal_code: Postal or ZIP codes.
    - grid_cell_coarse: Raster or model grid cells coarser than 1 km.
    - county: Counties or equivalent second-level administrative units.
    - city: Cities or municipalities.
    - utility_service_territory: Service territories of electric or gas utilities.
    - state_province: States, provinces or equivalent first-level administrative units.
    - climate_zone: Climate zones (for example ASHRAE or IECC zones).
    - census_region_division: U.S. census regions or divisions.
    - nation: Whole countries, with no finer location.
    - none: No location released
    - unknown: Could not be verified from public documentation
- temporal_coverage (TemporalCoverage): Period the data describe.
- temporal_resolution (string): ISO 8601 duration of the finest time step, or "static" or "irregular".
- update_frequency (string): How often the publisher releases new data (for example annual, irregular).
- statistical_nature (StatisticalNature, required): How the data were generated, which decides how they may be analyzed (for example a weighted sample survey must be analyzed with its weights).
    - census_complete: Complete enumeration of a population.
    - sample_survey_weighted: Probability sample; estimates need weights.
    - administrative_record: Records created by an administrative process (certificates, permits, disclosure, utility filings).
    - measured_monitoring: Sensor or meter measurements.
    - remote_sensing_derived: Derived from satellite, aerial or lidar data with a model.
    - crowdsourced: Volunteered geographic information.
    - reanalysis_model: Model-data assimilation product.
    - typical_year_synthetic: Typical meteorological year assembled from observations.
    - climate_projection: Output of climate models under scenarios.
    - simulation_synthetic: Output of building energy simulation.
    - standard_or_code: A standard, dictionary, code or reference model rather than observations.
    - compilation: Assembled from several of the above.
- sampling_weights (string): Weight variables and how to use them (required for weighted sample surveys).
- conventions (Convention, list): Dataset-wide rules for naming, coding and units that apply to many variables.
- record_count (integer): Number of records (rows, buildings, meters or stations) in the dataset.
- record_count_note (string): What the record count counts and its source.
- join_keys (JoinKey, list): Keys present in the public data that allow records to be linked to other datasets.
    - lat_lon: Latitude and longitude of the record.
    - geometry: A point, line or polygon geometry of the record.
    - address: Street address of the building or site.
    - parcel_id: Cadastral parcel or lot identifier shared with other datasets (for example BBL).
    - building_id: Building identifier shared with other datasets (for example BIN, UPRN); not a dataset-internal row id.
    - ubid: Unique Building Identifier derived from the footprint.
    - station_id: Identifier of a weather or measurement station (for example WMO or USAF id).
    - grid_cell: Identifier or coordinates of a raster or grid cell.
    - census_block_group: U.S. census block group code.
    - census_tract: U.S. census tract code.
    - small_statistical_area: Non-U.S. small statistical areas such as UK LSOA/MSOA or national census grid ids
    - postal_code: Postal or ZIP code.
    - fips_county: U.S. FIPS county code.
    - fips_state: U.S. FIPS state code.
    - census_region_division: U.S. census region or division code.
    - nuts_region: European NUTS region code.
    - country_iso: ISO 3166 country code.
    - utility_id: Identifier of an electric or gas utility (for example EIA utility id).
    - balancing_authority: Identifier of an electricity balancing authority.
    - climate_zone_ashrae: ASHRAE Standard 169 climate zone.
    - climate_zone_iecc: IECC climate zone.
    - building_type: Building type or use class (attribute key for statistical matching only).
    - vintage: Construction period (attribute key for statistical matching only).
    - timestamp: Date and time of an observation.
- variables_documented (boolean): True if the publisher documents every variable (codebook or data dictionary).
- machine_readable (boolean): True if the data are released in a machine-readable format, not only as reports.
- versioned (boolean): True if the publisher identifies releases with versions.
- persistent_identifier (boolean): True if the dataset has a persistent identifier such as a DOI.
- known_limitations (string): Limitations a user must know before using the data (bias, coverage gaps, suppression).
- notes (string): Other information about the dataset or about how its profile was verified.
- verified (Verification): Provenance of the profile: who checked it, when and against which sources.
- variables (VariableProfile, list): Variable-level profiles of the dataset's columns.
- Rule: A weighted sample survey must name its weights.

## Distribution
One way of obtaining the data.
- format (string): File format or media type of a distribution (for example CSV, GeoParquet, NetCDF).
- access_url (string): URL from which a distribution can be accessed or downloaded.
- api (boolean): True if the distribution is a programmatic interface (API or web service) rather than a file.
- registration_required (boolean): True if users must register or sign in before downloading.

## SpatialCoverage
Geographic area a dataset covers.
- countries (string, list): ISO 3166-1 alpha-2 codes, or GLOBAL.
- description (string): Longer description of the variable, such as the question text.
- bbox (string): WGS84 bounding box "minLon,minLat,maxLon,maxLat" when meaningful.

## TemporalCoverage
Period of time a dataset covers.
- start (string): First period covered (ISO 8601 year, month or date).
- end (string): Last period covered (ISO 8601), or 'present' for an ongoing series.

## Convention
A rule the publisher applies to many variables at once, such as a naming pattern for imputation flags, a code that means "not applicable", or a unit used for all energy totals. Conventions are usually stated once in a user guide and never in the individual codebook entries, so a person or an AI system reading one entry cannot infer them; the profile states them explicitly.
- applies_to (string): Which variables the convention applies to (a name pattern or a description).
- rule (string, required): The convention, stated as a rule that can be applied without other context.
- example (string): One concrete example of the rule from the dataset.

## VariableProfile
Variable-level (column-level) semantics. One VariableProfile per column of a tabular dataset, or per variable of a gridded dataset.
- name (string, required): Variable name exactly as it appears in the data file.
- label (string): Short human-readable label of the variable as given in the codebook.
- description (string): Longer description of the variable, such as the question text.
- datatype (VariableDatatype): Data type of the variable's values.
    - integer: Whole numbers, such as counts or years.
    - float: Real numbers that may have decimals.
    - string: Free text without a code list.
    - categorical: Codes from a fixed list (see code_list).
    - boolean: True or false.
    - datetime: Dates or date-times (ISO 8601).
    - geometry: Spatial geometries such as points, lines or polygons.
    - identifier: Identifiers of records or entities.
- concept (string): Id of the UBEMConcept this variable maps to, or "none".
- mapping_relation (MappingRelation): SKOS relation between the variable and its concept (exact, close, broad, narrow, related).
    - exactMatch: The variable measures exactly the concept.
    - closeMatch: The variable measures nearly the concept and can be used in its place in most applications.
    - broadMatch: The concept is more general than the variable.
    - narrowMatch: The concept is more specific than the variable.
    - relatedMatch: The variable is associated with the concept but does not measure it.
- unit (string): QUDT unit CURIE, e.g. unit:FT2, unit:KiloBTU_IT, unit:KiloW-HR, unit:DEG_C.
- unit_multiplier (float): Factor applied to raw values before the unit applies (e.g., 1000 for "thousand Btu").
- aggregation (Aggregation): How each value relates to time: static, instantaneous, total or average over a period, count or share.
    - static: Attribute that does not vary in the observation period.
    - instantaneous: Value at a point in time (for example a temperature reading).
    - total_over_period: Sum over the reporting period (for example annual energy use).
    - average_over_period: Mean over the reporting period.
    - count: Number of items (for example number of floors or occupants).
    - share: Fraction or percentage of a whole.
- entity (EntityType): What the variable or concept describes (building, household, system, meter, region, ...).
    - site: A property or campus that may contain several buildings.
    - building: A single building.
    - zone: A thermal zone or space within a building.
    - system: A building system or piece of equipment (HVAC, water heating, lighting, ...).
    - envelope: Walls, roofs, windows and other parts of the building envelope.
    - household: A household occupying a housing unit.
    - occupant: A person using a building.
    - meter: An energy or water meter.
    - region: A geographic area.
    - weather_station: A weather or climate observation station.
    - grid_cell: A cell of a raster or model grid.
    - dataset_record: Record bookkeeping (identifiers, weights, flags).
- code_list (CodeEntry, list): Codes of a categorical variable with their meanings.
- missing_codes (string, list): Raw values that mean missing, not applicable, or suppressed.
- is_weight (boolean): True if the variable is a sampling or analysis weight; such variables are not observations.
- is_imputation_flag (boolean): True if the variable records whether another variable was imputed.
- flags_variable (string): For an imputation or quality flag, the variable it refers to.

## CodeEntry
One code of a categorical variable and its meaning.
- code (string): A value as stored in the data.
- label (string): Short human-readable label of the variable as given in the codebook.
- concept_value (string): Optional normalized value in the target concept (e.g., an ASHRAE climate zone id).

## Verification
Provenance of the profile itself (who checked it, when, against which sources).
- date (string): Date of the verification (ISO 8601).
- by (string): Person or agent who carried out the verification.
- sources_checked (uri, list): Pages and documents consulted during verification.

## Worked example (dataset level)
# 2018 Commercial Buildings Energy Consumption Survey (CBECS) public-use microdata (chr-cbecs-2018)
- UBEM workflow roles: building_characteristics, calibration_validation
- Statistical nature: sample_survey_weighted
- Finest public spatial granularity: census_region_division
- Temporal resolution: P1Y
- Access: open_download
- Join keys: census_region_division, building_type
- License: US-Government-Public-Domain
- Survey weights: FINALWT plus 151 replicate weights (FINALWT1-FINALWT151); variable names confirmed in the public CSV header
- Conventions (apply to many variables; individual codebook entries do not repeat them):
  - variables whose name starts with Z: Z<NAME> is the imputation flag for the variable <NAME>; codes 0 = reported, 1 = imputed, 9 = inapplicable. Example: ZMONUSE flags MONUSE (months in use).
  - FINALWT, FINALWT1 to FINALWT151: FINALWT is the final analysis weight and FINALWT1 to FINALWT151 are replicate weights for variance estimation; weights are not observations and every estimate must be weighted by FINALWT. Example: The sum of FINALWT over all records estimates the number of U.S. commercial buildings.
  - categorical and numeric variables with "Missing=Not applicable" in the codebook: A blank cell means not applicable (the question was not asked); record it as a missing code "". Example: RENADD (addition or annex) is coded 1 = Yes, 2 = No, Missing = Not applicable.
  - yes/no questions that offer "Don't know": Code 5 means "Don't know" and is a missing code, not a category. Example: DRVTHRU 5 = Don't know.
  - count and category variables with codes in the 990s, and code 7 in PUBCLIM: Codes 994 and 995 are top-codes (ranges), not numbers; codes such as 996 and PUBCLIM 7 mark values withheld to protect confidentiality and are missing codes. Example: NFLOOR 994 = 10 to 14 floors and 995 = 15 or more floors; NOCCAT 996 = withheld.
  - energy consumption and expenditure variables: Energy is reported in thousand Btu ("thous Btu", multiply by 1,000 for Btu), natural gas volumes in hundred cubic feet (multiply by 100), floor area in square feet and expenditures in U.S. dollars. Example: MFBTU is annual major-fuel consumption in thousand Btu.
