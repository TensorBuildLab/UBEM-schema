# UBEM-Link metadata schema for open data in urban building energy modeling

UBEM-Link describes open datasets used in urban building energy modeling (UBEM) at two levels. The dataset level (DatasetProfile) is an application profile of W3C DCAT 3 with UBEM-specific facets: the UBEM workflow role, statistical nature, spatial granularity, temporal resolution, access level and join keys. The variable level (VariableProfile) records what each column means for UBEM: the concept it maps to in the UBEM-Link vocabulary, its unit (QUDT), its code list, its aggregation semantics, and whether it is a survey weight or an imputation flag. Concepts (UBEMConcept) form a SKOS hierarchy and carry mappings to BEDES, Brick, CityGML Energy ADE and EnergyPlus input objects. Between the two levels, one category profile per UBEM workflow role (WeatherProfile, GeometryProfile, OperationProfile, CharacteristicsProfile, EnergyProfile, SimulationProfile, ContextProfile) records what a modeler must know about that kind of data. The roles and category profiles refine an earlier seven-category taxonomy of open UBEM data (weather information; building stock GIS; occupant behavior; building characteristics; macroscopic energy; microscopic energy; comprehensive data lakes) and its per-category metadata table.

URI: https://w3id.org/ubem-link/schema

Name: ubem_link



## Classes

| Class | Description |
| --- | --- |
| [Catalog](Catalog.md) | A collection of dataset profiles and the concept vocabulary they refer to |
| [CategoryProfile](CategoryProfile.md) | Category-specific part of a dataset profile: what a modeler must know about o... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[CharacteristicsProfile](CharacteristicsProfile.md) | Non-geometric building characteristics (use type, vintage, envelope, systems,... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ContextProfile](ContextProfile.md) | Context and coupling data: socio-economic data, land use, grid emissions, tar... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[EnergyProfile](EnergyProfile.md) | Measured or reported energy use for calibration and validation, from national... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[GeometryProfile](GeometryProfile.md) | Building stock geometry and inventory: footprints, heights, 3D city models an... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[OperationProfile](OperationProfile.md) | Occupancy, occupant behavior, schedules, setpoints and time use |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[SimulationProfile](SimulationProfile.md) | Reference simulations and model libraries: synthetic building-stock outputs a... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[WeatherProfile](WeatherProfile.md) | Weather and climate data used as boundary conditions: observed station record... |
| [CodeEntry](CodeEntry.md) | One code of a categorical variable and its meaning |
| [Convention](Convention.md) | A rule the publisher applies to many variables at once, such as a naming patt... |
| [DatasetProfile](DatasetProfile.md) | Dataset-level description of one open dataset, sufficient to decide whether a... |
| [Distribution](Distribution.md) | One way of obtaining the data |
| [SpatialCoverage](SpatialCoverage.md) | Geographic area a dataset covers |
| [TemporalCoverage](TemporalCoverage.md) | Period of time a dataset covers |
| [UBEMConcept](UBEMConcept.md) | A concept in the UBEM-Link vocabulary: a quantity or attribute that a UBEM wo... |
| [VariableProfile](VariableProfile.md) | Variable-level (column-level) semantics |
| [Verification](Verification.md) | Provenance of the profile itself (who checked it, when, against which sources... |



## Slots

| Slot | Description |
| --- | --- |
| [access_level](access_level.md) | How the data can be obtained, from open download to restricted or commercial ... |
| [access_url](access_url.md) | URL from which a distribution can be accessed or downloaded |
| [aggregation](aggregation.md) | How each value relates to time: static, instantaneous, total or average over ... |
| [alt_labels](alt_labels.md) | Generic synonyms of the concept |
| [api](api.md) | True if the distribution is a programmatic interface (API or web service) rat... |
| [applies_to](applies_to.md) | Which variables the convention applies to (a name pattern or a description) |
| [applies_to_codes](applies_to_codes.md) | Codes or code labels that must all occur in a variable's documented codes for... |
| [applies_to_pattern](applies_to_pattern.md) | Regular expression over variable names giving the variables a convention appl... |
| [applies_to_variables](applies_to_variables.md) | Exact names of the variables a convention applies to (machine-readable scope) |
| [bbox](bbox.md) | WGS84 bounding box "minLon,minLat,maxLon,maxLat" when meaningful |
| [behavior_types](behavior_types.md) | Kinds of occupant behavior or building operation recorded |
| [broad_match](broad_match.md) | Term in another standard that is more general (SKOS broadMatch) |
| [broader](broader.md) | The more general concept in the hierarchy (SKOS broader) |
| [building_id_scheme](building_id_scheme.md) | Building identifier system used (for example BIN, UPRN, BAG, UBID); null if n... |
| [building_sectors](building_sectors.md) | Building sectors covered |
| [by](by.md) | Person or agent who carried out the verification |
| [canonical_unit](canonical_unit.md) | SI (or SI-accepted) unit in which normalized values are expressed |
| [characteristics_profile](characteristics_profile.md) | Category profile for a dataset with the role building_characteristics |
| [citation](citation.md) | Citation text the publisher asks users to give |
| [climate_scenarios](climate_scenarios.md) | Emission or socio-economic scenarios of a projection (for example SSP2-4 |
| [close_match](close_match.md) | Term in another standard with nearly the same meaning (SKOS closeMatch) |
| [code](code.md) | A value as stored in the data |
| [code_list](code_list.md) | Codes of a categorical variable with their meanings |
| [collection_method](collection_method.md) | How the behavior or operation data were collected |
| [concept](concept.md) | Id of the UBEMConcept this variable maps to, or "none" |
| [concept_role](concept_role.md) | UBEM workflow role the concept belongs to |
| [concept_value](concept_value.md) | Optional normalized value in the target concept (e |
| [concepts](concepts.md) | Concepts of the vocabulary held in the catalog |
| [confidence](confidence.md) | Confidence of an automatically produced mapping, between 0 and 1 |
| [content_types](content_types.md) | Kinds of content in the dataset (for example footprints, microdata, hourly lo... |
| [context_kind](context_kind.md) | Kind of context or coupling data |
| [context_profile](context_profile.md) | Category profile for a dataset with the role context_coupling |
| [control_actions](control_actions.md) | Occupant control actions recorded |
| [convention_type](convention_type.md) | What the convention concerns, so that tools can apply it (missing codes, unit... |
| [conventions](conventions.md) | Dataset-wide rules for naming, coding and units that apply to many variables |
| [coordinate_reference_system](coordinate_reference_system.md) | Coordinate reference system of the published geometry, as an EPSG code (for e... |
| [countries](countries.md) | ISO 3166-1 alpha-2 codes, or GLOBAL |
| [coverage_threshold](coverage_threshold.md) | Size or other threshold that decides which buildings are covered (for example... |
| [cross_tabulations](cross_tabulations.md) | For aggregate tables, the joint distributions published, each as concept ids ... |
| [crs_linear_unit](crs_linear_unit.md) | Linear unit of the coordinate reference system and of lengths and areas deriv... |
| [data_form](data_form.md) | Whether the data are records of individual units (microdata or building recor... |
| [datasets](datasets.md) | Dataset profiles held in the catalog |
| [datatype](datatype.md) | Data type of the variable's values |
| [date](date.md) | Date of the verification (ISO 8601) |
| [definition](definition.md) | What the concept means, written so that a person or an AI system can apply it... |
| [description](description.md) | Longer description of the variable, such as the question text |
| [distributions](distributions.md) | The downloadable files or services through which the data are released |
| [do_not_use](do_not_use.md) | True if the publisher says the variable must not be used (the reason is in a ... |
| [doi](doi.md) | DOI of the dataset itself (bare form, e |
| [end](end.md) | Last period covered (ISO 8601), or 'present' for an ongoing series |
| [energy_carriers](energy_carriers.md) | Energy carriers reported |
| [energy_data_scale](energy_data_scale.md) | Macroscopic (aggregates over many buildings) or microscopic (buildings, meter... |
| [energy_metrics](energy_metrics.md) | Kinds of energy quantity reported |
| [energy_profile](energy_profile.md) | Category profile for a dataset with the role calibration_validation |
| [energy_sectors](energy_sectors.md) | Energy-using sectors covered |
| [entity](entity.md) | What the variable or concept describes (building, household, system, meter, r... |
| [exact_match](exact_match.md) | Term in another standard with the same meaning (SKOS exactMatch) |
| [example](example.md) | One concrete example of the rule from the dataset |
| [flags_variable](flags_variable.md) | For an imputation or quality flag, the variable it refers to |
| [format](format.md) | File format or media type of a distribution (for example CSV, GeoParquet, Net... |
| [gap_filling](gap_filling.md) | How missing or sub-interval values were filled by the publisher |
| [geographic_scope](geographic_scope.md) | Extent of the area covered, from city to global |
| [geometry_dimension](geometry_dimension.md) | Geometric representation of buildings, from points and footprints to 3D solid... |
| [geometry_profile](geometry_profile.md) | Category profile for a dataset with the role geometry_inventory |
| [grid_resolution_km](grid_resolution_km.md) | Horizontal resolution of a gridded product in kilometres |
| [height_reference](height_reference.md) | Reference points between which a building height is measured |
| [height_source](height_source.md) | How building heights were obtained |
| [id](id.md) | Stable lowercase identifier of the record (letters, digits, '_', ' |
| [is_imputation_flag](is_imputation_flag.md) | True if the variable records whether another variable was imputed |
| [is_replicate_weight](is_replicate_weight.md) | True if the variable is a replicate weight used to estimate sampling variance |
| [is_weight](is_weight.md) | True if the variable is a sampling or analysis weight; such variables are not... |
| [join_key](join_key.md) | Key type the variable holds, if it can link records to other datasets (for ex... |
| [join_keys](join_keys.md) | Keys present in the public data that allow records to be linked to other data... |
| [known_limitations](known_limitations.md) | Limitations a user must know before using the data (bias, coverage gaps, supp... |
| [label](label.md) | Short human-readable label of the variable as given in the codebook |
| [landing_page](landing_page.md) | Web page of the dataset maintained by the publisher |
| [levels_of_detail](levels_of_detail.md) | CityGML levels of detail provided |
| [license](license.md) | License or terms of use, as stated by the publisher (SPDX identifier where on... |
| [machine_readable](machine_readable.md) | True if the data are released in a machine-readable format, not only as repor... |
| [mapping_relation](mapping_relation.md) | SKOS relation between the variable and its concept (exact, close, broad, narr... |
| [measurement_basis](measurement_basis.md) | Whether values are metered, billed, self-reported or modeled |
| [metadata_standards](metadata_standards.md) | Metadata standards or schemas the publisher already uses (for example Brick, ... |
| [metering_level](metering_level.md) | Finest level at which energy is measured or reported |
| [minimum_building_size](minimum_building_size.md) | Capture threshold for buildings, as stated by the publisher (for example 'lar... |
| [missing_codes](missing_codes.md) | Raw values that mean missing, not applicable, or suppressed |
| [name](name.md) | Variable name exactly as it appears in the data file |
| [narrow_match](narrow_match.md) | Term in another standard that is more specific (SKOS narrowMatch) |
| [notes](notes.md) | Other information about the dataset or about how its profile was verified |
| [operation_profile](operation_profile.md) | Category profile for a dataset with the role operation_use |
| [persistent_identifier](persistent_identifier.md) | True if the dataset has a persistent identifier such as a DOI |
| [pref_label](pref_label.md) | Preferred human-readable label of the concept |
| [profiled_by](profiled_by.md) | Who or what produced this variable profile (a person, or a model id such as o... |
| [provides_concepts](provides_concepts.md) | Ids of the UBEM-Link concepts the dataset provides values for (its content at... |
| [publisher](publisher.md) | Organization that publishes and maintains the dataset |
| [quantity_kind](quantity_kind.md) | QUDT quantity kind CURIE, e |
| [record_count](record_count.md) | Number of records (rows, buildings, meters or stations) in the dataset |
| [record_count_note](record_count_note.md) | What the record count counts and its source |
| [reference_paper_doi](reference_paper_doi.md) | DOI of a peer-reviewed paper that describes the dataset |
| [registration_required](registration_required.md) | True if users must register or sign in before downloading |
| [related_match](related_match.md) | Term in another standard that is associated but not equivalent (SKOS relatedM... |
| [reporting_period](reporting_period.md) | Period one value covers (for example calendar year, billing month) |
| [representativeness](representativeness.md) | How the covered buildings relate to the building stock, which decides whether... |
| [review_flags](review_flags.md) | Reasons this profile should be reviewed by a person (failed checks, low confi... |
| [rule](rule.md) | The convention, stated as a rule that can be applied without other context |
| [sampling_weights](sampling_weights.md) | Weight variables and how to use them (required for weighted sample surveys) |
| [short_name](short_name.md) | Common short name or acronym of the dataset (for example CBECS 2018) |
| [simulation_engine](simulation_engine.md) | Simulation engine that produced the data (for example EnergyPlus) |
| [simulation_profile](simulation_profile.md) | Category profile for a dataset with the role reference_simulation |
| [sources_checked](sources_checked.md) | Pages and documents consulted during verification |
| [spatial_coverage](spatial_coverage.md) | Area the dataset covers, as countries and optional regions |
| [spatial_granularity](spatial_granularity.md) | Finest location detail released publicly |
| [start](start.md) | First period covered (ISO 8601 year, month or date) |
| [station_id_scheme](station_id_scheme.md) | Identifier system of the stations (for example WMO, USAF-WBAN, GHCN) |
| [statistical_nature](statistical_nature.md) | How the data were generated, which decides how they may be analyzed (for exam... |
| [stock_representation](stock_representation.md) | How the simulated building stock is represented |
| [temporal_coverage](temporal_coverage.md) | Period the data describe |
| [temporal_resolution](temporal_resolution.md) | ISO 8601 duration of the finest time step, or "static" or "irregular" |
| [time_basis](time_basis.md) | Clock to which timestamps refer (UTC, local standard time, or local time with... |
| [timestamp_convention](timestamp_convention.md) | Whether a timestamp marks the end, the start or the instant of the interval i... |
| [title](title.md) | Full title of the dataset as given by its publisher |
| [ubem_roles](ubem_roles.md) | UBEM workflow steps the dataset feeds; first value is the primary role |
| [unit](unit.md) | QUDT unit CURIE, e |
| [unit_multiplier](unit_multiplier.md) | Factor applied to raw values before the unit applies (e |
| [unit_of_observation](unit_of_observation.md) | What one record describes (building, meter, household, station, grid_cell, re... |
| [update_frequency](update_frequency.md) | How often the publisher releases new data (for example annual, irregular) |
| [variables](variables.md) | Variable-level profiles of the dataset's columns |
| [variables_documented](variables_documented.md) | True if the publisher documents every variable (codebook or data dictionary) |
| [verified](verified.md) | Provenance of the profile: who checked it, when and against which sources |
| [versioned](versioned.md) | True if the publisher identifies releases with versions |
| [weather_basis](weather_basis.md) | Weather used for the simulations (for example AMY 2018, TMY3) |
| [weather_file_format](weather_file_format.md) | Formats in which weather is released, which decide whether a simulation engin... |
| [weather_normalized_available](weather_normalized_available.md) | True if weather-normalized values are published alongside the actual ones |
| [weather_profile](weather_profile.md) | Category profile for a dataset with the role boundary_conditions |
| [weather_year_type](weather_year_type.md) | Kind of weather year or series: actual series, actual or typical meteorologic... |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [AccessLevel](AccessLevel.md) | How the data can be obtained |
| [Aggregation](Aggregation.md) | How a value relates to time |
| [BehaviorType](BehaviorType.md) | Kind of occupant behavior or building operation |
| [BuildingSector](BuildingSector.md) | Building sector |
| [CollectionMethod](CollectionMethod.md) | How behavior or operation data were collected |
| [ContextKind](ContextKind.md) | Kind of context or coupling data |
| [ControlAction](ControlAction.md) | Occupant control action |
| [ConventionType](ConventionType.md) | What a dataset convention concerns |
| [DataForm](DataForm.md) | Form in which characteristics are released |
| [EnergyCarrier](EnergyCarrier.md) | Energy carrier |
| [EnergyDataScale](EnergyDataScale.md) | Scale of energy data |
| [EnergyMetric](EnergyMetric.md) | Kind of energy quantity |
| [EnergySector](EnergySector.md) | Energy-using sector |
| [EntityType](EntityType.md) | What a concept or variable describes |
| [GapFilling](GapFilling.md) | How missing or sub-interval values were filled |
| [GeographicScope](GeographicScope.md) | Extent of the area a dataset covers |
| [GeometryDimension](GeometryDimension.md) | Geometric representation of buildings |
| [HeightReference](HeightReference.md) | Reference points of a building height |
| [HeightSource](HeightSource.md) | How building heights were obtained |
| [JoinKey](JoinKey.md) | Keys in the public data through which records can be linked to other datasets |
| [LevelOfDetail](LevelOfDetail.md) | CityGML level of detail |
| [MappingRelation](MappingRelation.md) | SKOS mapping relation between a variable and a concept |
| [MeasurementBasis](MeasurementBasis.md) | How energy values were obtained |
| [MeteringLevel](MeteringLevel.md) | Finest level at which energy is measured or reported |
| [Representativeness](Representativeness.md) | How the covered buildings relate to the building stock |
| [SpatialGranularity](SpatialGranularity.md) | Ordered from finest to coarsest (see `rank` annotation) |
| [StatisticalNature](StatisticalNature.md) | How the data were generated; decides the statistical treatment they need |
| [StockRepresentation](StockRepresentation.md) | How a simulated building stock is represented |
| [TimeBasis](TimeBasis.md) | Clock to which timestamps refer |
| [TimestampConvention](TimestampConvention.md) | What a timestamp marks within its interval |
| [UBEMRole](UBEMRole.md) | The UBEM workflow step a dataset or concept serves |
| [VariableDatatype](VariableDatatype.md) | Data type of a variable's values |
| [WeatherFileFormat](WeatherFileFormat.md) | Format of released weather data |
| [WeatherYearType](WeatherYearType.md) | Kind of weather year or weather series |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
