---
title: "Supplementary material"
---


UBEM-Link: an AI-ready semantic schema for integrating open data in urban building energy modeling


## S1. Runs

The models (Qwen3 8B, Ollama tag qwen3:8b, digest 500a1f067a9f; Llama 3.1 8B, tag llama3.1:8b, digest 46e0c10c039e; Qwen3 14B, tag qwen3:14b, digest bdbd181c33f2, with partial CPU offload; all Q4_K_M quantization) were run through Ollama 0.40.16 on one NVIDIA GeForce RTX 3050 (8 GB), with an 8,192-token context, thinking disabled, seed equal to the run index, and output constrained by JSON Schema. Repeatability statistics use only the runs at T = 0.7.

| Task | Conditions | Temperature | Runs per item | Items |
|---|---|---|---|---|
| Mapping (T2) | L0, L1, L2, L3 | 0 and 0.7 | 1 at T = 0, 4 at T = 0.7 | 300 |
| Mapping (T2) | L2D, L2U, L2N, O0, O2D, XBR, XBE, XEA | 0 | 1 | 300 |
| Normalization (T3) | codebook entry only | 0 and 0.7 | 1 at T = 0, 2 at T = 0.7 | 390 |
| Normalization (T3P) | with the dataset card | 0 | 1 | 390 |
| National pipeline (E7) | entry only; with card | 0 and 0.7 | as T3/T3P | 11 |
| City case (E8): selection | L0, L2 | 0 | 1 | 6 concepts |
| City case (E8): normalization | entry only; with card | 0 | 1 | 4 to 5 columns |
| Four-source case (E8b): selection | L2 | 0 | 1 | 16 inputs |
| Four-source case (E8b): normalization | entry; card; scoped | 0 | 1 | 14 to 15 columns |
| Mapping, Qwen3 14B | L0, L1, L2D, L2, L3E | 0 | 1 | 300 |

## S2. Prompts

The system prompt carries the task and the schema artifacts; the user message carries the variable. Long vocabulary blocks are shortened here to their first lines; the full prompts of every call are in the released cache.

### Mapping, condition L0

```
You are an expert in urban building energy modeling (UBEM) and in building energy survey data. Answer with one JSON object that follows the required schema.

Task: map one survey variable to the single most specific concept in the target vocabulary that the variable measures or records. Answer "none" if no concept applies.

TARGET VOCABULARY
record_identifier
survey_weight
replicate_weight
imputation_flag
[... 69 more lines ...]

Output: {"concept": <id or "none">, "alternatives": [<up to two other ids, best first>], "confidence": <0 to 1>}
---
VARIABLE
dataset: cbecs2018
variable name: SQFT
label: Square footage
```

### Mapping, condition L2D

```
You are an expert in urban building energy modeling (UBEM) and in building energy survey data. Answer with one JSON object that follows the required schema.

Task: map one survey variable to the single most specific concept in the target vocabulary that the variable measures or records. Answer "none" if no concept applies.

TARGET VOCABULARY
record_identifier: record identifier. Identifier of a record, building, meter, station or respondent within the dataset.
survey_weight: survey analysis weight. Final sampling weight that expands a sampled record to the population it represents.
replicate_weight: replicate weight. Replicate weight used to estimate sampling variance (jackknife, balanced repeated replication).
imputation_flag: imputation or quality flag. Indicator that another variable's value was imputed, edited, top-coded or suppressed.
[... 69 more lines ...]

Output: {"concept": <id or "none">, "alternatives": [<up to two other ids, best first>], "confidence": <0 to 1>}
---
VARIABLE
dataset: cbecs2018
variable name: SQFT
label: Square footage
```

### Mapping, condition L2

```
You are an expert in urban building energy modeling (UBEM) and in building energy survey data. Answer with one JSON object that follows the required schema.

Task: map one survey variable to the single most specific concept in the target vocabulary that the variable measures or records. Answer "none" if no concept applies.

TARGET VOCABULARY
record_identifier: record identifier. Identifier of a record, building, meter, station or respondent within the dataset. [broader=record; describes=dataset_record; also called: id, identifier, unique id, building id, respondent id, key]
survey_weight: survey analysis weight. Final sampling weight that expands a sampled record to the population it represents. [broader=record; describes=dataset_record; also called: sampling weight, final weight, expansion factor, analysis weight]
replicate_weight: replicate weight. Replicate weight used to estimate sampling variance (jackknife, balanced repeated replication). [broader=record; describes=dataset_record; also called: jackknife weight, BRR weight, variance weight]
imputation_flag: imputation or quality flag. Indicator that another variable's value was imputed, edited, top-coded or suppressed. [broader=record; describes=dataset_record; also called: imputed flag, edit flag, data quality flag, allocation flag]
[... 69 more lines ...]

Output: {"concept": <id or "none">, "alternatives": [<up to two other ids, best first>], "confidence": <0 to 1>}
---
VARIABLE
dataset: cbecs2018
variable name: SQFT
label: Square footage
```

### Mapping, condition O2D

```
You are an expert in urban building energy modeling (UBEM) and in building energy survey data. Answer with one JSON object that follows the required schema.

Task: map one survey variable to the single most specific concept in the target vocabulary that the variable measures or records. Answer "none" if no concept applies.

TARGET VOCABULARY
C001: Identifier of a record, building, meter, station or respondent within the dataset.
C002: Final sampling weight that expands a sampled record to the population it represents.
C003: Replicate weight used to estimate sampling variance (jackknife, balanced repeated replication).
C004: Indicator that another variable's value was imputed, edited, top-coded or suppressed.
[... 69 more lines ...]

Output: {"concept": <id or "none">, "alternatives": [<up to two other ids, best first>], "confidence": <0 to 1>}
---
VARIABLE
dataset: cbecs2018
variable name: SQFT
label: Square footage
```

### Mapping, condition XBE

```
You are an expert in urban building energy modeling (UBEM) and in building energy survey data. Answer with one JSON object that follows the required schema.

Task: map one survey variable to the single most specific concept in the target vocabulary that the variable measures or records. Answer "none" if no concept applies.

TARGET VOCABULARY
record_identifier: Identifier. A unique value associated with an Identifier Label or other qualifier.
survey_weight
replicate_weight
imputation_flag: Derivation Method. The method by which the data was learned.
[... 69 more lines ...]

Output: {"concept": <id or "none">, "alternatives": [<up to two other ids, best first>], "confidence": <0 to 1>}
---
VARIABLE
dataset: cbecs2018
variable name: SQFT
label: Square footage
```

### Normalization, without the dataset card

```
You are an expert in urban building energy modeling (UBEM) and in building energy survey data. Answer with one JSON object that follows the required schema.

Task: read the codebook entry of one survey variable and normalize it. Fields:
is_weight: true if it is a sampling or analysis weight (final or replicate).
is_replicate_weight: true if it is a replicate weight.
is_imputation_flag: true if it flags imputation of another variable.
flags_variable: the variable name it flags, or "none".
unit: one of ['unit:BTU_IT', 'unit:KiloW-HR', 'unit:FT3', 'unit:GAL_US', 'iso4217:USD', 'unit:FT2', 'unit:DEG_F', 'unit:HR', 'none'] for numeric quantities; "none" for categorical or unitless variables.
unit_multiplier: factor applied to raw values before the unit applies (1000 for 'thousand Btu', 100 for 'hundred cubic feet', otherwise 1); 0 if there is no unit.
missing_codes: codes meaning not applicable, withheld, refused, don't know or missing; use "" for a blank ("Missing=...").
codes: every categorical code as [code, label]; [] if the variable is not categorical.
---
dataset: cbecs2018
variable name: MFBTU
label: Derived variable: Annual major fuels consumption (thous Btu)
values/format codes (verbatim):
124 – 802,588,047
Missing=Not applicable
```

### Normalization, with the dataset card

```
You are an expert in urban building energy modeling (UBEM) and in building energy survey data. Answer with one JSON object that follows the required schema.

Task: read the codebook entry of one survey variable and normalize it. Fields:
is_weight: true if it is a sampling or analysis weight (final or replicate).
is_replicate_weight: true if it is a replicate weight.
is_imputation_flag: true if it flags imputation of another variable.
flags_variable: the variable name it flags, or "none".
unit: one of ['unit:BTU_IT', 'unit:KiloW-HR', 'unit:FT3', 'unit:GAL_US', 'iso4217:USD', 'unit:FT2', 'unit:DEG_F', 'unit:HR', 'none'] for numeric quantities; "none" for categorical or unitless variables.
unit_multiplier: factor applied to raw values before the unit applies (1000 for 'thousand Btu', 100 for 'hundred cubic feet', otherwise 1); 0 if there is no unit.
missing_codes: codes meaning not applicable, withheld, refused, don't know or missing; use "" for a blank ("Missing=...").
codes: every categorical code as [code, label]; [] if the variable is not categorical.

DATASET PROFILE (UBEM-Link)
# 2018 Commercial Buildings Energy Consumption Survey (CBECS) public-use microdata (chr-cbecs-2018)
- UBEM workflow roles: building_characteristics, calibration_validation
- Statistical nature: sample_survey_weighted
- Finest public spatial granularity: census_region_division
- Temporal resolution: P1Y
- Access: open_download
- Join keys: census_region_division, building_type
- License: US-Government-Public-Domain
- Survey weights: FINALWT plus 151 replicate weights (FINALWT1-FINALWT151); variable
[... dataset card continues ...]
---
dataset: cbecs2018
variable name: MFBTU
label: Derived variable: Annual major fuels consumption (thous Btu)
values/format codes (verbatim):
124 – 802,588,047
Missing=Not applicable
```

### City case, column selection (L2)

```
You are an expert in urban building energy modeling (UBEM) and in building energy survey data. Answer with one JSON object that follows the required schema.

Task: a data pipeline needs the column of a dataset that holds a given concept. Choose the single best column, or "none" if no column holds it.

DATASET COLUMNS (field: display name)
report_year: Calendar Year
property_id: Property ID
property_name: Property Name
parent_property_id: Parent Property ID
parent_property_name: Parent Property Name
[... 260 more columns ...]
---
CONCEPT
gross_floor_area: gross floor area. Total floor area within the exterior walls, all storeys. [broader=characteristics; describes=building; unit=unit:M2; also called: floorspace, floor area, square footage, conditioned area, GFA, building size]

PURPOSE
compute annual energy use intensity per unit floor area
```

### City case, normalization input

```
dataset: nyc_ll84
variable name: Site Energy Use (kBtu)
label: Site Energy Use (kBtu). The annual amount of all the energy your property consumes on-site, regardless of the source. It includes energy purchased from the grid or in bulk (which are the amounts on utility bills), as well as renewable energy generated and consumed
values/format codes (verbatim):
numeric values from -403,402 to 47,279,141,222; "Not Available" (2,784 records)
```

### Four-source case: the tool's normalization prompt (scoped conventions)

```
You are an expert in urban building energy modeling (UBEM) and in building energy survey data. Answer with one JSON object that follows the required schema.

Task: read the documentation of one column of a dataset and a summary of its values, and state how its values must be read. Fields:
datatype: one of ['integer', 'float', 'string', 'categorical', 'boolean', 'datetime', 'geometry', 'identifier'].
unit: the unit of numeric quantities, chosen from the UNIT LIST exactly as the source publishes it (kBtu is unit:KiloBTU_IT, therms are unit:THM_US, feet are unit:FT); "none" for categorical, identifier, text or unitless columns and for counts and calendar years.
unit_multiplier: 1 unless the documentation says values are in thousands, hundreds or millions of the unit (for example "in thousands of dollars": unit:CCY_USD with multiplier 1000).
missing_codes: values that mean missing, unknown, not applicable or withheld (use "" for an empty value). Do not list a value that is a valid observation.
codes: every categorical code as [code, label]; [] if the column is not categorical.
is_weight, is_replicate_weight: true for sampling or analysis weights.
is_imputation_flag and flags_variable: true and the column it flags, if it records whether another column was imputed; otherwise false and "none".
aggregation: one of ['static', 'instantaneous', 'total_over_period', 'average_over_period', 'count', 'share', 'none'].

UNIT LIST
unit:KiloW-HR: kilowatt-hour (kWh) [energy]
unit:W-HR: watt-hour (Wh) [energy]
unit:MegaW-HR: megawatt-hour (MWh) [energy]
unit:GigaW-HR: gigawatt-hour (GWh) [energy]
unit:BTU_IT: British thermal unit (Btu) [energy]
unit:KiloBTU_IT: thousand Btu (kBtu) [energy]
[... 39 more units ...]

CONVENTIONS OF THIS DATASET THAT APPLY TO THIS COLUMN
- roof height and ground elevation: Heights and elevations are in feet; the roof height is measured above the ground elevation, not above sea level. Example: height_roof = 33.49 means a roof 33.49 ft (10.2 m) above the ground.
- roof height and construction year: A value of zero or an empty value means that the information was not available. Example: construction_year = 0 means the construction year is unknown.
---
COLUMN
dataset: nyc_footprints
column name: height_roof
label: Height Roof
values in the data: numeric values from 0 to 1,550 (median 26.15), 714 zeros
```


## S3. Category profiles

Every field of the seven category profiles, generated from the schema. The category profiles of the catalog were drafted by agents from the verified entries: 88 from the entry text alone, 3 also against a publisher page, and the New York City PLUTO and footprint entries from the publishers' metadata; fields that could not be established were left empty (provenance per entry in the repository).

Category-specific part of a dataset profile: what a modeler must know about one kind of UBEM data before using it. There is one profile class per UBEM workflow role. The classes refine the per-category metadata table of an earlier taxonomy of open UBEM data: its free-text fields became typed fields with closed value lists, its "macroscopic" and "microscopic" energy data share EnergyProfile and differ in energy_data_scale, and its "comprehensive data lake" is a Catalog of profiles rather than a category.

Every category profile also has `provides_concepts` (ids of UBEM-Link concepts the dataset provides) and `metadata_standards` (standards the publisher already uses).

### WeatherProfile

Key in a dataset profile: `weather_profile`; UBEM role: `boundary_conditions`.

Weather and climate data used as boundary conditions: observed station records, reanalyses, typical and actual meteorological years, and climate projections.

| Field | | Meaning | Allowed values |
|---|---|---|---|
| `weather_year_type` | required, list | Kind of weather year or series: actual series, actual or typical meteorological year, normals, or projection. | `actual_series`, `actual_meteorological_year`, `typical_meteorological_year`, `climate_normals`, `future_typical_year`, `projection_series`, `design_conditions` |
| `weather_file_format` | list | Formats in which weather is released, which decide whether a simulation engine can read it directly. | `epw`, `tmy3_csv`, `netcdf`, `grib`, `csv`, `api_json`, `other` |
| `timestamp_convention` |  | Whether a timestamp marks the end, the start or the instant of the interval it describes. | `interval_ending`, `interval_beginning`, `instantaneous`, `unknown` |
| `time_basis` |  | Clock to which timestamps refer (UTC, local standard time, or local time with daylight saving). | `utc`, `local_standard_time`, `local_time_with_dst`, `unknown` |
| `gap_filling` |  | How missing or sub-interval values were filled by the publisher. | `none`, `linear_interpolation`, `model_based`, `unknown` |
| `grid_resolution_km` |  | Horizontal resolution of a gridded product in kilometres. |  |
| `station_id_scheme` |  | Identifier system of the stations (for example WMO, USAF-WBAN, GHCN). |  |
| `climate_scenarios` | list | Emission or socio-economic scenarios of a projection (for example SSP2-4.5, RCP8.5). |  |

### GeometryProfile

Key in a dataset profile: `geometry_profile`; UBEM role: `geometry_inventory`.

Building stock geometry and inventory: footprints, heights, 3D city models and parcels.

| Field | | Meaning | Allowed values |
|---|---|---|---|
| `geometry_dimension` | required | Geometric representation of buildings, from points and footprints to 3D solids. | `point`, `footprint_2d`, `footprint_with_height`, `solid_3d`, `raster`, `parcel_polygon` |
| `levels_of_detail` | list | CityGML levels of detail provided. | `lod0`, `lod1`, `lod2`, `lod3`, `lod4` |
| `height_source` | list | How building heights were obtained. | `lidar`, `photogrammetry`, `plans_or_records`, `model_estimated`, `derived_from_floors`, `none` |
| `height_reference` |  | Reference points between which a building height is measured. | `ground_to_roof_top`, `ground_to_eave`, `ground_to_mean_roof`, `above_sea_level`, `unknown` |
| `coordinate_reference_system` |  | Coordinate reference system of the published geometry, as an EPSG code (for example EPSG:4326). |  |
| `crs_linear_unit` |  | Linear unit of the coordinate reference system and of lengths and areas derived from it (QUDT CURIE, for example unit:FT_US or unit:M). |  |
| `building_id_scheme` |  | Building identifier system used (for example BIN, UPRN, BAG, UBID); null if none. |  |
| `minimum_building_size` |  | Capture threshold for buildings, as stated by the publisher (for example 'larger than 400 sq ft'). |  |

### OperationProfile

Key in a dataset profile: `operation_profile`; UBEM role: `operation_use`.

Occupancy, occupant behavior, schedules, setpoints and time use.

| Field | | Meaning | Allowed values |
|---|---|---|---|
| `behavior_types` | required, list | Kinds of occupant behavior or building operation recorded. | `occupancy_presence`, `hvac_operation`, `thermostat_setpoint`, `window_operation`, `lighting_operation`, `appliance_plug_loads`, `hot_water_use`, `thermal_comfort`, `time_use_activities`, `mobility` |
| `control_actions` | list | Occupant control actions recorded. | `thermostat_adjustment`, `hvac_on_off`, `lighting_on_off`, `window_open_close`, `shading_adjustment`, `appliance_on_off` |
| `collection_method` | list | How the behavior or operation data were collected. | `sensors_or_logs`, `connected_devices`, `survey_or_diary`, `field_study_compilation`, `mobile_location` |
| `building_sectors` | list | Building sectors covered. | `residential`, `commercial`, `industrial`, `all` |

### CharacteristicsProfile

Key in a dataset profile: `characteristics_profile`; UBEM role: `building_characteristics`.

Non-geometric building characteristics (use type, vintage, envelope, systems, fuels) from surveys, administrative records, certificates and dictionaries.

| Field | | Meaning | Allowed values |
|---|---|---|---|
| `data_form` | required, list | Whether the data are records of individual units (microdata or building records) or published distributions (aggregate tables). | `microdata`, `building_records`, `aggregate_tables`, `dictionary_or_standard`, `archetype_library` |
| `building_sectors` | list | Building sectors covered. | `residential`, `commercial`, `industrial`, `all` |
| `representativeness` |  | How the covered buildings relate to the building stock, which decides whether results generalize. | `probability_sample`, `complete_population`, `mandated_subset`, `voluntary_or_convenience`, `synthetic`, `unknown` |
| `coverage_threshold` |  | Size or other threshold that decides which buildings are covered (for example 'more than 25,000 ft²'). |  |
| `cross_tabulations` | list | For aggregate tables, the joint distributions published, each as concept ids joined by ' x '. |  |

### EnergyProfile

Key in a dataset profile: `energy_profile`; UBEM role: `calibration_validation`.

Measured or reported energy use for calibration and validation, from national balances (macroscopic) to buildings, meters and appliances (microscopic).

| Field | | Meaning | Allowed values |
|---|---|---|---|
| `energy_data_scale` | required | Macroscopic (aggregates over many buildings) or microscopic (buildings, meters, circuits or appliances). | `macroscopic`, `microscopic` |
| `energy_sectors` | list | Energy-using sectors covered. | `residential`, `commercial`, `industrial`, `transportation`, `all` |
| `energy_carriers` | list | Energy carriers reported. | `electricity`, `natural_gas`, `fuel_oil`, `propane`, `district_energy`, `biomass`, `onsite_renewables`, `all_carriers` |
| `energy_metrics` | list | Kinds of energy quantity reported. | `site_energy`, `source_energy`, `primary_energy`, `end_use_energy`, `load_profile`, `peak_demand`, `emissions`, `expenditure` |
| `metering_level` |  | Finest level at which energy is measured or reported. | `area_aggregate`, `utility_territory`, `whole_building`, `submeter_end_use`, `circuit_or_appliance` |
| `measurement_basis` |  | Whether values are metered, billed, self-reported or modeled. | `metered`, `billed`, `self_reported`, `modeled_or_estimated`, `mixed` |
| `weather_normalized_available` |  | True if weather-normalized values are published alongside the actual ones. |  |
| `reporting_period` |  | Period one value covers (for example calendar year, billing month). |  |

### SimulationProfile

Key in a dataset profile: `simulation_profile`; UBEM role: `reference_simulation`.

Reference simulations and model libraries: synthetic building-stock outputs and prototype models.

| Field | | Meaning | Allowed values |
|---|---|---|---|
| `simulation_engine` |  | Simulation engine that produced the data (for example EnergyPlus). |  |
| `stock_representation` |  | How the simulated building stock is represented. | `sampled_models`, `building_by_building`, `prototype_library` |
| `weather_basis` |  | Weather used for the simulations (for example AMY 2018, TMY3). |  |
| `building_sectors` | list | Building sectors covered. | `residential`, `commercial`, `industrial`, `all` |

### ContextProfile

Key in a dataset profile: `context_profile`; UBEM role: `context_coupling`.

Context and coupling data: socio-economic data, land use, grid emissions, tariffs and urban climate.

| Field | | Meaning | Allowed values |
|---|---|---|---|
| `context_kind` | list | Kind of context or coupling data. | `grid_emissions`, `energy_tariffs`, `land_use`, `socio_economic`, `urban_climate_zones` |


## S4. Concept vocabulary

The 73 mapping targets with their definitions, canonical units and links to Brick 1.4.4, BEDES 2.5 and the CityGML Energy ADE 1.0. Each linked term was checked to exist in the release files; the relation type was assigned with AI assistance and has not been audited by an independent expert.

| id | group | definition | unit | links (standard:relation) |
|---|---|---|---|---|
| record_identifier | record | Identifier of a record, building, meter, station or respondent within the dataset. |  | bedes:closeMatch |
| survey_weight | record | Final sampling weight that expands a sampled record to the population it represents. |  |  |
| replicate_weight | record | Replicate weight used to estimate sampling variance (jackknife, balanced repeated replication). |  |  |
| imputation_flag | record | Indicator that another variable's value was imputed, edited, top-coded or suppressed. |  | bedes:relatedMatch; bedes:relatedMatch |
| timestamp | record | Date and time the observation refers to. |  | brick:closeMatch; bedes:broadMatch; energy_ade:relatedMatch |
| survey_reference_detail | record | Information about how the record was collected (respondent type, interview mode, data source), not about the building. |  | bedes:relatedMatch |
| geographic_coordinates | location | Latitude and longitude (WGS84) of a building, station or grid cell centroid. |  | brick:closeMatch; brick:narrowMatch; brick:narrowMatch; bedes:narrowMatch; bedes:narrowMatch; energy_ade:closeMatch |
| administrative_region | location | Region the record belongs to, such as country, census region or division, state, county, city, tract or postal code. |  | brick:closeMatch; bedes:narrowMatch; bedes:narrowMatch; bedes:narrowMatch; bedes:narrowMatch; bedes:narrowMatch |
| climate_zone | location | Climate classification of the location (ASHRAE/IECC climate zone, building America zone, Koppen class). |  | bedes:exactMatch; bedes:relatedMatch |
| urban_rural_indicator | location | Classification of the location by settlement type or density. |  | bedes:closeMatch |
| dry_bulb_temperature | weather | Outdoor air temperature measured by a thermometer shielded from radiation and moisture. | unit:DEG_C | brick:relatedMatch; bedes:closeMatch; energy_ade:closeMatch |
| dew_point_temperature | weather | Temperature to which outdoor air must be cooled at constant pressure to reach saturation. | unit:DEG_C | brick:relatedMatch |
| relative_humidity | weather | Ratio of the partial pressure of water vapor in outdoor air to its saturation pressure. | unit:PERCENT | brick:relatedMatch; bedes:closeMatch; energy_ade:closeMatch |
| atmospheric_pressure | weather | Atmospheric pressure at the station elevation. | unit:PA | brick:broadMatch |
| global_horizontal_irradiance | weather | Total solar irradiance on a horizontal surface. | unit:W-PER-M2 | brick:broadMatch; bedes:closeMatch; energy_ade:closeMatch |
| direct_normal_irradiance | weather | Beam solar irradiance on a surface normal to the sun. | unit:W-PER-M2 | bedes:closeMatch; energy_ade:relatedMatch |
| diffuse_horizontal_irradiance | weather | Sky-diffuse solar irradiance on a horizontal surface. | unit:W-PER-M2 | bedes:closeMatch; energy_ade:closeMatch |
| wind_speed | weather | Horizontal wind speed at the reference height. | unit:M-PER-SEC | brick:relatedMatch; bedes:closeMatch; energy_ade:closeMatch |
| wind_direction | weather | Direction from which the wind blows, clockwise from north. | unit:DEG | brick:relatedMatch |
| precipitation | weather | Liquid-equivalent precipitation depth over the time step. | unit:MilliM | brick:relatedMatch |
| degree_days | weather | Sum over a period of the difference between a base temperature and daily mean outdoor temperature. | unit:DEG_C | bedes:narrowMatch; bedes:narrowMatch |
| footprint | geometry | Polygon of the building's ground outline. |  |  |
| building_height | geometry | Height of the building from ground to roof (state reference points where known). | unit:M | bedes:broadMatch; energy_ade:closeMatch |
| floors_above_ground | geometry | Count of storeys above grade. |  | bedes:relatedMatch |
| floors_below_ground | geometry | Count or presence of storeys below grade, including basements. |  | brick:relatedMatch |
| floor_to_ceiling_height | geometry | Typical vertical distance between floor and ceiling. | unit:M | bedes:relatedMatch |
| building_shape | geometry | Plan shape of the building (rectangle, L, U, H, courtyard, other). |  | bedes:exactMatch |
| roof_shape | geometry | Roof geometry type or slope (flat, pitched, gable, hip). |  | bedes:closeMatch |
| window_to_wall_ratio | geometry | Share of exterior wall area that is glazed. | unit:PERCENT | bedes:exactMatch; energy_ade:closeMatch |
| building_use_type | characteristics | Principal activity or function of the building (office, retail, education, single-family, etc.). |  | brick:closeMatch; bedes:closeMatch; energy_ade:closeMatch |
| secondary_use | characteristics | Additional activities in the building, or a finer subtype of its principal activity. |  |  |
| gross_floor_area | characteristics | Total floor area within the exterior walls, all storeys. | unit:M2 | brick:exactMatch; bedes:broadMatch; bedes:relatedMatch; energy_ade:closeMatch |
| floor_area_category | gross_floor_area | Binned floor area class. |  |  |
| year_of_construction | characteristics | Year (or period) the building was completed. |  | brick:closeMatch |
| renovation | characteristics | Whether and how the building was renovated (envelope, systems, lighting, additions). |  | energy_ade:closeMatch |
| wall_construction | characteristics | Material or assembly type of exterior walls. |  | bedes:broadMatch; energy_ade:broadMatch |
| roof_construction | characteristics | Material or assembly type of the roof. |  | bedes:broadMatch; energy_ade:broadMatch |
| window_properties | characteristics | Window type, number of panes, frame, coatings, tinting or shading. |  | bedes:closeMatch; bedes:narrowMatch; bedes:narrowMatch; bedes:narrowMatch |
| insulation | characteristics | Presence, level or upgrade of thermal insulation in walls, roof or floors. |  | brick:relatedMatch; bedes:closeMatch; bedes:narrowMatch; energy_ade:relatedMatch |
| heating_system | characteristics | Type, presence or share of space heating equipment (furnace, boiler, heat pump, district heat). |  | brick:broadMatch; bedes:closeMatch |
| cooling_system | characteristics | Type, presence or share of space cooling equipment (chiller, packaged unit, central AC, room AC). |  | brick:broadMatch; bedes:closeMatch |
| ventilation_system | characteristics | Ventilation, economizer, variable-air-volume or air distribution features. |  | brick:closeMatch; brick:narrowMatch; brick:narrowMatch; bedes:narrowMatch; bedes:narrowMatch; bedes:narrowMatch; energy_ade:narrowMatch |
| water_heating_system | characteristics | Type, fuel or size of domestic or service hot-water equipment. |  | brick:closeMatch; brick:narrowMatch; bedes:closeMatch |
| lighting_system | characteristics | Lamp types, lit share of floor area, or lighting controls. |  | brick:closeMatch; bedes:narrowMatch; energy_ade:closeMatch |
| plug_and_process_equipment | characteristics | Presence or count of appliances, computers, refrigeration, cooking or other process equipment. |  | bedes:narrowMatch; bedes:narrowMatch; energy_ade:closeMatch |
| energy_sources_used | characteristics | Which fuels or energy carriers are used in the building, overall or for a given end use. |  | bedes:closeMatch; energy_ade:closeMatch |
| onsite_generation | characteristics | On-site renewable or fossil generation, cogeneration, or energy storage. |  | brick:narrowMatch; brick:narrowMatch; brick:narrowMatch; bedes:narrowMatch; bedes:narrowMatch; energy_ade:narrowMatch; energy_ade:narrowMatch; energy_ade:narrowMatch |
| building_controls | characteristics | Energy management systems, smart thermostats, demand response participation, or control strategies. |  | brick:narrowMatch; bedes:closeMatch; bedes:narrowMatch |
| dwelling_units | characteristics | Number of housing units in the building. |  | bedes:relatedMatch; energy_ade:relatedMatch |
| ownership_tenure | characteristics | Who owns or occupies the building and how (owner-occupied, rented, government, vacant share). |  | bedes:closeMatch; bedes:narrowMatch; bedes:narrowMatch; energy_ade:closeMatch |
| rooms_and_spaces | characteristics | Counts or shares of specific spaces (bedrooms, classrooms, seats, beds, server rooms). |  | brick:relatedMatch; bedes:relatedMatch; energy_ade:narrowMatch |
| occupant_count | operation | Number of people who work in, live in or occupy the building. |  | brick:relatedMatch; bedes:relatedMatch; energy_ade:closeMatch |
| operating_hours | operation | Hours or days per week the building or a space is open or occupied. |  | bedes:narrowMatch; energy_ade:narrowMatch |
| thermostat_setpoint | operation | Indoor temperature setpoint for heating or cooling, occupied or unoccupied. | unit:DEG_C | brick:narrowMatch; brick:narrowMatch; bedes:broadMatch; bedes:relatedMatch; energy_ade:narrowMatch; energy_ade:narrowMatch |
| equipment_usage_behavior | operation | How often or how long occupants use appliances or systems. |  |  |
| time_use_activity | operation | Activity episodes of persons with time, duration and location. |  |  |
| thermal_comfort_response | operation | Occupant thermal sensation, preference or acceptability vote. |  |  |
| occupant_control_action | operation | Observed occupant interaction with building systems (window opening, light switching, blinds, thermostat change). |  |  |
| indoor_environment | operation | Measured indoor temperature, humidity, CO2, illuminance or air quality. |  | brick:narrowMatch; brick:narrowMatch; brick:narrowMatch; brick:narrowMatch; brick:narrowMatch |
| household_demographics | operation | Socio-demographic attributes of occupants (age, income, education, employment). |  | bedes:narrowMatch; bedes:narrowMatch; energy_ade:narrowMatch |
| total_energy_consumption | energy | Total site energy over a period, all carriers combined. | unit:KiloW-HR | brick:broadMatch; bedes:relatedMatch |
| electricity_consumption | energy | Electricity used over a period. | unit:KiloW-HR | brick:relatedMatch; bedes:relatedMatch |
| natural_gas_consumption | energy | Natural gas used over a period. | unit:KiloW-HR | brick:relatedMatch; bedes:relatedMatch |
| other_fuel_consumption | energy | Fuel oil, propane, district heat or steam, wood or other carriers used over a period. | unit:KiloW-HR | brick:narrowMatch; bedes:relatedMatch; bedes:relatedMatch; bedes:relatedMatch |
| end_use_energy | energy | Energy attributed to one end use (heating, cooling, ventilation, water heating, lighting, cooking, refrigeration, office equipment, other). | unit:KiloW-HR | bedes:relatedMatch; energy_ade:relatedMatch |
| energy_expenditure | energy | Money spent on energy over a period. | unit:CCY_USD | bedes:closeMatch |
| energy_use_intensity | energy | Energy use per unit floor area over a year. | unit:KiloW-HR-PER-M2 | bedes:closeMatch |
| load_timeseries | energy | Energy or power at sub-annual intervals from a meter, sub-meter or aggregate. | unit:KiloW | brick:relatedMatch; bedes:relatedMatch; energy_ade:broadMatch |
| peak_demand | energy | Maximum power over a period. | unit:KiloW | brick:relatedMatch; bedes:relatedMatch; energy_ade:closeMatch |
| primary_energy_or_emissions | energy | Source energy, primary energy or greenhouse gas emissions attributed to energy use. |  | bedes:narrowMatch; bedes:relatedMatch; energy_ade:relatedMatch |
| grid_emission_factor | context | Emissions per unit of electricity generated or consumed in a grid region. |  | bedes:broadMatch; bedes:relatedMatch; energy_ade:relatedMatch |
| energy_price | context | Price per unit energy or demand, or tariff structure. |  | bedes:closeMatch; bedes:narrowMatch |
| land_use | context | Land use class or land cover of the parcel or cell. |  |  |

## S5. Profile checks

Version 1 was written on the 11 variables of the national pipeline (E7). Version 2 was written after applying version 1 to all normalization outputs of the benchmark, and committed before any profile of the New York City data was generated, but in the same commit as the LL84 catalog entry; three of its terms ('Not Available', kBtu, ft²) occur in LL84 and in neither survey, and S20 also reports version 2 without them. Both are Python functions; they use the codebook entry and the schema's unit vocabulary and are not generated from the LinkML source.

### Version 1

```python
def profile_check(item: dict, prof: dict) -> list[str]:
    """Consistency rules a schema-aware validator can apply to an AI-built variable profile, using only the
    codebook entry (never the gold): the unit agrees with the unit word in the label, the multiplier agrees with
    a 'thousand'/'hundred' qualifier and is a power of ten, a missing code is a blank or a listed code with a
    non-substantive label, and a missing code of a continuous variable lies outside its valid range."""
    label = (item.get("label") or "").lower()
    out = []
    u = prof["unit"]
    named = [k for k, words in UNIT_WORDS.items() if any(w in label for w in words)]
    if named and u not in named:
        out.append("unit disagrees with label")
    if u != "none":
        m = float(prof["unit_multiplier"] or 1)
        want = 1000.0 if "thous" in label else 100.0 if "hundred" in label else 1.0
        if m != want:
            out.append("multiplier disagrees with label")
    codes = {str(c): str(lab).lower() for c, lab in (item.get("code_list") or [])}
    lo, hi = item.get("value_min"), item.get("value_max")
    for c in prof["missing_codes"]:
        if c == "":
            continue
        if codes:
            if c not in codes:
                out.append(f"missing code {c!r} not in code list")
            elif not any(w in codes[c] for w in ("withheld", "not applicable", "don't know", "refused", "missing",
                                                   "not ascertained", "skipped")):
                out.append(f"missing code {c!r} is a substantive category")
        else:
            try:
                x = float(c)
            except ValueError:
                out.append(f"missing code {c!r} is not a code")
                continue
            if lo is not None and hi is not None and lo <= x <= hi:
                out.append(f"missing code {c!r} inside the valid range")
    return out
```

### Version 2

```python
def expected_multiplier(label: str, unit: str) -> float:
    """Multiplier implied by the label's qualifiers for the given base unit."""
    s = label.lower()
    if unit == "unit:BTU_IT":
        if re.search(r"\bmmbtu\b|million btu", s):
            return 1e6
        if re.search(r"\btherms?\b", s):
            return 1e5
        if re.search(r"\bkbtu\b|thous\w* btu|thousand british", s):
            return 1e3
    if unit == "unit:FT3":
        if re.search(r"\bccf\b|hundred cubic", s):
            return 100.0
        if re.search(r"\bmcf\b|thous\w* cubic", s):
            return 1e3
    if re.search(r"\bthous", s):
        return 1e3
    if re.search(r"\bhundred", s):
        return 100.0
    return 1.0

def check(item: dict, prof: dict) -> list[str]:
    label = item.get("label") or ""
    low = label.lower()
    codes = {str(c): str(lab).lower() for c, lab in (item.get("code_list") or [])}
    out = []
    u = prof.get("unit") or "none"
    if codes and len(codes) > 2 and u != "none":
        out.append("unit given for a categorical variable")
    if not codes or len(codes) <= 2:  # continuous (a 'Missing=...' line may appear as a one-entry code list)
        named = [k for k, words in UNIT_WORDS.items() if any(w in low for w in words)]
        if named and u not in named:
            out.append("unit disagrees with label")
        if u != "none" and float(prof.get("unit_multiplier") or 1) != expected_multiplier(label, u):
            out.append("multiplier disagrees with label")
    lo, hi = item.get("value_min"), item.get("value_max")
    for c in prof.get("missing_codes") or []:
        c = str(c)
        if c == "":
            continue
        if c in codes:
            if not any(w in codes[c] for w in NON_SUBSTANTIVE):
                out.append(f"missing code {c!r} is a substantive category")
            continue
        try:
            x = float(c)
        except ValueError:
            if not any(w in c.lower() for w in NON_SUBSTANTIVE):
                out.append(f"missing code {c!r} is neither a listed code nor a missing-value label")
            continue
        if lo is not None and hi is not None and lo <= x <= hi:
            out.append(f"missing code {c!r} inside the valid range")
    return out
```


## S6. Mapping accuracy by condition: intervals, surveys, concepts, design weights and abstention

Cluster intervals resample gold concepts. Design-weighted accuracy weights each variable by the inverse sampling fraction of its stratum (survey x rule-based draft concept).

| model | condition | n | acc@1 | cluster_lo | cluster_hi | lenient | acc_cbecs | acc_recs | macro_per_concept | concepts | design_weighted | none_items | none_answered_none | false_none_on_mappable |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| llama3.1:8b | L0 | 295 | 0.427 | 0.279 | 0.605 | 0.553 | 0.510 | 0.342 | 0.629 | 44 | 0.429 | 5 | 0 | 5 |
| llama3.1:8b | L1 | 295 | 0.397 | 0.270 | 0.575 | 0.498 | 0.470 | 0.322 | 0.614 | 44 | 0.398 | 5 | 3 | 33 |
| llama3.1:8b | L2D | 295 | 0.525 | 0.368 | 0.693 | 0.634 | 0.638 | 0.411 | 0.700 | 44 | 0.526 | 5 | 1 | 3 |
| llama3.1:8b | L2 | 295 | 0.546 | 0.426 | 0.695 | 0.637 | 0.611 | 0.479 | 0.681 | 44 | 0.543 | 5 | 1 | 14 |
| llama3.1:8b | L2N | 295 | 0.576 | 0.467 | 0.699 | 0.651 | 0.644 | 0.507 | 0.704 | 44 | 0.584 | 5 | 1 | 11 |
| llama3.1:8b | O0 | 295 | 0.020 | 0.004 | 0.042 | 0.020 | 0.013 | 0.027 | 0.036 | 44 | 0.014 | 5 | 0 | 0 |
| llama3.1:8b | O2D | 295 | 0.553 | 0.418 | 0.681 | 0.644 | 0.638 | 0.466 | 0.660 | 44 | 0.558 | 5 | 0 | 1 |
| llama3.1:8b | L2S | 295 | 0.546 | 0.440 | 0.679 | 0.631 | 0.523 | 0.568 | 0.695 | 44 | 0.514 | 5 | 1 | 10 |
| llama3.1:8b | L2U | 295 | 0.532 | 0.416 | 0.673 | 0.627 | 0.584 | 0.479 | 0.677 | 44 | 0.524 | 5 | 2 | 15 |
| llama3.1:8b | L3 | 295 | 0.522 | 0.424 | 0.655 | 0.607 | 0.604 | 0.438 | 0.735 | 44 | 0.512 | 5 | 3 | 40 |
| llama3.1:8b | L3E | 295 | 0.583 | 0.502 | 0.688 | 0.685 | 0.631 | 0.534 | 0.762 | 44 | 0.576 | 5 | 2 | 25 |
| llama3.1:8b | XBR | 295 | 0.349 | 0.218 | 0.534 | 0.441 | 0.423 | 0.274 | 0.613 | 44 | 0.341 | 5 | 1 | 28 |
| llama3.1:8b | XBE | 295 | 0.427 | 0.303 | 0.598 | 0.542 | 0.510 | 0.342 | 0.608 | 44 | 0.430 | 5 | 1 | 13 |
| llama3.1:8b | XEA | 295 | 0.420 | 0.289 | 0.604 | 0.508 | 0.497 | 0.342 | 0.615 | 44 | 0.423 | 5 | 3 | 45 |
| qwen3:8b | L0 | 295 | 0.417 | 0.289 | 0.587 | 0.522 | 0.443 | 0.390 | 0.699 | 44 | 0.389 | 5 | 0 | 9 |
| qwen3:8b | L1 | 295 | 0.471 | 0.318 | 0.664 | 0.576 | 0.517 | 0.425 | 0.757 | 44 | 0.456 | 5 | 0 | 10 |
| qwen3:8b | L2D | 295 | 0.549 | 0.386 | 0.713 | 0.668 | 0.597 | 0.500 | 0.797 | 44 | 0.535 | 5 | 1 | 9 |
| qwen3:8b | L2 | 295 | 0.586 | 0.443 | 0.744 | 0.685 | 0.631 | 0.541 | 0.757 | 44 | 0.573 | 5 | 1 | 5 |
| qwen3:8b | L2N | 295 | 0.553 | 0.404 | 0.736 | 0.647 | 0.564 | 0.541 | 0.804 | 44 | 0.531 | 5 | 0 | 13 |
| qwen3:8b | O0 | 295 | 0.007 | 0.000 | 0.026 | 0.007 | 0.007 | 0.007 | 0.023 | 44 | 0.002 | 5 | 0 | 0 |
| qwen3:8b | O2D | 295 | 0.620 | 0.525 | 0.729 | 0.715 | 0.631 | 0.610 | 0.772 | 44 | 0.609 | 5 | 0 | 0 |
| qwen3:8b | L2S | 295 | 0.546 | 0.420 | 0.703 | 0.641 | 0.550 | 0.541 | 0.779 | 44 | 0.517 | 5 | 1 | 4 |
| qwen3:8b | L2U | 295 | 0.593 | 0.442 | 0.745 | 0.692 | 0.644 | 0.541 | 0.758 | 44 | 0.585 | 5 | 1 | 6 |
| qwen3:8b | L3 | 295 | 0.512 | 0.425 | 0.634 | 0.597 | 0.597 | 0.425 | 0.740 | 44 | 0.500 | 5 | 1 | 25 |
| qwen3:8b | L3E | 295 | 0.563 | 0.449 | 0.687 | 0.661 | 0.604 | 0.521 | 0.778 | 44 | 0.542 | 5 | 0 | 20 |
| qwen3:8b | XBR | 295 | 0.424 | 0.272 | 0.612 | 0.519 | 0.483 | 0.363 | 0.699 | 44 | 0.412 | 5 | 5 | 51 |
| qwen3:8b | XBE | 295 | 0.475 | 0.323 | 0.633 | 0.563 | 0.510 | 0.438 | 0.706 | 44 | 0.456 | 5 | 0 | 21 |
| qwen3:8b | XEA | 295 | 0.461 | 0.336 | 0.630 | 0.549 | 0.544 | 0.377 | 0.751 | 44 | 0.450 | 5 | 3 | 29 |

## S7. Paired comparisons under four label sets

Exact McNemar tests; Holm adjustment over all comparisons and both models within each label set.

| label_set | model | experiment | condition | versus | question | n | acc_condition | acc_versus | delta | delta_cluster_lo | delta_cluster_hi | gained | lost | p_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| adjudicated gold | llama3.1:8b | E1 | L1 | L0 | labels over identifiers | 295 | 0.397 | 0.427 | -0.031 | -0.102 | 0.031 | 17 | 26 | 0.222 | 1.000 |
| adjudicated gold | llama3.1:8b | E1 | L2D | L1 | definitions over labels | 295 | 0.525 | 0.397 | 0.129 | -0.003 | 0.268 | 53 | 15 | 0.000 | 0.000 |
| adjudicated gold | llama3.1:8b | E1 | L2 | L2D | group, entity, unit and synonyms over definitions | 295 | 0.546 | 0.525 | 0.020 | -0.049 | 0.083 | 28 | 22 | 0.480 | 1.000 |
| adjudicated gold | llama3.1:8b | E1 | L2N | L1 | group, entity, unit and synonyms over labels (no definitions) | 295 | 0.576 | 0.397 | 0.180 | 0.068 | 0.273 | 63 | 10 | 0.000 | 0.000 |
| adjudicated gold | llama3.1:8b | E1 | L2 | L2N | definitions over the rest of the card | 295 | 0.546 | 0.576 | -0.031 | -0.116 | 0.074 | 23 | 32 | 0.281 | 1.000 |
| adjudicated gold | llama3.1:8b | E1 | O2D | O0 | definitions with opaque codes | 295 | 0.553 | 0.020 | 0.532 | 0.390 | 0.659 | 160 | 3 | 0.000 | 0.000 |
| adjudicated gold | llama3.1:8b | E1 | L0 | O0 | meaningful identifiers over opaque codes | 295 | 0.427 | 0.020 | 0.407 | 0.262 | 0.584 | 123 | 3 | 0.000 | 0.000 |
| adjudicated gold | llama3.1:8b | E2 | L2U | L2 | open versus closed output | 295 | 0.532 | 0.546 | -0.014 | -0.027 | 0.000 | 0 | 4 | 0.125 | 1.000 |
| adjudicated gold | llama3.1:8b | R | L2S | L2 | shuffled versus grouped order of the cards | 295 | 0.546 | 0.546 | 0.000 | -0.118 | 0.152 | 41 | 41 | 1.000 | 1.000 |
| adjudicated gold | llama3.1:8b | E5 | L3 | L2 | ten lexically retrieved cards versus all cards | 295 | 0.522 | 0.546 | -0.024 | -0.106 | 0.091 | 38 | 45 | 0.510 | 1.000 |
| adjudicated gold | llama3.1:8b | E5 | L3E | L2 | ten densely retrieved cards versus all cards | 295 | 0.583 | 0.546 | 0.037 | -0.102 | 0.183 | 53 | 42 | 0.305 | 1.000 |
| adjudicated gold | llama3.1:8b | E6 | XBR | L0 | Brick documentation over identifiers | 295 | 0.349 | 0.427 | -0.078 | -0.135 | -0.016 | 9 | 32 | 0.000 | 0.009 |
| adjudicated gold | llama3.1:8b | E6 | XBE | L0 | BEDES documentation over identifiers | 295 | 0.427 | 0.427 | 0.000 | -0.115 | 0.117 | 32 | 32 | 1.000 | 1.000 |
| adjudicated gold | llama3.1:8b | E6 | XEA | L0 | Energy ADE documentation over identifiers | 295 | 0.420 | 0.427 | -0.007 | -0.076 | 0.059 | 25 | 27 | 0.890 | 1.000 |
| adjudicated gold | llama3.1:8b | E6 | XBR | L2 | Brick documentation versus UBEM-Link cards | 295 | 0.349 | 0.546 | -0.197 | -0.332 | -0.078 | 11 | 69 | 0.000 | 0.000 |
| adjudicated gold | llama3.1:8b | E6 | XBE | L2 | BEDES documentation versus UBEM-Link cards | 295 | 0.427 | 0.546 | -0.119 | -0.217 | -0.026 | 17 | 52 | 0.000 | 0.001 |
| adjudicated gold | llama3.1:8b | E6 | XEA | L2 | Energy ADE documentation versus UBEM-Link cards | 295 | 0.420 | 0.546 | -0.125 | -0.269 | -0.003 | 24 | 61 | 0.000 | 0.002 |
| adjudicated gold | qwen3:8b | E1 | L1 | L0 | labels over identifiers | 295 | 0.471 | 0.417 | 0.054 | 0.011 | 0.098 | 23 | 7 | 0.005 | 0.099 |
| adjudicated gold | qwen3:8b | E1 | L2D | L1 | definitions over labels | 295 | 0.549 | 0.471 | 0.078 | -0.012 | 0.164 | 36 | 13 | 0.001 | 0.028 |
| adjudicated gold | qwen3:8b | E1 | L2 | L2D | group, entity, unit and synonyms over definitions | 295 | 0.586 | 0.549 | 0.037 | -0.053 | 0.127 | 32 | 21 | 0.169 | 1.000 |
| adjudicated gold | qwen3:8b | E1 | L2N | L1 | group, entity, unit and synonyms over labels (no definitions) | 295 | 0.553 | 0.471 | 0.081 | -0.004 | 0.198 | 36 | 12 | 0.001 | 0.015 |
| adjudicated gold | qwen3:8b | E1 | L2 | L2N | definitions over the rest of the card | 295 | 0.586 | 0.553 | 0.034 | -0.048 | 0.097 | 27 | 17 | 0.174 | 1.000 |
| adjudicated gold | qwen3:8b | E1 | O2D | O0 | definitions with opaque codes | 295 | 0.620 | 0.007 | 0.614 | 0.517 | 0.718 | 181 | 0 | 0.000 | 0.000 |
| adjudicated gold | qwen3:8b | E1 | L0 | O0 | meaningful identifiers over opaque codes | 295 | 0.417 | 0.007 | 0.410 | 0.287 | 0.567 | 121 | 0 | 0.000 | 0.000 |
| adjudicated gold | qwen3:8b | E2 | L2U | L2 | open versus closed output | 295 | 0.593 | 0.586 | 0.007 | 0.000 | 0.020 | 2 | 0 | 0.500 | 1.000 |
| adjudicated gold | qwen3:8b | R | L2S | L2 | shuffled versus grouped order of the cards | 295 | 0.546 | 0.586 | -0.041 | -0.126 | 0.078 | 24 | 36 | 0.155 | 1.000 |
| adjudicated gold | qwen3:8b | E5 | L3 | L2 | ten lexically retrieved cards versus all cards | 295 | 0.512 | 0.586 | -0.075 | -0.196 | 0.045 | 31 | 53 | 0.021 | 0.364 |
| adjudicated gold | qwen3:8b | E5 | L3E | L2 | ten densely retrieved cards versus all cards | 295 | 0.563 | 0.586 | -0.024 | -0.136 | 0.099 | 34 | 41 | 0.489 | 1.000 |
| adjudicated gold | qwen3:8b | E6 | XBR | L0 | Brick documentation over identifiers | 295 | 0.424 | 0.417 | 0.007 | -0.050 | 0.048 | 16 | 14 | 0.856 | 1.000 |
| adjudicated gold | qwen3:8b | E6 | XBE | L0 | BEDES documentation over identifiers | 295 | 0.475 | 0.417 | 0.058 | -0.011 | 0.123 | 29 | 12 | 0.012 | 0.207 |
| adjudicated gold | qwen3:8b | E6 | XEA | L0 | Energy ADE documentation over identifiers | 295 | 0.461 | 0.417 | 0.044 | -0.016 | 0.101 | 25 | 12 | 0.047 | 0.752 |
| adjudicated gold | qwen3:8b | E6 | XBR | L2 | Brick documentation versus UBEM-Link cards | 295 | 0.424 | 0.586 | -0.163 | -0.278 | -0.034 | 13 | 61 | 0.000 | 0.000 |
| adjudicated gold | qwen3:8b | E6 | XBE | L2 | BEDES documentation versus UBEM-Link cards | 295 | 0.475 | 0.586 | -0.112 | -0.183 | -0.023 | 13 | 46 | 0.000 | 0.000 |
| adjudicated gold | qwen3:8b | E6 | XEA | L2 | Energy ADE documentation versus UBEM-Link cards | 295 | 0.461 | 0.586 | -0.125 | -0.273 | 0.005 | 17 | 54 | 0.000 | 0.000 |
| annotator 1 alone | llama3.1:8b | E1 | L1 | L0 | labels over identifiers | 297 | 0.407 | 0.438 | -0.030 | -0.097 | 0.032 | 17 | 26 | 0.222 | 1.000 |
| annotator 1 alone | llama3.1:8b | E1 | L2D | L1 | definitions over labels | 297 | 0.532 | 0.407 | 0.125 | 0.007 | 0.256 | 52 | 15 | 0.000 | 0.000 |
| annotator 1 alone | llama3.1:8b | E1 | L2 | L2D | group, entity, unit and synonyms over definitions | 297 | 0.545 | 0.532 | 0.013 | -0.048 | 0.076 | 26 | 22 | 0.665 | 1.000 |
| annotator 1 alone | llama3.1:8b | E1 | L2N | L1 | group, entity, unit and synonyms over labels (no definitions) | 297 | 0.572 | 0.407 | 0.165 | 0.062 | 0.259 | 60 | 11 | 0.000 | 0.000 |
| annotator 1 alone | llama3.1:8b | E1 | L2 | L2N | definitions over the rest of the card | 297 | 0.545 | 0.572 | -0.027 | -0.119 | 0.079 | 24 | 32 | 0.350 | 1.000 |
| annotator 1 alone | llama3.1:8b | E1 | O2D | O0 | definitions with opaque codes | 297 | 0.549 | 0.020 | 0.529 | 0.379 | 0.651 | 160 | 3 | 0.000 | 0.000 |
| annotator 1 alone | llama3.1:8b | E1 | L0 | O0 | meaningful identifiers over opaque codes | 297 | 0.438 | 0.020 | 0.418 | 0.271 | 0.605 | 127 | 3 | 0.000 | 0.000 |
| annotator 1 alone | llama3.1:8b | E2 | L2U | L2 | open versus closed output | 297 | 0.532 | 0.545 | -0.013 | -0.029 | 0.000 | 0 | 4 | 0.125 | 1.000 |
| annotator 1 alone | llama3.1:8b | R | L2S | L2 | shuffled versus grouped order of the cards | 297 | 0.532 | 0.545 | -0.013 | -0.135 | 0.144 | 39 | 43 | 0.741 | 1.000 |
| annotator 1 alone | llama3.1:8b | E5 | L3 | L2 | ten lexically retrieved cards versus all cards | 297 | 0.525 | 0.545 | -0.020 | -0.104 | 0.123 | 39 | 45 | 0.586 | 1.000 |
| annotator 1 alone | llama3.1:8b | E5 | L3E | L2 | ten densely retrieved cards versus all cards | 297 | 0.603 | 0.545 | 0.057 | -0.083 | 0.212 | 57 | 40 | 0.104 | 1.000 |
| annotator 1 alone | llama3.1:8b | E6 | XBR | L0 | Brick documentation over identifiers | 297 | 0.360 | 0.438 | -0.077 | -0.137 | -0.013 | 9 | 32 | 0.000 | 0.009 |
| annotator 1 alone | llama3.1:8b | E6 | XBE | L0 | BEDES documentation over identifiers | 297 | 0.441 | 0.438 | 0.003 | -0.121 | 0.129 | 33 | 32 | 1.000 | 1.000 |
| annotator 1 alone | llama3.1:8b | E6 | XEA | L0 | Energy ADE documentation over identifiers | 297 | 0.428 | 0.438 | -0.010 | -0.080 | 0.052 | 25 | 28 | 0.784 | 1.000 |
| annotator 1 alone | llama3.1:8b | E6 | XBR | L2 | Brick documentation versus UBEM-Link cards | 297 | 0.360 | 0.545 | -0.185 | -0.299 | -0.055 | 11 | 66 | 0.000 | 0.000 |
| annotator 1 alone | llama3.1:8b | E6 | XBE | L2 | BEDES documentation versus UBEM-Link cards | 297 | 0.441 | 0.545 | -0.104 | -0.200 | -0.017 | 19 | 50 | 0.000 | 0.005 |
| annotator 1 alone | llama3.1:8b | E6 | XEA | L2 | Energy ADE documentation versus UBEM-Link cards | 297 | 0.428 | 0.545 | -0.118 | -0.264 | 0.004 | 24 | 59 | 0.000 | 0.004 |
| annotator 1 alone | qwen3:8b | E1 | L1 | L0 | labels over identifiers | 297 | 0.461 | 0.421 | 0.040 | -0.010 | 0.092 | 20 | 8 | 0.036 | 0.607 |
| annotator 1 alone | qwen3:8b | E1 | L2D | L1 | definitions over labels | 297 | 0.559 | 0.461 | 0.098 | 0.016 | 0.185 | 38 | 9 | 0.000 | 0.001 |
| annotator 1 alone | qwen3:8b | E1 | L2 | L2D | group, entity, unit and synonyms over definitions | 297 | 0.586 | 0.559 | 0.027 | -0.057 | 0.112 | 30 | 22 | 0.332 | 1.000 |
| annotator 1 alone | qwen3:8b | E1 | L2N | L1 | group, entity, unit and synonyms over labels (no definitions) | 297 | 0.529 | 0.461 | 0.067 | -0.021 | 0.175 | 34 | 14 | 0.006 | 0.110 |
| annotator 1 alone | qwen3:8b | E1 | L2 | L2N | definitions over the rest of the card | 297 | 0.586 | 0.529 | 0.057 | -0.027 | 0.121 | 30 | 13 | 0.014 | 0.247 |
| annotator 1 alone | qwen3:8b | E1 | O2D | O0 | definitions with opaque codes | 297 | 0.609 | 0.007 | 0.603 | 0.500 | 0.704 | 179 | 0 | 0.000 | 0.000 |
| annotator 1 alone | qwen3:8b | E1 | L0 | O0 | meaningful identifiers over opaque codes | 297 | 0.421 | 0.007 | 0.414 | 0.292 | 0.601 | 123 | 0 | 0.000 | 0.000 |
| annotator 1 alone | qwen3:8b | E2 | L2U | L2 | open versus closed output | 297 | 0.593 | 0.586 | 0.007 | 0.000 | 0.021 | 2 | 0 | 0.500 | 1.000 |
| annotator 1 alone | qwen3:8b | R | L2S | L2 | shuffled versus grouped order of the cards | 297 | 0.539 | 0.586 | -0.047 | -0.133 | 0.060 | 23 | 37 | 0.092 | 1.000 |
| annotator 1 alone | qwen3:8b | E5 | L3 | L2 | ten lexically retrieved cards versus all cards | 297 | 0.505 | 0.586 | -0.081 | -0.194 | 0.045 | 29 | 53 | 0.011 | 0.202 |
| annotator 1 alone | qwen3:8b | E5 | L3E | L2 | ten densely retrieved cards versus all cards | 297 | 0.569 | 0.586 | -0.017 | -0.132 | 0.112 | 34 | 39 | 0.640 | 1.000 |
| annotator 1 alone | qwen3:8b | E6 | XBR | L0 | Brick documentation over identifiers | 297 | 0.414 | 0.421 | -0.007 | -0.075 | 0.045 | 16 | 18 | 0.864 | 1.000 |
| annotator 1 alone | qwen3:8b | E6 | XBE | L0 | BEDES documentation over identifiers | 297 | 0.458 | 0.421 | 0.037 | -0.038 | 0.099 | 27 | 16 | 0.126 | 1.000 |
| annotator 1 alone | qwen3:8b | E6 | XEA | L0 | Energy ADE documentation over identifiers | 297 | 0.444 | 0.421 | 0.024 | -0.032 | 0.074 | 22 | 15 | 0.324 | 1.000 |
| annotator 1 alone | qwen3:8b | E6 | XBR | L2 | Brick documentation versus UBEM-Link cards | 297 | 0.414 | 0.586 | -0.172 | -0.286 | -0.048 | 10 | 61 | 0.000 | 0.000 |
| annotator 1 alone | qwen3:8b | E6 | XBE | L2 | BEDES documentation versus UBEM-Link cards | 297 | 0.458 | 0.586 | -0.128 | -0.196 | -0.053 | 10 | 48 | 0.000 | 0.000 |
| annotator 1 alone | qwen3:8b | E6 | XEA | L2 | Energy ADE documentation versus UBEM-Link cards | 297 | 0.444 | 0.586 | -0.141 | -0.264 | 0.000 | 14 | 56 | 0.000 | 0.000 |
| annotator 2 alone | llama3.1:8b | E1 | L1 | L0 | labels over identifiers | 296 | 0.395 | 0.436 | -0.041 | -0.112 | 0.021 | 17 | 29 | 0.104 | 1.000 |
| annotator 2 alone | llama3.1:8b | E1 | L2D | L1 | definitions over labels | 296 | 0.534 | 0.395 | 0.139 | 0.015 | 0.276 | 56 | 15 | 0.000 | 0.000 |
| annotator 2 alone | llama3.1:8b | E1 | L2 | L2D | group, entity, unit and synonyms over definitions | 296 | 0.537 | 0.534 | 0.003 | -0.071 | 0.069 | 27 | 26 | 1.000 | 1.000 |
| annotator 2 alone | llama3.1:8b | E1 | L2N | L1 | group, entity, unit and synonyms over labels (no definitions) | 296 | 0.568 | 0.395 | 0.172 | 0.058 | 0.273 | 62 | 11 | 0.000 | 0.000 |
| annotator 2 alone | llama3.1:8b | E1 | L2 | L2N | definitions over the rest of the card | 296 | 0.537 | 0.568 | -0.030 | -0.118 | 0.081 | 23 | 32 | 0.281 | 1.000 |
| annotator 2 alone | llama3.1:8b | E1 | O2D | O0 | definitions with opaque codes | 296 | 0.557 | 0.020 | 0.537 | 0.400 | 0.658 | 162 | 3 | 0.000 | 0.000 |
| annotator 2 alone | llama3.1:8b | E1 | L0 | O0 | meaningful identifiers over opaque codes | 296 | 0.436 | 0.020 | 0.416 | 0.265 | 0.596 | 126 | 3 | 0.000 | 0.000 |
| annotator 2 alone | llama3.1:8b | E2 | L2U | L2 | open versus closed output | 296 | 0.524 | 0.537 | -0.014 | -0.029 | 0.000 | 0 | 4 | 0.125 | 1.000 |
| annotator 2 alone | llama3.1:8b | R | L2S | L2 | shuffled versus grouped order of the cards | 296 | 0.554 | 0.537 | 0.017 | -0.106 | 0.174 | 45 | 40 | 0.665 | 1.000 |
| annotator 2 alone | llama3.1:8b | E5 | L3 | L2 | ten lexically retrieved cards versus all cards | 296 | 0.510 | 0.537 | -0.027 | -0.114 | 0.102 | 37 | 45 | 0.440 | 1.000 |
| annotator 2 alone | llama3.1:8b | E5 | L3E | L2 | ten densely retrieved cards versus all cards | 296 | 0.571 | 0.537 | 0.034 | -0.105 | 0.186 | 51 | 41 | 0.348 | 1.000 |
| annotator 2 alone | llama3.1:8b | E6 | XBR | L0 | Brick documentation over identifiers | 296 | 0.348 | 0.436 | -0.088 | -0.151 | -0.023 | 9 | 35 | 0.000 | 0.002 |
| annotator 2 alone | llama3.1:8b | E6 | XBE | L0 | BEDES documentation over identifiers | 296 | 0.426 | 0.436 | -0.010 | -0.137 | 0.106 | 32 | 35 | 0.807 | 1.000 |
| annotator 2 alone | llama3.1:8b | E6 | XEA | L0 | Energy ADE documentation over identifiers | 296 | 0.416 | 0.436 | -0.020 | -0.099 | 0.046 | 24 | 30 | 0.497 | 1.000 |
| annotator 2 alone | llama3.1:8b | E6 | XBR | L2 | Brick documentation versus UBEM-Link cards | 296 | 0.348 | 0.537 | -0.189 | -0.320 | -0.067 | 12 | 68 | 0.000 | 0.000 |
| annotator 2 alone | llama3.1:8b | E6 | XBE | L2 | BEDES documentation versus UBEM-Link cards | 296 | 0.426 | 0.537 | -0.111 | -0.212 | -0.016 | 18 | 51 | 0.000 | 0.002 |
| annotator 2 alone | llama3.1:8b | E6 | XEA | L2 | Energy ADE documentation versus UBEM-Link cards | 296 | 0.416 | 0.537 | -0.122 | -0.283 | 0.000 | 24 | 60 | 0.000 | 0.002 |
| annotator 2 alone | qwen3:8b | E1 | L1 | L0 | labels over identifiers | 296 | 0.476 | 0.422 | 0.054 | 0.004 | 0.099 | 24 | 8 | 0.007 | 0.127 |
| annotator 2 alone | qwen3:8b | E1 | L2D | L1 | definitions over labels | 296 | 0.554 | 0.476 | 0.078 | -0.010 | 0.161 | 37 | 14 | 0.002 | 0.035 |
| annotator 2 alone | qwen3:8b | E1 | L2 | L2D | group, entity, unit and synonyms over definitions | 296 | 0.588 | 0.554 | 0.034 | -0.052 | 0.118 | 32 | 22 | 0.220 | 1.000 |
| annotator 2 alone | qwen3:8b | E1 | L2N | L1 | group, entity, unit and synonyms over labels (no definitions) | 296 | 0.554 | 0.476 | 0.078 | -0.015 | 0.195 | 36 | 13 | 0.001 | 0.029 |
| annotator 2 alone | qwen3:8b | E1 | L2 | L2N | definitions over the rest of the card | 296 | 0.588 | 0.554 | 0.034 | -0.051 | 0.100 | 27 | 17 | 0.174 | 1.000 |
| annotator 2 alone | qwen3:8b | E1 | O2D | O0 | definitions with opaque codes | 296 | 0.622 | 0.007 | 0.615 | 0.514 | 0.703 | 182 | 0 | 0.000 | 0.000 |
| annotator 2 alone | qwen3:8b | E1 | L0 | O0 | meaningful identifiers over opaque codes | 296 | 0.422 | 0.007 | 0.416 | 0.286 | 0.583 | 123 | 0 | 0.000 | 0.000 |
| annotator 2 alone | qwen3:8b | E2 | L2U | L2 | open versus closed output | 296 | 0.595 | 0.588 | 0.007 | 0.000 | 0.020 | 2 | 0 | 0.500 | 1.000 |
| annotator 2 alone | qwen3:8b | R | L2S | L2 | shuffled versus grouped order of the cards | 296 | 0.551 | 0.588 | -0.037 | -0.124 | 0.088 | 25 | 36 | 0.200 | 1.000 |
| annotator 2 alone | qwen3:8b | E5 | L3 | L2 | ten lexically retrieved cards versus all cards | 296 | 0.500 | 0.588 | -0.088 | -0.205 | 0.039 | 30 | 56 | 0.007 | 0.127 |
| annotator 2 alone | qwen3:8b | E5 | L3E | L2 | ten densely retrieved cards versus all cards | 296 | 0.554 | 0.588 | -0.034 | -0.152 | 0.088 | 33 | 43 | 0.302 | 1.000 |
| annotator 2 alone | qwen3:8b | E6 | XBR | L0 | Brick documentation over identifiers | 296 | 0.429 | 0.422 | 0.007 | -0.052 | 0.050 | 16 | 14 | 0.856 | 1.000 |
| annotator 2 alone | qwen3:8b | E6 | XBE | L0 | BEDES documentation over identifiers | 296 | 0.483 | 0.422 | 0.061 | -0.014 | 0.132 | 31 | 13 | 0.010 | 0.163 |
| annotator 2 alone | qwen3:8b | E6 | XEA | L0 | Energy ADE documentation over identifiers | 296 | 0.466 | 0.422 | 0.044 | -0.015 | 0.104 | 25 | 12 | 0.047 | 0.752 |
| annotator 2 alone | qwen3:8b | E6 | XBR | L2 | Brick documentation versus UBEM-Link cards | 296 | 0.429 | 0.588 | -0.159 | -0.274 | -0.022 | 14 | 61 | 0.000 | 0.000 |
| annotator 2 alone | qwen3:8b | E6 | XBE | L2 | BEDES documentation versus UBEM-Link cards | 296 | 0.483 | 0.588 | -0.105 | -0.179 | -0.028 | 15 | 46 | 0.000 | 0.002 |
| annotator 2 alone | qwen3:8b | E6 | XEA | L2 | Energy ADE documentation versus UBEM-Link cards | 296 | 0.466 | 0.588 | -0.122 | -0.255 | 0.025 | 18 | 54 | 0.000 | 0.001 |
| rule-based draft (keyword rules) | llama3.1:8b | E1 | L1 | L0 | labels over identifiers | 277 | 0.375 | 0.397 | -0.022 | -0.086 | 0.041 | 16 | 22 | 0.418 | 1.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E1 | L2D | L1 | definitions over labels | 277 | 0.531 | 0.375 | 0.155 | 0.033 | 0.275 | 54 | 11 | 0.000 | 0.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E1 | L2 | L2D | group, entity, unit and synonyms over definitions | 277 | 0.534 | 0.531 | 0.004 | -0.061 | 0.077 | 24 | 23 | 1.000 | 1.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E1 | L2N | L1 | group, entity, unit and synonyms over labels (no definitions) | 277 | 0.563 | 0.375 | 0.188 | 0.071 | 0.276 | 62 | 10 | 0.000 | 0.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E1 | L2 | L2N | definitions over the rest of the card | 277 | 0.534 | 0.563 | -0.029 | -0.119 | 0.069 | 22 | 30 | 0.332 | 1.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E1 | O2D | O0 | definitions with opaque codes | 277 | 0.606 | 0.014 | 0.592 | 0.435 | 0.741 | 165 | 1 | 0.000 | 0.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E1 | L0 | O0 | meaningful identifiers over opaque codes | 277 | 0.397 | 0.014 | 0.383 | 0.259 | 0.552 | 107 | 1 | 0.000 | 0.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E2 | L2U | L2 | open versus closed output | 277 | 0.531 | 0.534 | -0.004 | -0.015 | 0.010 | 1 | 2 | 1.000 | 1.000 |
| rule-based draft (keyword rules) | llama3.1:8b | R | L2S | L2 | shuffled versus grouped order of the cards | 277 | 0.509 | 0.534 | -0.025 | -0.146 | 0.117 | 31 | 38 | 0.470 | 1.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E5 | L3 | L2 | ten lexically retrieved cards versus all cards | 277 | 0.534 | 0.534 | 0.000 | -0.080 | 0.124 | 38 | 38 | 1.000 | 1.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E5 | L3E | L2 | ten densely retrieved cards versus all cards | 277 | 0.574 | 0.534 | 0.040 | -0.114 | 0.171 | 47 | 36 | 0.272 | 1.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E6 | XBR | L0 | Brick documentation over identifiers | 277 | 0.347 | 0.397 | -0.051 | -0.115 | 0.023 | 12 | 26 | 0.034 | 0.604 |
| rule-based draft (keyword rules) | llama3.1:8b | E6 | XBE | L0 | BEDES documentation over identifiers | 277 | 0.430 | 0.397 | 0.032 | -0.085 | 0.152 | 35 | 26 | 0.306 | 1.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E6 | XEA | L0 | Energy ADE documentation over identifiers | 277 | 0.419 | 0.397 | 0.022 | -0.034 | 0.073 | 26 | 20 | 0.461 | 1.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E6 | XBR | L2 | Brick documentation versus UBEM-Link cards | 277 | 0.347 | 0.534 | -0.188 | -0.318 | -0.049 | 13 | 65 | 0.000 | 0.000 |
| rule-based draft (keyword rules) | llama3.1:8b | E6 | XBE | L2 | BEDES documentation versus UBEM-Link cards | 277 | 0.430 | 0.534 | -0.105 | -0.189 | -0.023 | 19 | 48 | 0.001 | 0.011 |
| rule-based draft (keyword rules) | llama3.1:8b | E6 | XEA | L2 | Energy ADE documentation versus UBEM-Link cards | 277 | 0.419 | 0.534 | -0.116 | -0.249 | 0.000 | 22 | 54 | 0.000 | 0.007 |
| rule-based draft (keyword rules) | qwen3:8b | E1 | L1 | L0 | labels over identifiers | 277 | 0.412 | 0.379 | 0.032 | -0.023 | 0.081 | 18 | 9 | 0.122 | 1.000 |
| rule-based draft (keyword rules) | qwen3:8b | E1 | L2D | L1 | definitions over labels | 277 | 0.531 | 0.412 | 0.119 | 0.023 | 0.198 | 42 | 9 | 0.000 | 0.000 |
| rule-based draft (keyword rules) | qwen3:8b | E1 | L2 | L2D | group, entity, unit and synonyms over definitions | 277 | 0.574 | 0.531 | 0.043 | -0.044 | 0.134 | 29 | 17 | 0.104 | 1.000 |
| rule-based draft (keyword rules) | qwen3:8b | E1 | L2N | L1 | group, entity, unit and synonyms over labels (no definitions) | 277 | 0.505 | 0.412 | 0.094 | 0.010 | 0.228 | 36 | 10 | 0.000 | 0.004 |
| rule-based draft (keyword rules) | qwen3:8b | E1 | L2 | L2N | definitions over the rest of the card | 277 | 0.574 | 0.505 | 0.069 | 0.000 | 0.124 | 29 | 10 | 0.003 | 0.068 |
| rule-based draft (keyword rules) | qwen3:8b | E1 | O2D | O0 | definitions with opaque codes | 277 | 0.632 | 0.007 | 0.625 | 0.513 | 0.739 | 173 | 0 | 0.000 | 0.000 |
| rule-based draft (keyword rules) | qwen3:8b | E1 | L0 | O0 | meaningful identifiers over opaque codes | 277 | 0.379 | 0.007 | 0.372 | 0.242 | 0.535 | 103 | 0 | 0.000 | 0.000 |
| rule-based draft (keyword rules) | qwen3:8b | E2 | L2U | L2 | open versus closed output | 277 | 0.578 | 0.574 | 0.004 | -0.010 | 0.020 | 2 | 1 | 1.000 | 1.000 |
| rule-based draft (keyword rules) | qwen3:8b | R | L2S | L2 | shuffled versus grouped order of the cards | 277 | 0.523 | 0.574 | -0.051 | -0.129 | 0.050 | 21 | 35 | 0.081 | 1.000 |
| rule-based draft (keyword rules) | qwen3:8b | E5 | L3 | L2 | ten lexically retrieved cards versus all cards | 277 | 0.534 | 0.574 | -0.040 | -0.171 | 0.075 | 37 | 48 | 0.278 | 1.000 |
| rule-based draft (keyword rules) | qwen3:8b | E5 | L3E | L2 | ten densely retrieved cards versus all cards | 277 | 0.556 | 0.574 | -0.018 | -0.123 | 0.088 | 29 | 34 | 0.615 | 1.000 |
| rule-based draft (keyword rules) | qwen3:8b | E6 | XBR | L0 | Brick documentation over identifiers | 277 | 0.390 | 0.379 | 0.011 | -0.035 | 0.054 | 15 | 12 | 0.701 | 1.000 |
| rule-based draft (keyword rules) | qwen3:8b | E6 | XBE | L0 | BEDES documentation over identifiers | 277 | 0.433 | 0.379 | 0.054 | -0.020 | 0.118 | 26 | 11 | 0.020 | 0.381 |
| rule-based draft (keyword rules) | qwen3:8b | E6 | XEA | L0 | Energy ADE documentation over identifiers | 277 | 0.412 | 0.379 | 0.032 | -0.039 | 0.102 | 22 | 13 | 0.175 | 1.000 |
| rule-based draft (keyword rules) | qwen3:8b | E6 | XBR | L2 | Brick documentation versus UBEM-Link cards | 277 | 0.390 | 0.574 | -0.184 | -0.288 | -0.068 | 9 | 60 | 0.000 | 0.000 |
| rule-based draft (keyword rules) | qwen3:8b | E6 | XBE | L2 | BEDES documentation versus UBEM-Link cards | 277 | 0.433 | 0.574 | -0.141 | -0.197 | -0.084 | 7 | 46 | 0.000 | 0.000 |
| rule-based draft (keyword rules) | qwen3:8b | E6 | XEA | L2 | Energy ADE documentation versus UBEM-Link cards | 277 | 0.412 | 0.574 | -0.162 | -0.288 | -0.027 | 9 | 54 | 0.000 | 0.000 |

## S8. Run-to-run variation (temperature 0.7 runs only)



| model | condition | runs_T0.7 | acc_T0 | acc_T0.7_mean | acc_T0.7_sd | pairwise_agreement_T0.7_min | pairwise_agreement_T0.7_max |
|---|---|---|---|---|---|---|---|
| llama3.1:8b | L0 | 4 | 0.427 | 0.433 | 0.013 | 0.697 | 0.893 |
| llama3.1:8b | L1 | 4 | 0.397 | 0.382 | 0.013 | 0.800 | 0.903 |
| llama3.1:8b | L2 | 4 | 0.546 | 0.534 | 0.010 | 0.843 | 0.963 |
| llama3.1:8b | L3 | 4 | 0.522 | 0.511 | 0.014 | 0.873 | 0.950 |
| qwen3:8b | L0 | 4 | 0.417 | 0.415 | 0.002 | 0.970 | 0.993 |
| qwen3:8b | L1 | 4 | 0.471 | 0.472 | 0.003 | 0.960 | 1.000 |
| qwen3:8b | L2 | 4 | 0.586 | 0.588 | 0.002 | 0.957 | 0.997 |
| qwen3:8b | L3 | 4 | 0.512 | 0.512 | 0.003 | 0.967 | 1.000 |

## S9. Accuracy with and without lexical overlap between the variable label and the gold concept

Overlap: the label contains the concept's label or one of its synonyms.

| model | condition | n_overlap | n_no_overlap | acc_overlap | acc_no_overlap |
|---|---|---|---|---|---|
| llama3.1:8b | L0 | 71 | 224 | 0.732 | 0.330 |
| llama3.1:8b | L1 | 71 | 224 | 0.718 | 0.295 |
| llama3.1:8b | L2D | 71 | 224 | 0.789 | 0.442 |
| llama3.1:8b | L2 | 71 | 224 | 0.761 | 0.478 |
| llama3.1:8b | L2N | 71 | 224 | 0.803 | 0.504 |
| llama3.1:8b | O0 | 71 | 224 | 0.028 | 0.018 |
| llama3.1:8b | O2D | 71 | 224 | 0.704 | 0.504 |
| llama3.1:8b | L2S | 71 | 224 | 0.662 | 0.509 |
| llama3.1:8b | L2U | 71 | 224 | 0.746 | 0.464 |
| llama3.1:8b | L3 | 71 | 224 | 0.803 | 0.433 |
| llama3.1:8b | L3E | 71 | 224 | 0.845 | 0.500 |
| llama3.1:8b | XBR | 71 | 224 | 0.704 | 0.237 |
| llama3.1:8b | XBE | 71 | 224 | 0.648 | 0.357 |
| llama3.1:8b | XEA | 71 | 224 | 0.704 | 0.330 |
| qwen3:8b | L0 | 71 | 224 | 0.676 | 0.335 |
| qwen3:8b | L1 | 71 | 224 | 0.676 | 0.406 |
| qwen3:8b | L2D | 71 | 224 | 0.775 | 0.478 |
| qwen3:8b | L2 | 71 | 224 | 0.803 | 0.518 |
| qwen3:8b | L2N | 71 | 224 | 0.789 | 0.478 |
| qwen3:8b | O0 | 71 | 224 | 0.028 | 0.000 |
| qwen3:8b | O2D | 71 | 224 | 0.718 | 0.589 |
| qwen3:8b | L2S | 71 | 224 | 0.817 | 0.460 |
| qwen3:8b | L2U | 71 | 224 | 0.817 | 0.522 |
| qwen3:8b | L3 | 71 | 224 | 0.817 | 0.415 |
| qwen3:8b | L3E | 71 | 224 | 0.775 | 0.496 |
| qwen3:8b | XBR | 71 | 224 | 0.704 | 0.335 |
| qwen3:8b | XBE | 71 | 224 | 0.648 | 0.420 |
| qwen3:8b | XEA | 71 | 224 | 0.676 | 0.393 |

## S10. Documentation transplant by SKOS relation of the transplanted term



| model | standard | relation | n_variables | concepts | acc_standard_docs | acc_ubem_link_cards | acc_ids_only |
|---|---|---|---|---|---|---|---|
| llama3.1:8b | brick | exact or close match | 24 | 7 | 0.792 | 0.792 | 0.833 |
| llama3.1:8b | brick | broad, narrow or related match | 87 | 12 | 0.517 | 0.552 | 0.586 |
| llama3.1:8b | bedes | exact or close match | 133 | 16 | 0.534 | 0.594 | 0.414 |
| llama3.1:8b | bedes | broad, narrow or related match | 137 | 22 | 0.365 | 0.533 | 0.453 |
| llama3.1:8b | energy_ade | exact or close match | 94 | 9 | 0.383 | 0.564 | 0.415 |
| llama3.1:8b | energy_ade | broad, narrow or related match | 74 | 10 | 0.324 | 0.405 | 0.297 |
| qwen3:8b | brick | exact or close match | 24 | 7 | 0.708 | 0.625 | 0.625 |
| qwen3:8b | brick | broad, narrow or related match | 87 | 12 | 0.644 | 0.678 | 0.586 |
| qwen3:8b | bedes | exact or close match | 133 | 16 | 0.511 | 0.632 | 0.414 |
| qwen3:8b | bedes | broad, narrow or related match | 137 | 22 | 0.409 | 0.555 | 0.380 |
| qwen3:8b | energy_ade | exact or close match | 94 | 9 | 0.298 | 0.415 | 0.202 |
| qwen3:8b | energy_ade | broad, narrow or related match | 74 | 10 | 0.338 | 0.554 | 0.378 |

## S11. Quantity-kind checks on mappings (E4), strict and lenient error basis



| model | basis | wrong | wrong_flagged | recall_pct | correct | correct_flagged | false_alarm_pct | precision_pct |
|---|---|---|---|---|---|---|---|---|
| llama3.1:8b | strict, 295 mappable variables | 134 | 7 | 5.224 | 161 | 4 | 2.484 | 63.636 |
| llama3.1:8b | lenient, all 300 variables | 110 | 7 | 6.364 | 190 | 4 | 2.105 | 63.636 |
| qwen3:8b | strict, 295 mappable variables | 122 | 20 | 16.393 | 173 | 4 | 2.312 | 83.333 |
| qwen3:8b | lenient, all 300 variables | 96 | 20 | 20.833 | 204 | 4 | 1.961 | 83.333 |

## S12. Profile checks on the national pipeline profiles (E7)



| temperature | class | profiles | flagged_v1 | flagged_v2 |
|---|---|---|---|---|
| 0.0 | changes an indicator | 4 | 4 | 3 |
| 0.0 | deviates, no effect on indicators | 22 | 14 | 11 |
| 0.0 | identical to gold | 18 | 0 | 0 |
| 0.7 | changes an indicator | 7 | 7 | 7 |
| 0.7 | deviates, no effect on indicators | 18 | 14 | 6 |
| 0.7 | identical to gold | 19 | 0 | 0 |
| all | changes an indicator | 11 | 11 | 10 |
| all | deviates, no effect on indicators | 40 | 28 | 17 |
| all | identical to gold | 37 | 0 | 0 |

## S13. Every E7 profile that changed a national indicator



| model | condition | dataset | variable | fields_wrong | max_effect_pct | flags | ai_profile |
|---|---|---|---|---|---|---|---|
| qwen3:8b | codebook entry only | cbecs2018 | ELBTU | unit_multiplier; missing_codes | 99900.000 | multiplier disagrees with label; missing code 'Not applicable' not in code list; missing code 'no_thought' not in code list | {'is_weight': False, 'unit': 'unit:BTU_IT', 'unit_multiplier': 1000000, 'missing_codes': ['Not applicable', 'no_thought' |
| qwen3:8b | codebook entry only, T=0.7 run 2 | recs2020 | BTUNG | missing_codes | 64.962 | missing code '0' inside the valid range | {'is_weight': False, 'unit': 'unit:BTU_IT', 'unit_multiplier': 1000, 'missing_codes': ['0']} |
| llama3.1:8b | codebook entry only | cbecs2018 | PUBCLIM | missing_codes | 2.454 | missing code '7=Withheld for confidentiality' not in code list | {'is_weight': False, 'unit': 'none', 'unit_multiplier': 0, 'missing_codes': ['7=Withheld for confidentiality']} |
| llama3.1:8b | codebook entry only | recs2020 | BTUNG | missing_codes | 64.962 | missing code '0' inside the valid range | {'is_weight': False, 'unit': 'unit:BTU_IT', 'unit_multiplier': 1000, 'missing_codes': ['0']} |
| llama3.1:8b | with dataset card | cbecs2018 | PUBCLIM | missing_codes | 100.000 | missing code '5' is a substantive category | {'is_weight': False, 'unit': 'none', 'unit_multiplier': 0, 'missing_codes': ['', '5']} |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | recs2020 | TOTALBTU | unit; unit_multiplier | 241.214 | unit disagrees with label; multiplier disagrees with label | {'is_weight': False, 'unit': 'unit:KiloW-HR', 'unit_multiplier': 0, 'missing_codes': ['']} |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | recs2020 | BTUEL | unit_multiplier; missing_codes | 100.000 | multiplier disagrees with label; missing code 'Missing=...' is not a code | {'is_weight': False, 'unit': 'unit:BTU_IT', 'unit_multiplier': 0.001, 'missing_codes': ['Missing=...']} |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | recs2020 | BTUNG | missing_codes | 64.962 | missing code '0' inside the valid range | {'is_weight': False, 'unit': 'unit:BTU_IT', 'unit_multiplier': 1000, 'missing_codes': ['0']} |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | recs2020 | TOTALBTU | unit; missing_codes | 341114.163 | unit disagrees with label; missing code 'NA' is not a code; missing code 'NA' is not a code; missing code 'NA' is not a code | {'is_weight': False, 'unit': 'unit:KiloW-HR', 'unit_multiplier': 1000, 'missing_codes': ['NA', 'NA', 'NA']} |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | recs2020 | BTUEL | unit; unit_multiplier; missing_codes | 241.214 | unit disagrees with label; multiplier disagrees with label; missing code 'N/A' is not a code; missing code 'NA' is not a code | {'is_weight': False, 'unit': 'unit:KiloW-HR', 'unit_multiplier': 0, 'missing_codes': ['', 'N/A', 'NA', '-1', '-9', '-99' |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | recs2020 | BTUNG | missing_codes | 64.962 | missing code '0' inside the valid range | {'is_weight': False, 'unit': 'unit:BTU_IT', 'unit_multiplier': 1000, 'missing_codes': ['0']} |

## S14. Profile checks on all benchmark normalization outputs

Excludes the 11 variables the version 1 rules were written on. Version 2 results on these data are in-sample.

| rules | model | temperature | profiles | unit_or_multiplier_errors | flagged_pct_of_those | missing_code_errors_only | flagged_pct_of_missing_code_errors | correct_profiles | false_alarm_pct |
|---|---|---|---|---|---|---|---|---|---|
| v1 (frozen, held-out) | llama3.1:8b | 0.000 | 766 | 21 | 33.333 | 523 | 90.440 | 222 | 28.378 |
| v1 (frozen, held-out) | llama3.1:8b | 0.700 | 766 | 44 | 79.545 | 547 | 94.333 | 175 | 17.143 |
| v1 (frozen, held-out) | qwen3:8b | 0.000 | 766 | 13 | 15.385 | 265 | 58.113 | 488 | 13.525 |
| v1 (frozen, held-out) | qwen3:8b | 0.700 | 766 | 8 | 25.000 | 332 | 60.241 | 426 | 15.728 |
| v2 (revised, in-sample) | llama3.1:8b | 0.000 | 766 | 21 | 52.381 | 523 | 33.461 | 222 | 0.000 |
| v2 (revised, in-sample) | llama3.1:8b | 0.700 | 766 | 44 | 88.636 | 547 | 40.219 | 175 | 0.000 |
| v2 (revised, in-sample) | qwen3:8b | 0.000 | 766 | 13 | 38.462 | 265 | 41.887 | 488 | 0.000 |
| v2 (revised, in-sample) | qwen3:8b | 0.700 | 766 | 8 | 25.000 | 332 | 55.723 | 426 | 0.000 |

## S15. National indicators: reference values and design-based standard errors

Replicate-weight variance as specified by EIA: CBECS 2018, 151 jackknife replicates with coefficient 1; RECS 2020, 60 jackknife replicates with coefficient 59/60.

| dataset | quantity | reference | se | rse_pct |
|---|---|---|---|---|
| cbecs2018 | Buildings (thousand) | 5918.211 | 232.829 | 3.934 |
| cbecs2018 | Floor area (million m2) | 8967.670 | 273.007 | 3.044 |
| cbecs2018 | EUI, major fuels (kWh/m2) | 221.885 | 4.044 | 1.822 |
| cbecs2018 | EUI, electricity (kWh/m2) | 133.422 | 2.755 | 2.065 |
| cbecs2018 | EUI, natural gas (kWh/m2) | 75.202 | 2.159 | 2.871 |
| cbecs2018 | Share in hot or very hot zone (%) | 13.830 | 2.503 | 18.097 |
| recs2020 | Households (million) | 123.529 | 0.000 | 0.000 |
| recs2020 | Site energy per household (MWh) | 22.494 | 0.091 | 0.405 |
| recs2020 | Electricity per household (MWh) | 10.565 | 0.040 | 0.377 |
| recs2020 | Natural gas per household (MWh) | 10.061 | 0.091 | 0.908 |
| recs2020 | Site EUI (kWh/m2) | 133.126 | 0.568 | 0.427 |

## S16. National indicators from AI-built profiles at all temperatures



| model | condition | dataset | quantity | reference | ai_pipeline | rel_error_pct |
|---|---|---|---|---|---|---|
| qwen3:8b | codebook entry only | cbecs2018 | Buildings (thousand) | 5918.211 | 5918.211 | 0.000 |
| qwen3:8b | codebook entry only | cbecs2018 | Floor area (million m2) | 8967.670 | 8967.670 | 0.000 |
| qwen3:8b | codebook entry only | cbecs2018 | EUI, major fuels (kWh/m2) | 221.885 | 221.885 | 0.000 |
| qwen3:8b | codebook entry only | cbecs2018 | EUI, electricity (kWh/m2) | 133.422 | 133421.631 | 99900.000 |
| qwen3:8b | codebook entry only | cbecs2018 | EUI, natural gas (kWh/m2) | 75.202 | 75.202 | 0.000 |
| qwen3:8b | codebook entry only | cbecs2018 | Share in hot or very hot zone (%) | 13.830 | 13.830 | 0.000 |
| qwen3:8b | codebook entry only | recs2020 | Households (million) | 123.529 | 123.529 | 0.000 |
| qwen3:8b | codebook entry only | recs2020 | Site energy per household (MWh) | 22.494 | 22.494 | 0.000 |
| qwen3:8b | codebook entry only | recs2020 | Electricity per household (MWh) | 10.565 | 10.565 | 0.000 |
| qwen3:8b | codebook entry only | recs2020 | Natural gas per household (MWh) | 10.061 | 10.061 | 0.000 |
| qwen3:8b | codebook entry only | recs2020 | Site EUI (kWh/m2) | 133.126 | 133.126 | 0.000 |
| qwen3:8b | with dataset card | cbecs2018 | Buildings (thousand) | 5918.211 | 5918.211 | 0.000 |
| qwen3:8b | with dataset card | cbecs2018 | Floor area (million m2) | 8967.670 | 8967.670 | 0.000 |
| qwen3:8b | with dataset card | cbecs2018 | EUI, major fuels (kWh/m2) | 221.885 | 221.885 | 0.000 |
| qwen3:8b | with dataset card | cbecs2018 | EUI, electricity (kWh/m2) | 133.422 | 133.422 | 0.000 |
| qwen3:8b | with dataset card | cbecs2018 | EUI, natural gas (kWh/m2) | 75.202 | 75.202 | 0.000 |
| qwen3:8b | with dataset card | cbecs2018 | Share in hot or very hot zone (%) | 13.830 | 13.830 | 0.000 |
| qwen3:8b | with dataset card | recs2020 | Households (million) | 123.529 | 123.529 | 0.000 |
| qwen3:8b | with dataset card | recs2020 | Site energy per household (MWh) | 22.494 | 22.494 | 0.000 |
| qwen3:8b | with dataset card | recs2020 | Electricity per household (MWh) | 10.565 | 10.565 | 0.000 |
| qwen3:8b | with dataset card | recs2020 | Natural gas per household (MWh) | 10.061 | 10.061 | 0.000 |
| qwen3:8b | with dataset card | recs2020 | Site EUI (kWh/m2) | 133.126 | 133.126 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | Buildings (thousand) | 5918.211 | 5918.211 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | Floor area (million m2) | 8967.670 | 8967.670 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | EUI, major fuels (kWh/m2) | 221.885 | 221.885 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | EUI, electricity (kWh/m2) | 133.422 | 133.422 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | EUI, natural gas (kWh/m2) | 75.202 | 75.202 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | Share in hot or very hot zone (%) | 13.830 | 13.830 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 1 | recs2020 | Households (million) | 123.529 | 123.529 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 1 | recs2020 | Site energy per household (MWh) | 22.494 | 22.494 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 1 | recs2020 | Electricity per household (MWh) | 10.565 | 10.565 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 1 | recs2020 | Natural gas per household (MWh) | 10.061 | 10.061 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 1 | recs2020 | Site EUI (kWh/m2) | 133.126 | 133.126 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | Buildings (thousand) | 5918.211 | 5918.211 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | Floor area (million m2) | 8967.670 | 8967.670 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | EUI, major fuels (kWh/m2) | 221.885 | 221.885 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | EUI, electricity (kWh/m2) | 133.422 | 133.422 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | EUI, natural gas (kWh/m2) | 75.202 | 75.202 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | Share in hot or very hot zone (%) | 13.830 | 13.830 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 2 | recs2020 | Households (million) | 123.529 | 123.529 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 2 | recs2020 | Site energy per household (MWh) | 22.494 | 22.494 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 2 | recs2020 | Electricity per household (MWh) | 10.565 | 10.565 | 0.000 |
| qwen3:8b | codebook entry only, T=0.7 run 2 | recs2020 | Natural gas per household (MWh) | 10.061 | 16.597 | 64.962 |
| qwen3:8b | codebook entry only, T=0.7 run 2 | recs2020 | Site EUI (kWh/m2) | 133.126 | 133.126 | 0.000 |
| llama3.1:8b | codebook entry only | cbecs2018 | Buildings (thousand) | 5918.211 | 5918.211 | 0.000 |
| llama3.1:8b | codebook entry only | cbecs2018 | Floor area (million m2) | 8967.670 | 8967.670 | 0.000 |
| llama3.1:8b | codebook entry only | cbecs2018 | EUI, major fuels (kWh/m2) | 221.885 | 221.885 | 0.000 |
| llama3.1:8b | codebook entry only | cbecs2018 | EUI, electricity (kWh/m2) | 133.422 | 133.422 | 0.000 |
| llama3.1:8b | codebook entry only | cbecs2018 | EUI, natural gas (kWh/m2) | 75.202 | 75.202 | -0.000 |
| llama3.1:8b | codebook entry only | cbecs2018 | Share in hot or very hot zone (%) | 13.830 | 13.491 | -2.454 |
| llama3.1:8b | codebook entry only | recs2020 | Households (million) | 123.529 | 123.529 | 0.000 |
| llama3.1:8b | codebook entry only | recs2020 | Site energy per household (MWh) | 22.494 | 22.494 | 0.000 |
| llama3.1:8b | codebook entry only | recs2020 | Electricity per household (MWh) | 10.565 | 10.565 | 0.000 |
| llama3.1:8b | codebook entry only | recs2020 | Natural gas per household (MWh) | 10.061 | 16.597 | 64.962 |
| llama3.1:8b | codebook entry only | recs2020 | Site EUI (kWh/m2) | 133.126 | 133.126 | 0.000 |
| llama3.1:8b | with dataset card | cbecs2018 | Buildings (thousand) | 5918.211 | 5918.211 | 0.000 |
| llama3.1:8b | with dataset card | cbecs2018 | Floor area (million m2) | 8967.670 | 8967.670 | 0.000 |
| llama3.1:8b | with dataset card | cbecs2018 | EUI, major fuels (kWh/m2) | 221.885 | 221.885 | -0.000 |
| llama3.1:8b | with dataset card | cbecs2018 | EUI, electricity (kWh/m2) | 133.422 | 133.422 | -0.000 |
| llama3.1:8b | with dataset card | cbecs2018 | EUI, natural gas (kWh/m2) | 75.202 | 75.202 | -0.000 |
| llama3.1:8b | with dataset card | cbecs2018 | Share in hot or very hot zone (%) | 13.830 | 0.000 | -100.000 |
| llama3.1:8b | with dataset card | recs2020 | Households (million) | 123.529 | 123.529 | 0.000 |
| llama3.1:8b | with dataset card | recs2020 | Site energy per household (MWh) | 22.494 | 22.494 | 0.000 |
| llama3.1:8b | with dataset card | recs2020 | Electricity per household (MWh) | 10.565 | 10.565 | 0.000 |
| llama3.1:8b | with dataset card | recs2020 | Natural gas per household (MWh) | 10.061 | 10.061 | 0.000 |
| llama3.1:8b | with dataset card | recs2020 | Site EUI (kWh/m2) | 133.126 | 133.126 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | Buildings (thousand) | 5918.211 | 5918.211 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | Floor area (million m2) | 8967.670 | 8967.670 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | EUI, major fuels (kWh/m2) | 221.885 | 221.885 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | EUI, electricity (kWh/m2) | 133.422 | 133.422 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | EUI, natural gas (kWh/m2) | 75.202 | 75.202 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | cbecs2018 | Share in hot or very hot zone (%) | 13.830 | 13.830 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | recs2020 | Households (million) | 123.529 | 123.529 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | recs2020 | Site energy per household (MWh) | 22.494 | 76.753 | 241.214 |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | recs2020 | Electricity per household (MWh) | 10.565 | 0.000 | -100.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | recs2020 | Natural gas per household (MWh) | 10.061 | 16.597 | 64.962 |
| llama3.1:8b | codebook entry only, T=0.7 run 1 | recs2020 | Site EUI (kWh/m2) | 133.126 | 454.243 | 241.214 |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | Buildings (thousand) | 5918.211 | 5918.211 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | Floor area (million m2) | 8967.670 | 8967.670 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | EUI, major fuels (kWh/m2) | 221.885 | 221.885 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | EUI, electricity (kWh/m2) | 133.422 | 133.422 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | EUI, natural gas (kWh/m2) | 75.202 | 75.202 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | cbecs2018 | Share in hot or very hot zone (%) | 13.830 | 13.830 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | recs2020 | Households (million) | 123.529 | 123.529 | 0.000 |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | recs2020 | Site energy per household (MWh) | 22.494 | 76752.754 | 341114.163 |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | recs2020 | Electricity per household (MWh) | 10.565 | 36.051 | 241.214 |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | recs2020 | Natural gas per household (MWh) | 10.061 | 16.597 | 64.962 |
| llama3.1:8b | codebook entry only, T=0.7 run 2 | recs2020 | Site EUI (kWh/m2) | 133.126 | 454243.067 | 341114.163 |

## S17. Top-code sensitivity (CBECS 2018 floors)



| assumption | code_994 | code_995 | weighted_mean_floors | codes_read_as_numbers | relative_error_pct |
|---|---|---|---|---|---|
| lower bounds | 10 | 15 | 1.461 | 4.082 | 179.494 |
| midpoint, lower bound (paper's central case) | 12 | 15 | 1.464 | 4.082 | 178.887 |
| upper bound, 20 floors | 14 | 20 | 1.472 | 4.082 | 177.263 |
| upper bound, 30 floors | 14 | 30 | 1.483 | 4.082 | 175.245 |

## S18. Effect of single normalization errors on CBECS 2018 quantities



| t3_error_type | quantity | correct | with_error | rel_error_pct |
|---|---|---|---|---|
| unit multiplier dropped (thousand Btu read as Btu) | national EUI [kWh/m2] | 221.885 | 0.222 | -99.900 |
| wrong unit (thousand Btu read as kWh) | national EUI [kWh/m2] | 221.885 | 757.101 | 241.214 |
| ft2 read as m2 | total floorspace [million m2] | 8967.670 | 96527.197 | 976.391 |
| top-codes read as values (NFLOOR 994/995) | weighted mean floors | 1.464 | 4.082 | 178.887 |
| withheld code kept as data (PUBCLIM 7) | share of buildings in hot/very hot zone | 0.138 | 0.135 | -2.454 |
| survey weights ignored | number of buildings [thousand] | 5918.211 | 6.436 | -99.891 |

## S19. City case: columns selected by the models

The tax-lot key is described by the JoinKey value parcel_id. Correct columns per role are listed in ubem_link.city.ROLES; for floor area, the variants with and without parking are accepted.

| model | selection | card | role | column | correct | confidence |
|---|---|---|---|---|---|---|
| qwen3:8b | L0 | False | bbl | nyc_building_identification | False | 0.900 |
| qwen3:8b | L0 | False | area | property_gfa_calculated | True | 1.000 |
| qwen3:8b | L0 | False | site | site_energy_use_kbtu | True | 1.000 |
| qwen3:8b | L0 | False | elec | electricity_weather_normalized_1 | False | 1.000 |
| qwen3:8b | L0 | False | gas | natural_gas_weather_normalized_1 | False | 1.000 |
| qwen3:8b | L0 | False | pluto_bbl | bbl | True |  |
| qwen3:8b | L0 | True | bbl | nyc_building_identification | False | 0.900 |
| qwen3:8b | L0 | True | area | property_gfa_calculated | True | 1.000 |
| qwen3:8b | L0 | True | site | site_energy_use_kbtu | True | 1.000 |
| qwen3:8b | L0 | True | elec | electricity_weather_normalized_1 | False | 1.000 |
| qwen3:8b | L0 | True | gas | natural_gas_weather_normalized_1 | False | 1.000 |
| qwen3:8b | L0 | True | pluto_bbl | bbl | True |  |
| qwen3:8b | L2 | False | bbl | nyc_borough_block_and_lot | True | 0.950 |
| qwen3:8b | L2 | False | area | property_gfa_calculated | True | 1.000 |
| qwen3:8b | L2 | False | site | site_energy_use_kbtu | True | 1.000 |
| qwen3:8b | L2 | False | elec | electricity_use_grid_purchase_1 | True | 0.950 |
| qwen3:8b | L2 | False | gas | natural_gas_use_kbtu | True | 0.950 |
| qwen3:8b | L2 | False | pluto_bbl | bbl | True |  |
| qwen3:8b | L2 | True | bbl | nyc_borough_block_and_lot | True | 0.950 |
| qwen3:8b | L2 | True | area | property_gfa_calculated | True | 1.000 |
| qwen3:8b | L2 | True | site | site_energy_use_kbtu | True | 1.000 |
| qwen3:8b | L2 | True | elec | electricity_use_grid_purchase_1 | True | 0.950 |
| qwen3:8b | L2 | True | gas | natural_gas_use_kbtu | True | 0.950 |
| qwen3:8b | L2 | True | pluto_bbl | bbl | True |  |
| llama3.1:8b | L0 | False | bbl | nyc_borough_block_and_lot | True | 1.000 |
| llama3.1:8b | L0 | False | area | largest_property_use_type_1 | False | 0.900 |
| llama3.1:8b | L0 | False | site | site_eui_kbtu_ft | False | 1.000 |
| llama3.1:8b | L0 | False | elec | electricity_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L0 | False | gas | natural_gas_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L0 | False | pluto_bbl | bbl | True |  |
| llama3.1:8b | L0 | True | bbl | nyc_borough_block_and_lot | True | 1.000 |
| llama3.1:8b | L0 | True | area | largest_property_use_type_1 | False | 0.900 |
| llama3.1:8b | L0 | True | site | site_eui_kbtu_ft | False | 1.000 |
| llama3.1:8b | L0 | True | elec | electricity_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L0 | True | gas | natural_gas_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L0 | True | pluto_bbl | bbl | True |  |
| llama3.1:8b | L2 | False | bbl | nyc_borough_block_and_lot | True | 1.000 |
| llama3.1:8b | L2 | False | area | property_gfa_calculated | True | 0.900 |
| llama3.1:8b | L2 | False | site | site_energy_use_kbtu | True | 0.900 |
| llama3.1:8b | L2 | False | elec | electricity_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L2 | False | gas | natural_gas_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L2 | False | pluto_bbl | bbl | True |  |
| llama3.1:8b | L2 | True | bbl | nyc_borough_block_and_lot | True | 1.000 |
| llama3.1:8b | L2 | True | area | property_gfa_calculated | True | 0.900 |
| llama3.1:8b | L2 | True | site | site_energy_use_kbtu | True | 0.900 |
| llama3.1:8b | L2 | True | elec | electricity_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L2 | True | gas | natural_gas_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L2 | True | pluto_bbl | bbl | True |  |

## S20. City case: AI-built profiles and profile checks

Second table: every distinct profile of the city runs. Error: a wrong conversion to SI units, a unit given to a column that has none in the vocabulary (an intensity), or a numeric missing code that occurs in the data. Rows with source 'post hoc units' come from the exploratory variant whose unit vocabulary also offers kBtu and therms, which version 2 of the checks does not know; they are not part of the held-out evaluation.

| model | selection | card | column | fields_wrong | flags_v1 | flags_v2 | profile |
|---|---|---|---|---|---|---|---|
| qwen3:8b | L0 | False | property_gfa_calculated |  |  |  | {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": [""]} |
| qwen3:8b | L0 | False | site_energy_use_kbtu | unit; unit_multiplier | unit disagrees with label; missing code 'Not Available' is not a code | unit disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| qwen3:8b | L0 | False | electricity_weather_normalized_1 | unit | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| qwen3:8b | L0 | False | natural_gas_weather_normalized_1 | unit | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| qwen3:8b | L0 | True | property_gfa_calculated | missing_codes | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| qwen3:8b | L0 | True | site_energy_use_kbtu | unit | unit disagrees with label; multiplier disagrees with label; missing code 'Not Available' is not a code | unit disagrees with label; multiplier disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1000, "missing_codes": ["Not Available"]} |
| qwen3:8b | L0 | True | electricity_weather_normalized_1 | unit | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| qwen3:8b | L0 | True | natural_gas_weather_normalized_1 | unit | missing code 'Not Available' is not a code | unit disagrees with label | {"is_weight": false, "unit": "unit:DEG_F", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| qwen3:8b | L2 | False | property_gfa_calculated |  |  |  | {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": [""]} |
| qwen3:8b | L2 | False | site_energy_use_kbtu | unit; unit_multiplier | unit disagrees with label; missing code 'Not Available' is not a code | unit disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| qwen3:8b | L2 | False | electricity_use_grid_purchase_1 |  | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| qwen3:8b | L2 | False | natural_gas_use_kbtu | unit; unit_multiplier | unit disagrees with label; missing code 'Not Available' is not a code | unit disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| qwen3:8b | L2 | True | property_gfa_calculated | missing_codes | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| qwen3:8b | L2 | True | site_energy_use_kbtu | unit | unit disagrees with label; multiplier disagrees with label; missing code 'Not Available' is not a code | unit disagrees with label; multiplier disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1000, "missing_codes": ["Not Available"]} |
| qwen3:8b | L2 | True | electricity_use_grid_purchase_1 |  | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| qwen3:8b | L2 | True | natural_gas_use_kbtu | unit | unit disagrees with label; multiplier disagrees with label; missing code 'Not Available' is not a code | unit disagrees with label; multiplier disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1000, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L0 | False | largest_property_use_type_1 |  | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L0 | False | site_eui_kbtu_ft | unit | unit disagrees with label; missing code 'Not Available' is not a code | unit disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L0 | False | electricity_weather_normalized_1 | unit | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L0 | False | natural_gas_weather_normalized_1 | unit | missing code 'Not Available' is not a code | unit disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L0 | True | largest_property_use_type_1 |  | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L0 | True | site_eui_kbtu_ft | unit | unit disagrees with label; missing code 'Not Available' is not a code | unit disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 0, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L0 | True | electricity_weather_normalized_1 | unit | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L0 | True | natural_gas_weather_normalized_1 | unit | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L2 | False | property_gfa_calculated | missing_codes | missing code 'NA' is not a code; missing code 'DK' is not a code; missing code 'REFUSED' is not a code | missing code 'NA' is neither a listed code nor a missing-value label; missing code 'DK' is neither a listed code nor a missing-value label | {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["", "NA", "DK", "REFUSED"]} |
| llama3.1:8b | L2 | False | site_energy_use_kbtu | unit; unit_multiplier | unit disagrees with label; missing code 'Not Available' is not a code | unit disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L2 | False | electricity_weather_normalized_1 | unit | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L2 | False | natural_gas_weather_normalized_1 | unit | missing code 'Not Available' is not a code | unit disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L2 | True | property_gfa_calculated | missing_codes | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L2 | True | site_energy_use_kbtu | unit | unit disagrees with label; multiplier disagrees with label; missing code 'Not Available' is not a code | unit disagrees with label; multiplier disagrees with label | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1000, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L2 | True | electricity_weather_normalized_1 | unit | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:KiloW-HR", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |
| llama3.1:8b | L2 | True | natural_gas_weather_normalized_1 | unit | missing code 'Not Available' is not a code |  | {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Available"]} |

| source | model | column | unit | multiplier | missing_codes | unit_wrong | drops_valid_values | status | flagged_v1 | flagged_v2 | flagged_v2_without_ll84_terms | flags_v2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| main | qwen3:8b | property_gfa_calculated | unit:FT2 | 1 |  | False | False | exact | False | False | False |  |
| main | qwen3:8b | site_energy_use_kbtu | unit:KiloW-HR | 1 | Not Available | True | False | error | True | True | True | unit disagrees with label |
| main | qwen3:8b | electricity_weather_normalized_1 | unit:KiloW-HR | 1 | Not Available | True | False | error | True | False | True |  |
| main | qwen3:8b | natural_gas_weather_normalized_1 | unit:FT2 | 1 | Not Available | True | False | error | True | False | True |  |
| main | qwen3:8b | property_gfa_calculated | unit:FT2 | 1 | Not Available | False | False | harmless deviation | True | False | True |  |
| main | qwen3:8b | site_energy_use_kbtu | unit:KiloW-HR | 1000 | Not Available | True | False | error | True | True | True | unit disagrees with label; multiplier disagrees with label |
| main | qwen3:8b | natural_gas_weather_normalized_1 | unit:DEG_F | 1 | Not Available | True | False | error | True | True | True | unit disagrees with label |
| main | qwen3:8b | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | False | False | exact | True | False | True |  |
| main | qwen3:8b | natural_gas_use_kbtu | unit:KiloW-HR | 1 | Not Available | True | False | error | True | True | True | unit disagrees with label |
| main | qwen3:8b | natural_gas_use_kbtu | unit:KiloW-HR | 1000 | Not Available | True | False | error | True | True | True | unit disagrees with label; multiplier disagrees with label |
| main | llama3.1:8b | largest_property_use_type_1 | unit:FT2 | 1 | Not Available | False | False | exact | True | False | True |  |
| main | llama3.1:8b | site_eui_kbtu_ft | unit:KiloW-HR | 1 | Not Available | True | False | error | True | True | True | unit disagrees with label |
| main | llama3.1:8b | electricity_weather_normalized_1 | unit:KiloW-HR | 1 | Not Available | True | False | error | True | False | True |  |
| main | llama3.1:8b | natural_gas_weather_normalized_1 | unit:KiloW-HR | 1 | Not Available | True | False | error | True | True | True | unit disagrees with label |
| main | llama3.1:8b | site_eui_kbtu_ft | unit:KiloW-HR | 0 | Not Available | True | False | error | True | True | True | unit disagrees with label |
| main | llama3.1:8b | natural_gas_weather_normalized_1 | unit:FT2 | 1 | Not Available | True | False | error | True | False | True |  |
| main | llama3.1:8b | property_gfa_calculated | unit:FT2 | 1 | ; NA; DK; REFUSED | False | False | harmless deviation | True | True | True | missing code 'NA' is neither a listed code nor a missing-value label; missing code 'DK' is neither a listed code nor a missing-value label |
| main | llama3.1:8b | site_energy_use_kbtu | unit:KiloW-HR | 1 | Not Available | True | False | error | True | True | True | unit disagrees with label |
| main | llama3.1:8b | property_gfa_calculated | unit:FT2 | 1 | Not Available | False | False | harmless deviation | True | False | True |  |
| main | llama3.1:8b | site_energy_use_kbtu | unit:KiloW-HR | 1000 | Not Available | True | False | error | True | True | True | unit disagrees with label; multiplier disagrees with label |
| main | qwen3:8b | property_gfa_calculated_1 | unit:FT2 | 1 | 0 | False | True | error | True | True | True | missing code '0' inside the valid range |
| main | qwen3:8b | property_gfa_calculated_1 | unit:FT2 | 1 | Not Available | False | False | harmless deviation | True | False | True |  |
| post hoc units | qwen3:8b | property_gfa_calculated_1 | unit:FT2 | 1 |  | False | False | exact | False | False | False |  |
| post hoc units | qwen3:8b | site_energy_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | False | False | exact | True | True | True | unit disagrees with label |
| post hoc units | qwen3:8b | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | False | False | exact | True | False | True |  |
| post hoc units | qwen3:8b | natural_gas_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | False | False | exact | True | True | True | unit disagrees with label |
| post hoc units | qwen3:8b | property_gfa_calculated_1 | unit:FT2 | 1 | Not Available | False | False | harmless deviation | True | False | True |  |
| post hoc units | qwen3:8b | site_energy_use_kbtu | unit:KiloBTU_IT | 1000 | Not Available | True | False | error | True | True | True | unit disagrees with label; multiplier disagrees with label |
| post hoc units | qwen3:8b | natural_gas_use_kbtu | unit:KiloBTU_IT | 1000 | Not Available | True | False | error | True | True | True | unit disagrees with label; multiplier disagrees with label |
| main | llama3.1:8b | property_gfa_calculated_1 | unit:FT2 | 1 | ; NA; WK; WD | False | False | harmless deviation | True | True | True | missing code 'NA' is neither a listed code nor a missing-value label; missing code 'WK' is neither a listed code nor a missing-value label; missing code 'WD' is neither a listed code nor a missing-value label |
| main | llama3.1:8b | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | False | False | exact | True | False | True |  |
| main | llama3.1:8b | natural_gas_use_kbtu | unit:KiloW-HR | 1 | Not Available | True | False | error | True | True | True | unit disagrees with label |
| main | llama3.1:8b | property_gfa_calculated_1 | unit:FT2 | 1 | Not Available | False | False | harmless deviation | True | False | True |  |
| main | llama3.1:8b | natural_gas_use_kbtu | unit:KiloW-HR | 1000 | Not Available | True | False | error | True | True | True | unit disagrees with label; multiplier disagrees with label |
| post hoc units | llama3.1:8b | property_gfa_calculated_1 | unit:FT2 | 1 | ; NA; WK; WD | False | False | harmless deviation | True | True | True | missing code 'NA' is neither a listed code nor a missing-value label; missing code 'WK' is neither a listed code nor a missing-value label; missing code 'WD' is neither a listed code nor a missing-value label |
| post hoc units | llama3.1:8b | site_energy_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | False | False | exact | True | True | True | unit disagrees with label |
| post hoc units | llama3.1:8b | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | False | False | exact | True | False | True |  |
| post hoc units | llama3.1:8b | natural_gas_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | False | False | exact | True | True | True | unit disagrees with label |
| post hoc units | llama3.1:8b | property_gfa_calculated_1 | unit:FT2 | 1 | Not Available | False | False | harmless deviation | True | False | True |  |
| post hoc units | llama3.1:8b | site_energy_use_kbtu | unit:KiloBTU_IT | 1000 | Not Available | True | False | error | True | True | True | unit disagrees with label; multiplier disagrees with label |
| post hoc units | llama3.1:8b | natural_gas_use_kbtu | unit:KiloBTU_IT | 1000 | Not Available | True | False | error | True | True | True | unit disagrees with label; multiplier disagrees with label |

## S21. City case: pipeline results, decomposition and the first run

First table: model columns and model profiles. Second: model columns with gold profiles (selection only), reference columns with model profiles (normalization only), and the post hoc unit variant. Third and fourth: the first run, in which the tax-lot key was described by the concept record_identifier ('Identifier of a record, building, meter, station or respondent within the dataset'); with that definition both models chose the internal Property ID and no property was joined.

| model | selection | card | failed | linked | linked_vs_ref_pct | eui_city | eui_city_err_pct | elec_city_err_pct | gas_city_err_pct | districts_off_by_5pct | median_abs_district_err_pct | max_abs_district_err_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3:8b | L0 | False | False | 1 | -99.997 | 21.584 | -91.664 | -100.000 | -100.000 | 1 | 92.411 | 92.411 |
| qwen3:8b | L0 | True | False | 0 | -100.000 |  |  |  |  | 0 |  |  |
| qwen3:8b | L2 | False | False | 29794 | -0.839 | 803.978 | 210.488 | -7.913 | 204.918 | 65 | 215.418 | 241.214 |
| qwen3:8b | L2 | True | False | 43 | -99.857 | 1691.310 | 553.166 | -99.871 | 558.698 | 23 | 394.189 | 1381.968 |
| llama3.1:8b | L0 | False | False | 67 | -99.777 | 49.355 | -80.940 | -99.344 | -99.903 | 38 | 96.764 | 148.891 |
| llama3.1:8b | L0 | True | False | 67 | -99.777 | 49.355 | -80.940 | -99.344 | -100.000 | 38 | 96.764 | 148.891 |
| llama3.1:8b | L2 | False | False | 29794 | -0.839 | 803.978 | 210.488 | -99.999 | -100.000 | 65 | 215.418 | 241.214 |
| llama3.1:8b | L2 | True | False | 43 | -99.857 | 1691.310 | 553.166 | -100.000 | -100.000 | 23 | 394.189 | 1381.968 |

| model | variant | selection | card | failed | linked | eui_city_err_pct | elec_city_err_pct | gas_city_err_pct | median_abs_district_err_pct | profiles |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3:8b | selection only | L0 |  | False | 1 | -97.557 | -100.000 | -100.000 | 97.776 |  |
| qwen3:8b | selection only | L2 |  | False | 30044 | -2.031 | -2.032 | -2.031 | 1.509 |  |
| qwen3:8b | normalization only | reference | False | False | 29778 | 214.655 | -6.497 | 207.951 | 223.266 | {"property_gfa_calculated_1": {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["0"]}, "s |
| qwen3:8b | normalization only | reference | True | False | 43 | 553.828 | -99.871 | 559.365 | 394.189 | {"property_gfa_calculated_1": {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Avai |
| qwen3:8b | normalization only, publisher units offered (post hoc) | reference | False | False | 30046 | 0.000 | 0.000 | 0.000 | 0.000 | {"property_gfa_calculated_1": {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": [""]}, "si |
| qwen3:8b | normalization only, publisher units offered (post hoc) | reference | True | False | 105 | 416.648 | -99.794 | 599.474 | 397.671 | {"property_gfa_calculated_1": {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Avai |
| llama3.1:8b | selection only | L0 |  | False | 0 |  |  |  |  |  |
| llama3.1:8b | selection only | L2 |  | False | 30044 | -2.031 | -100.000 | -100.000 | 1.509 |  |
| llama3.1:8b | normalization only | reference | False | False | 29778 | 214.655 | -6.497 | 207.951 | 223.266 | {"property_gfa_calculated_1": {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["", "NA", |
| llama3.1:8b | normalization only | reference | True | False | 43 | 553.828 | -99.871 | 559.365 | 394.189 | {"property_gfa_calculated_1": {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Avai |
| llama3.1:8b | normalization only, publisher units offered (post hoc) | reference | False | False | 30046 | 0.000 | 0.000 | 0.000 | 0.000 | {"property_gfa_calculated_1": {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["", "NA", |
| llama3.1:8b | normalization only, publisher units offered (post hoc) | reference | True | False | 105 | 416.648 | -99.794 | 599.474 | 397.671 | {"property_gfa_calculated_1": {"is_weight": false, "unit": "unit:FT2", "unit_multiplier": 1, "missing_codes": ["Not Avai |

| model | selection | card | failed | linked | linked_vs_ref_pct | eui_city | eui_city_err_pct | elec_city_err_pct | gas_city_err_pct | districts_off_by_5pct | median_abs_district_err_pct | max_abs_district_err_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3:8b | L0 | False | False | 29794 | -0.839 | 803.978 | 210.488 | -99.999 | -100.000 | 65 | 215.418 | 241.214 |
| qwen3:8b | L0 | True | False | 43 | -99.857 | 1691.310 | 553.166 | -100.000 | -100.000 | 23 | 394.189 | 1381.968 |
| qwen3:8b | L2 | False | False | 0 | -100.000 |  |  |  |  | 0 |  |  |
| qwen3:8b | L2 | True | False | 0 | -100.000 |  |  |  |  | 0 |  |  |
| llama3.1:8b | L0 | False | False | 67 | -99.777 | 49.355 | -80.940 | -99.344 | -99.903 | 38 | 96.764 | 148.891 |
| llama3.1:8b | L0 | True | False | 67 | -99.777 | 49.355 | -80.940 | -99.344 | -100.000 | 38 | 96.764 | 148.891 |
| llama3.1:8b | L2 | False | False | 0 | -100.000 |  |  |  |  | 0 |  |  |
| llama3.1:8b | L2 | True | False | 0 | -100.000 |  |  |  |  | 0 |  |  |

| model | selection | card | role | column | correct | confidence |
|---|---|---|---|---|---|---|
| qwen3:8b | L0 | False | bbl | nyc_borough_block_and_lot | True | 0.950 |
| qwen3:8b | L0 | False | area | property_gfa_calculated | True | 1.000 |
| qwen3:8b | L0 | False | site | site_energy_use_kbtu | True | 1.000 |
| qwen3:8b | L0 | False | elec | electricity_weather_normalized_1 | False | 1.000 |
| qwen3:8b | L0 | False | gas | natural_gas_weather_normalized_1 | False | 1.000 |
| qwen3:8b | L0 | False | pluto_bbl | bbl | True |  |
| qwen3:8b | L0 | True | bbl | nyc_borough_block_and_lot | True | 0.950 |
| qwen3:8b | L0 | True | area | property_gfa_calculated | True | 1.000 |
| qwen3:8b | L0 | True | site | site_energy_use_kbtu | True | 1.000 |
| qwen3:8b | L0 | True | elec | electricity_weather_normalized_1 | False | 1.000 |
| qwen3:8b | L0 | True | gas | natural_gas_weather_normalized_1 | False | 1.000 |
| qwen3:8b | L0 | True | pluto_bbl | bbl | True |  |
| qwen3:8b | L2 | False | bbl | property_id | False | 1.000 |
| qwen3:8b | L2 | False | area | property_gfa_calculated | True | 1.000 |
| qwen3:8b | L2 | False | site | site_energy_use_kbtu | True | 1.000 |
| qwen3:8b | L2 | False | elec | electricity_use_grid_purchase_1 | True | 0.950 |
| qwen3:8b | L2 | False | gas | natural_gas_use_kbtu | True | 0.950 |
| qwen3:8b | L2 | False | pluto_bbl | bbl | True |  |
| qwen3:8b | L2 | True | bbl | property_id | False | 1.000 |
| qwen3:8b | L2 | True | area | property_gfa_calculated | True | 1.000 |
| qwen3:8b | L2 | True | site | site_energy_use_kbtu | True | 1.000 |
| qwen3:8b | L2 | True | elec | electricity_use_grid_purchase_1 | True | 0.950 |
| qwen3:8b | L2 | True | gas | natural_gas_use_kbtu | True | 0.950 |
| qwen3:8b | L2 | True | pluto_bbl | bbl | True |  |
| llama3.1:8b | L0 | False | bbl | nyc_borough_block_and_lot | True | 1.000 |
| llama3.1:8b | L0 | False | area | largest_property_use_type_1 | False | 0.900 |
| llama3.1:8b | L0 | False | site | site_eui_kbtu_ft | False | 1.000 |
| llama3.1:8b | L0 | False | elec | electricity_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L0 | False | gas | natural_gas_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L0 | False | pluto_bbl | bbl | True |  |
| llama3.1:8b | L0 | True | bbl | nyc_borough_block_and_lot | True | 1.000 |
| llama3.1:8b | L0 | True | area | largest_property_use_type_1 | False | 0.900 |
| llama3.1:8b | L0 | True | site | site_eui_kbtu_ft | False | 1.000 |
| llama3.1:8b | L0 | True | elec | electricity_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L0 | True | gas | natural_gas_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L0 | True | pluto_bbl | bbl | True |  |
| llama3.1:8b | L2 | False | bbl | property_id | False | 1.000 |
| llama3.1:8b | L2 | False | area | property_gfa_calculated | True | 0.900 |
| llama3.1:8b | L2 | False | site | site_energy_use_kbtu | True | 0.900 |
| llama3.1:8b | L2 | False | elec | electricity_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L2 | False | gas | natural_gas_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L2 | False | pluto_bbl | bbl | True |  |
| llama3.1:8b | L2 | True | bbl | property_id | False | 1.000 |
| llama3.1:8b | L2 | True | area | property_gfa_calculated | True | 0.900 |
| llama3.1:8b | L2 | True | site | site_energy_use_kbtu | True | 0.900 |
| llama3.1:8b | L2 | True | elec | electricity_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L2 | True | gas | natural_gas_weather_normalized_1 | False | 0.900 |
| llama3.1:8b | L2 | True | pluto_bbl | bbl | True |  |


## S22. Four-source city integration (E8b)

LL84 benchmarking, PLUTO tax lots, building footprints (polygons and roof heights) and TMYx weather files of four stations. Columns chosen by each model (definitions given, L2) and the profiles built with the tool's normalization prompt under four context conditions: entry (portal description and values only), card (all dataset conventions as prose), scoped (only the conventions whose machine-readable scope covers the column) and tool (scoped, with the conventions' stated values applied by the tool). Status compares a profile with the reference: error (a wrong conversion to SI units, a missing code of the reference not declared while it occurs in the data, or a frequent valid value declared missing), harmless deviation, or exact.

### Reference pipeline

| links | records | usable | linked_pluto | linked_footprints | linked_weather | complete |
|---|---|---|---|---|---|---|
| reference | 33684 | 30439 | 30071 | 29692 | 30061 | 29077 |

### Weather stations

| station | state | country | wmo | latitude | longitude | tz | elevation_m | file | hdd18 | cdd18 | mean_temp_c |
|---|---|---|---|---|---|---|---|---|---|---|---|
| New.York-Central.Park.Obs-Belvedere.Castle | NY | USA | 725053 | 40.779 | -73.969 | -5.000 | 48.000 | USA_NY_New.York-Central.Park.Obs-Belvedere.Castle.725053_TMYx.2009-2023.zip | 2463.679 | 717.675 | 13.216 |
| New.York-Downtown.Manhattan.Heli | NY | USA | 720553 | 40.701 | -74.009 | -5.000 | 2.100 | USA_NY_New.York-Downtown.Manhattan.Heli.720553_TMYx.2009-2023.zip | 2377.446 | 755.600 | 13.557 |
| New.York-Kennedy.Intl.AP | NY | USA | 744860 | 40.639 | -73.764 | -5.000 | 3.400 | USA_NY_New.York-Kennedy.Intl.AP.744860_TMYx.2009-2023.zip | 2437.863 | 641.796 | 13.079 |
| New.York-LaGuardia.AP | NY | USA | 725030 | 40.779 | -73.880 | -5.000 | 3.400 | USA_NY_New.York-LaGuardia.AP.725030_TMYx.2009-2023.zip | 2418.192 | 767.104 | 13.476 |

### Columns selected

| model | role | column | reference | correct |
|---|---|---|---|---|
| qwen3:8b | ll84.bbl | nyc_borough_block_and_lot | nyc_borough_block_and_lot | True |
| qwen3:8b | ll84.bin | nyc_building_identification | nyc_building_identification | True |
| qwen3:8b | ll84.area | property_gfa_calculated | property_gfa_calculated_1 | True |
| qwen3:8b | ll84.site | site_energy_use_kbtu | site_energy_use_kbtu | True |
| qwen3:8b | ll84.elec | electricity_use_grid_purchase_1 | electricity_use_grid_purchase_1 | True |
| qwen3:8b | ll84.gas | natural_gas_use_kbtu | natural_gas_use_kbtu | True |
| qwen3:8b | pluto.bbl | bbl | bbl | True |
| qwen3:8b | pluto.cd | cd | cd | True |
| qwen3:8b | pluto.year | yearbuilt | yearbuilt | True |
| qwen3:8b | pluto.floors | numfloors | numfloors | True |
| qwen3:8b | pluto.lat | latitude | latitude | True |
| qwen3:8b | pluto.lon | longitude | longitude | True |
| qwen3:8b | footprints.bin | bin | bin | True |
| qwen3:8b | footprints.height | height_roof | height_roof | True |
| qwen3:8b | footprints.footprint | shape_area | the_geom | False |
| qwen3:8b | footprints.year | construction_year | construction_year | True |
| llama3.1:8b | ll84.bbl | nyc_borough_block_and_lot | nyc_borough_block_and_lot | True |
| llama3.1:8b | ll84.bin | nyc_building_identification | nyc_building_identification | True |
| llama3.1:8b | ll84.area | property_gfa_calculated | property_gfa_calculated_1 | True |
| llama3.1:8b | ll84.site | site_energy_use_kbtu | site_energy_use_kbtu | True |
| llama3.1:8b | ll84.elec | electricity_weather_normalized_1 | electricity_use_grid_purchase_1 | False |
| llama3.1:8b | ll84.gas | natural_gas_weather_normalized_1 | natural_gas_use_kbtu | False |
| llama3.1:8b | pluto.bbl | bbl | bbl | True |
| llama3.1:8b | pluto.cd | cd | cd | True |
| llama3.1:8b | pluto.year | yearbuilt | yearbuilt | True |
| llama3.1:8b | pluto.floors | numfloors | numfloors | True |
| llama3.1:8b | pluto.lat | latitude | latitude | True |
| llama3.1:8b | pluto.lon | longitude | longitude | True |
| llama3.1:8b | footprints.bin | base_bbl | bin | False |
| llama3.1:8b | footprints.height | height_roof | height_roof | True |
| llama3.1:8b | footprints.footprint | the_geom | the_geom | True |
| llama3.1:8b | footprints.year | construction_year | construction_year | True |

### Profiles of the reference columns

| model | condition | dataset | column | unit | multiplier | missing_codes | model_unit | model_multiplier | status | status_model_answer | review_flags_on_answer | review_flags_frozen |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3:8b | entry | ll84 | nyc_borough_block_and_lot | none | 1 | Not Available | none | 1 | exact | exact |  |  |
| qwen3:8b | entry | ll84 | nyc_building_identification | none | 1 | Not Available | none | 1 | error | error |  |  |
| qwen3:8b | entry | ll84 | property_gfa_calculated_1 | unit:FT2 | 1 | 17 | unit:FT2 | 1 | harmless deviation | harmless deviation |  |  |
| qwen3:8b | entry | ll84 | site_energy_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | unit:KiloBTU_IT | 1 | exact | exact |  |  |
| qwen3:8b | entry | ll84 | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | unit:KiloW-HR | 1 | exact | exact |  |  |
| qwen3:8b | entry | ll84 | natural_gas_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | unit:KiloBTU_IT | 1 | exact | exact |  |  |
| qwen3:8b | entry | pluto | bbl | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | entry | pluto | yearbuilt | none | 1 | 0 | none | 1 | exact | exact |  |  |
| qwen3:8b | entry | pluto | numfloors | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | entry | pluto | latitude | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | entry | pluto | longitude | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | entry | footprints | bin | none | 1 | 0 | none | 1 | error | error |  |  |
| qwen3:8b | entry | footprints | height_roof | none | 1 | 0 | none | 1 | error | error |  |  |
| qwen3:8b | entry | footprints | construction_year | none | 1 |  | none | 1 | harmless deviation | harmless deviation |  |  |
| qwen3:8b | card | ll84 | nyc_borough_block_and_lot | none | 1 | Not Available | none | 1 | exact | exact |  |  |
| qwen3:8b | card | ll84 | nyc_building_identification | none | 1 | Not Available | none | 1 | error | error |  |  |
| qwen3:8b | card | ll84 | property_gfa_calculated_1 | unit:FT2 | 1 |  | unit:FT2 | 1 | exact | exact |  |  |
| qwen3:8b | card | ll84 | site_energy_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | unit:KiloBTU_IT | 1 | exact | exact |  |  |
| qwen3:8b | card | ll84 | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | unit:KiloW-HR | 1 | exact | exact |  |  |
| qwen3:8b | card | ll84 | natural_gas_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | unit:KiloBTU_IT | 1 | exact | exact |  |  |
| qwen3:8b | card | pluto | bbl | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | card | pluto | yearbuilt | none | 1 | 0 | none | 1 | exact | exact |  |  |
| qwen3:8b | card | pluto | numfloors | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | card | pluto | latitude | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | card | pluto | longitude | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | card | footprints | bin | none | 1 | 0 | none | 1 | error | error |  |  |
| qwen3:8b | card | footprints | height_roof | unit:FT | 1 | 0 | unit:FT | 1 | exact | exact |  |  |
| qwen3:8b | card | footprints | construction_year | none | 1 |  | none | 1 | harmless deviation | harmless deviation |  |  |
| qwen3:8b | scoped | ll84 | nyc_borough_block_and_lot | none | 1 | Not Available | none | 1 | exact | exact |  |  |
| qwen3:8b | scoped | ll84 | nyc_building_identification | none | 1 | Not Available | none | 1 | error | error |  |  |
| qwen3:8b | scoped | ll84 | property_gfa_calculated_1 | unit:FT2 | 1 | 0 | unit:FT2 | 1 | harmless deviation | harmless deviation |  |  |
| qwen3:8b | scoped | ll84 | site_energy_use_kbtu | unit:KiloBTU_IT | 1000 | Not Available | unit:KiloBTU_IT | 1000 | error | error |  |  |
| qwen3:8b | scoped | ll84 | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | unit:KiloW-HR | 1 | exact | exact |  |  |
| qwen3:8b | scoped | ll84 | natural_gas_use_kbtu | unit:KiloBTU_IT | 1000 | Not Available | unit:KiloBTU_IT | 1000 | error | error |  |  |
| qwen3:8b | scoped | pluto | bbl | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | scoped | pluto | yearbuilt | none | 1 | 0 | none | 1 | exact | exact |  |  |
| qwen3:8b | scoped | pluto | numfloors | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | scoped | pluto | latitude | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | scoped | pluto | longitude | none | 1 |  | none | 1 | exact | exact |  |  |
| qwen3:8b | scoped | footprints | bin | none | 1 |  | none | 1 | error | error |  |  |
| qwen3:8b | scoped | footprints | height_roof | unit:FT | 1 | 0 | unit:FT | 1 | exact | exact |  |  |
| qwen3:8b | scoped | footprints | construction_year | none | 1 |  | none | 1 | harmless deviation | harmless deviation |  |  |
| qwen3:8b | tool | ll84 | nyc_borough_block_and_lot | none | 1 | Not Available | none | 1 | exact | exact |  | no unit, but the documentation names unit:W-HR |
| qwen3:8b | tool | ll84 | nyc_building_identification | none | 1 | Not Available | none | 1 | error | error |  |  |
| qwen3:8b | tool | ll84 | property_gfa_calculated_1 | unit:FT2 | 1 | 0; Not Available | unit:FT2 | 1 | harmless deviation | harmless deviation | numeric missing code '0' is not documented as missing | numeric missing code '0' is not documented as missing |
| qwen3:8b | tool | ll84 | site_energy_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | unit:KiloBTU_IT | 1000 | exact | error | convention set unit unit:KiloBTU_IT | convention set unit unit:KiloBTU_IT |
| qwen3:8b | tool | ll84 | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | unit:KiloW-HR | 1 | exact | exact |  |  |
| qwen3:8b | tool | ll84 | natural_gas_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | unit:KiloBTU_IT | 1000 | exact | error | convention set unit unit:KiloBTU_IT | convention set unit unit:KiloBTU_IT |
| qwen3:8b | tool | pluto | bbl | none | 1 |  | none | 1 | exact | exact |  | no unit, but the documentation names unit:W-HR |
| qwen3:8b | tool | pluto | yearbuilt | none | 1 | 0;  | none | 1 | exact | exact |  | no unit, but the documentation names unit:W-HR |
| qwen3:8b | tool | pluto | numfloors | none | 1 |  | none | 1 | exact | exact |  | no unit, but the documentation names unit:FT |
| qwen3:8b | tool | pluto | latitude | none | 1 |  | none | 1 | exact | exact |  | no unit, but the documentation names unit:PA |
| qwen3:8b | tool | pluto | longitude | none | 1 |  | none | 1 | exact | exact |  | no unit, but the documentation names unit:PA |
| qwen3:8b | tool | footprints | bin | none | 1 | ; 1000000; 2000000; 3000000; 4000000; 5000000 | none | 1 | exact | error |  | no unit, but the documentation names unit:W-HR |
| qwen3:8b | tool | footprints | height_roof | unit:FT | 1 | 0;  | unit:FT | 1 | exact | exact |  |  |
| qwen3:8b | tool | footprints | construction_year | none | 1 | ; 0 | none | 1 | exact | harmless deviation |  |  |
| llama3.1:8b | entry | ll84 | nyc_borough_block_and_lot | none | 1 | Not Available | none | 1 | exact | exact |  |  |
| llama3.1:8b | entry | ll84 | nyc_building_identification | none | 1 | Not Available | none | 1 | error | error |  |  |
| llama3.1:8b | entry | ll84 | property_gfa_calculated_1 | unit:FT2 | 1 | ; ], // 17 zeros and 12 empty values are considered missing codes for this column, as they are not valid observations of property gross floor area in square feet (ft²) and are likely errors or missing data points in the dataset. The empty values are represented by an empty string ( | unit:FT2 | 1 | harmless deviation | harmless deviation |  |  |
| llama3.1:8b | entry | ll84 | site_energy_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | unit:KiloBTU_IT | 1 | exact | exact |  |  |
| llama3.1:8b | entry | ll84 | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | unit:KiloW-HR | 1 | exact | exact |  |  |
| llama3.1:8b | entry | ll84 | natural_gas_use_kbtu | none | 1 | Not Available | none | 1 | error | error |  |  |
| llama3.1:8b | entry | pluto | bbl | none | 1 |  | none | 1 | exact | exact |  |  |
| llama3.1:8b | entry | pluto | yearbuilt | none | 1 | ; :-1; :-2 | none | 1 | error | error |  |  |
| llama3.1:8b | entry | pluto | numfloors | none | 1 | ; ,; 0 | none | 1 | harmless deviation | harmless deviation |  |  |
| llama3.1:8b | entry | pluto | latitude | none | 1 | ; 0; NULL | none | 1 | harmless deviation | harmless deviation |  |  |
| llama3.1:8b | entry | pluto | longitude | none | 1 | 937 | none | 1 | harmless deviation | harmless deviation |  |  |
| llama3.1:8b | entry | footprints | bin | none | 1 |  | none | 1 | error | error |  |  |
| llama3.1:8b | entry | footprints | height_roof | none | 1 | 714 | none | 1 | error | error |  |  |
| llama3.1:8b | entry | footprints | construction_year | none | 1 |  | none | 1 | harmless deviation | harmless deviation |  |  |
| llama3.1:8b | card | ll84 | nyc_borough_block_and_lot | none | 1 | Not Available | none | 1 | exact | exact |  |  |
| llama3.1:8b | card | ll84 | nyc_building_identification | none | 1 | Not Available | none | 1 | error | error |  |  |
| llama3.1:8b | card | ll84 | property_gfa_calculated_1 | none | 1 | ; 0 | none | 1 | error | error |  |  |
| llama3.1:8b | card | ll84 | site_energy_use_kbtu | none | 1 | Not Available | none | 1 | error | error |  |  |
| llama3.1:8b | card | ll84 | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | unit:KiloW-HR | 1 | exact | exact |  |  |
| llama3.1:8b | card | ll84 | natural_gas_use_kbtu | none | 1 | Not Available | none | 1 | error | error |  |  |
| llama3.1:8b | card | pluto | bbl | none | 1 |  | none | 1 | exact | exact |  |  |
| llama3.1:8b | card | pluto | yearbuilt | none | 1 | ; :-1 | none | 1 | error | error |  |  |
| llama3.1:8b | card | pluto | numfloors | none | 1 | ; , 0, 0, 0 | none | 1 | harmless deviation | harmless deviation |  |  |
| llama3.1:8b | card | pluto | latitude | none | 1 |  | none | 1 | exact | exact |  |  |
| llama3.1:8b | card | pluto | longitude | none | 1 |  | none | 1 | exact | exact |  |  |
| llama3.1:8b | card | footprints | bin | none | 1 |  | none | 1 | error | error |  |  |
| llama3.1:8b | card | footprints | height_roof | none | 1 | 0 | none | 1 | error | error |  |  |
| llama3.1:8b | card | footprints | construction_year | none | 1 | 0 | none | 1 | exact | exact |  |  |
| llama3.1:8b | scoped | ll84 | nyc_borough_block_and_lot | none | 1 | Not Available | none | 1 | exact | exact |  |  |
| llama3.1:8b | scoped | ll84 | nyc_building_identification | none | 1 | Not Available | none | 1 | error | error |  |  |
| llama3.1:8b | scoped | ll84 | property_gfa_calculated_1 | none | 1 | Not Available | none | 1 | error | error |  |  |
| llama3.1:8b | scoped | ll84 | site_energy_use_kbtu | unit:KiloBTU_IT | 1000 | Not Available | unit:KiloBTU_IT | 1000 | error | error |  |  |
| llama3.1:8b | scoped | ll84 | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | unit:KiloW-HR | 1 | exact | exact |  |  |
| llama3.1:8b | scoped | ll84 | natural_gas_use_kbtu | unit:KiloBTU_IT | 1000 | Not Available | unit:KiloBTU_IT | 1000 | error | error |  |  |
| llama3.1:8b | scoped | pluto | bbl | none | 1 |  | none | 1 | exact | exact |  |  |
| llama3.1:8b | scoped | pluto | yearbuilt | none | 1 | 0;  | none | 1 | exact | exact |  |  |
| llama3.1:8b | scoped | pluto | numfloors | none | 1 | ; ,; 0 | none | 1 | harmless deviation | harmless deviation |  |  |
| llama3.1:8b | scoped | pluto | latitude | none | 1 | ; 0; NULL | none | 1 | harmless deviation | harmless deviation |  |  |
| llama3.1:8b | scoped | pluto | longitude | none | 1 | 937 | none | 1 | harmless deviation | harmless deviation |  |  |
| llama3.1:8b | scoped | footprints | bin | none | 1 |  | none | 1 | error | error |  |  |
| llama3.1:8b | scoped | footprints | height_roof | none | 1 | 0 | none | 1 | error | error |  |  |
| llama3.1:8b | scoped | footprints | construction_year | none | 1 |  | none | 1 | harmless deviation | harmless deviation |  |  |
| llama3.1:8b | tool | ll84 | nyc_borough_block_and_lot | none | 1 | Not Available | none | 1 | exact | exact |  | no unit, but the documentation names unit:W-HR |
| llama3.1:8b | tool | ll84 | nyc_building_identification | none | 1 | Not Available | none | 1 | error | error |  |  |
| llama3.1:8b | tool | ll84 | property_gfa_calculated_1 | unit:FT2 | 1 | Not Available | none | 1 | harmless deviation | error | no unit for a concept measured in unit:M2; convention set unit unit:FT2 | no unit for a concept measured in unit:M2; convention set unit unit:FT2 |
| llama3.1:8b | tool | ll84 | site_energy_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | unit:KiloBTU_IT | 1000 | exact | error | convention set unit unit:KiloBTU_IT | convention set unit unit:KiloBTU_IT |
| llama3.1:8b | tool | ll84 | electricity_use_grid_purchase_1 | unit:KiloW-HR | 1 | Not Available | unit:KiloW-HR | 1 | exact | exact |  |  |
| llama3.1:8b | tool | ll84 | natural_gas_use_kbtu | unit:KiloBTU_IT | 1 | Not Available | unit:KiloBTU_IT | 1000 | exact | error | convention set unit unit:KiloBTU_IT | convention set unit unit:KiloBTU_IT |
| llama3.1:8b | tool | pluto | bbl | none | 1 |  | none | 1 | exact | exact |  | no unit, but the documentation names unit:W-HR |
| llama3.1:8b | tool | pluto | yearbuilt | none | 1 | 0;  | none | 1 | exact | exact |  | no unit, but the documentation names unit:W-HR |
| llama3.1:8b | tool | pluto | numfloors | none | 1 | ; ,; 0 | none | 1 | harmless deviation | harmless deviation | missing code ',' is not a missing-value label | no unit, but the documentation names unit:FT; missing code ',' is not a missing-value label |
| llama3.1:8b | tool | pluto | latitude | none | 1 | ; 0; NULL | none | 1 | harmless deviation | harmless deviation | numeric missing code '0' is not documented as missing | no unit, but the documentation names unit:PA; numeric missing code '0' is not documented as missing |
| llama3.1:8b | tool | pluto | longitude | none | 1 | 937 | none | 1 | harmless deviation | harmless deviation | numeric missing code '937' is not documented as missing | no unit, but the documentation names unit:PA; numeric missing code '937' is not documented as missing |
| llama3.1:8b | tool | footprints | bin | none | 1 | 1000000; 2000000; 3000000; 4000000; 5000000 | none | 1 | exact | error |  | no unit, but the documentation names unit:W-HR |
| llama3.1:8b | tool | footprints | height_roof | unit:FT | 1 | 0;  | none | 1 | exact | error | no unit for a concept measured in unit:M; convention set unit unit:FT | no unit for a concept measured in unit:M; convention set unit unit:FT |
| llama3.1:8b | tool | footprints | construction_year | none | 1 | ; 0 | none | 1 | exact | harmless deviation |  |  |

### Indicators of the integrated table

| model | condition | linked_pluto | linked_footprints | linked_weather | complete_inputs | floor_area_share_before 1940 | eui_before 1940 | floor_area_share_1940-1979 | eui_1940-1979 | floor_area_share_1980-2009 | eui_1980-2009 | floor_area_share_2010 or later | eui_2010 or later | median_height_m | median_height_per_floor_m | median_gfa_to_footprint_x_floors | total_volume_million_m3 | gas_per_m2_hdd | usable | complete |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| reference | reference | 30071 | 29692 | 30061 | 29077 | 35.538 | 244.159 | 40.520 | 286.827 | 14.926 | 250.016 | 9.016 | 191.518 | 20.684 | 3.536 | 1.040 | 1488.459 | 0.062 | 30439 | 29077 |
| qwen3:8b | selection only (gold profiles) | 30069 | 29691 | 30059 | 0 | 34.977 | 243.007 | 40.707 | 279.680 | 15.167 | 241.017 | 9.149 | 184.896 | 20.684 | 3.536 |  | 0.000 | 0.061 | 30437 | 0 |
| qwen3:8b | entry, model columns | 30069 | 29702 | 30059 | 29087 | 34.977 | 243.007 | 40.707 | 279.680 | 15.167 | 241.017 | 9.149 | 184.896 | 67.860 | 11.600 | 0.598 | 8527.844 | 0.061 | 30437 | 29087 |
| qwen3:8b | entry, reference columns | 30071 | 29703 | 30061 | 29077 | 35.538 | 244.159 | 40.520 | 286.827 | 14.926 | 250.016 | 9.016 | 191.518 | 67.860 | 11.600 | 1.040 | 4883.397 | 0.062 | 30439 | 29077 |
| qwen3:8b | card, model columns | 30069 | 29702 | 30059 | 29087 | 34.977 | 243.007 | 40.707 | 279.680 | 15.167 | 241.017 | 9.149 | 184.896 | 20.684 | 3.536 | 0.598 | 2599.287 | 0.061 | 30437 | 29087 |
| qwen3:8b | card, reference columns | 30071 | 29703 | 30061 | 29077 | 35.538 | 244.159 | 40.520 | 286.827 | 14.926 | 250.016 | 9.016 | 191.518 | 20.684 | 3.536 | 1.040 | 1488.459 | 0.062 | 30439 | 29077 |
| qwen3:8b | scoped, model columns | 105 | 97 | 105 | 95 | 26.205 | 1594.024 | 59.995 | 1247.723 | 1.597 | 1367.936 | 12.202 | 1327.814 | 19.297 | 3.962 | 0.591 | 9.966 | 0.601 | 109 | 95 |
| qwen3:8b | scoped, reference columns | 105 | 97 | 105 | 94 | 26.283 | 1594.024 | 60.125 | 1248.713 | 1.602 | 1367.936 | 11.991 | 1355.208 | 19.297 | 3.962 | 1.032 | 5.712 | 0.601 | 109 | 94 |
| qwen3:8b | tool, model columns | 30069 | 29691 | 30059 | 0 | 34.977 | 243.007 | 40.707 | 279.680 | 15.167 | 241.017 | 9.149 | 184.896 | 20.684 | 3.536 |  | 0.000 | 0.061 | 30437 | 0 |
| qwen3:8b | tool, reference columns | 30071 | 29692 | 30061 | 29077 | 35.538 | 244.159 | 40.520 | 286.827 | 14.926 | 250.016 | 9.016 | 191.518 | 20.684 | 3.536 | 1.040 | 1488.459 | 0.062 | 30439 | 29077 |
| llama3.1:8b | selection only (gold profiles) | 30069 | 1 | 30059 | 0 | 34.977 | 243.007 | 40.707 | 279.680 | 15.167 | 241.017 | 9.149 | 184.896 | 18.288 | 4.572 |  | 0.000 | 0.000 | 30437 | 0 |
| llama3.1:8b | entry, model columns | 28621 | 0 | 28609 | 0 | 35.370 | 24.453 | 40.377 | 27.816 | 15.288 | 23.151 | 8.965 | 18.229 |  |  |  | 0.000 | 0.000 | 28913 | 0 |
| llama3.1:8b | entry, reference columns | 30075 | 29703 | 30061 | 29132 | 36.204 | 248.025 | 40.101 | 286.827 | 14.772 | 250.016 | 8.923 | 191.518 | 67.860 | 11.600 | 1.040 | 4883.397 | 0.212 | 30439 | 29132 |
| llama3.1:8b | card, model columns | 29915 | 0 | 29901 | 0 | 35.492 | 79.945 | 40.418 | 90.379 | 15.052 | 77.549 | 9.038 | 59.254 |  |  |  | 0.000 | 0.000 | 30252 | 0 |
| llama3.1:8b | card, reference columns | 29922 | 29554 | 29908 | 28951 | 36.037 | 80.335 | 40.227 | 92.655 | 14.824 | 80.350 | 8.912 | 61.311 | 67.881 | 11.596 | 11.195 | 4859.733 | 0.020 | 30259 | 28951 |
| llama3.1:8b | scoped, model columns | 737 | 1 | 736 | 0 | 35.640 | 1201.180 | 42.643 | 1108.339 | 9.600 | 1429.963 | 12.117 | 1442.899 | 60.000 | 15.000 |  | 0.000 | 0.000 | 789 | 0 |
| llama3.1:8b | scoped, reference columns | 724 | 678 | 723 | 647 | 36.744 | 1194.594 | 42.942 | 1082.844 | 8.288 | 1476.966 | 12.026 | 1469.336 | 58.714 | 12.923 | 11.195 | 102.073 | 0.241 | 776 | 647 |
| llama3.1:8b | tool, model columns | 30069 | 1 | 30059 | 0 | 34.977 | 243.007 | 40.707 | 279.680 | 15.167 | 241.017 | 9.149 | 184.896 | 18.288 | 4.572 |  | 0.000 | 0.000 | 30437 | 0 |
| llama3.1:8b | tool, reference columns | 30071 | 29692 | 30061 | 29077 | 35.538 | 244.159 | 40.520 | 286.827 | 14.926 | 250.016 | 9.016 | 191.518 | 20.684 | 3.536 | 1.040 | 1488.459 | 0.062 | 30439 | 29077 |




## S24. Catalog

Every dataset with its primary UBEM role, finest public spatial granularity and best linkage to buildings. Linkage classes: shared_identifier (a field holding the same building or parcel identifier as a footprint or parcel dataset of the same jurisdiction); building_location (coordinates or addresses of individual buildings); area_code (only an area such as a census unit, postal code or climate zone); attribute_only (records of individual buildings described only by attributes, with no location); none (no usable key).

| id | primary_role | granularity | linkage |
|---|---|---|---|
| chr-ahs | building_characteristics | census_region_division | area_code |
| chr-bedes | building_characteristics | none | none |
| chr-bps | building_characteristics | city | area_code |
| chr-buildingsync | building_characteristics | none | none |
| chr-cbecs-2018 | building_characteristics | census_region_division | area_code |
| chr-doe-bpd | building_characteristics | none | area_code |
| chr-doe-prototypes | reference_simulation | climate_zone | area_code |
| chr-energy-codes-status | building_characteristics | state_province | none |
| chr-eu-bso | building_characteristics | nation | area_code |
| chr-france-dpe | building_characteristics | building | shared_identifier |
| chr-germany-zensus-2022 | building_characteristics | grid_cell_fine | area_code |
| chr-hotmaps | building_characteristics | grid_cell_fine | area_code |
| chr-ireland-ber | building_characteristics | unknown | none |
| chr-nyc-ll84 | calibration_validation | building | shared_identifier |
| chr-nyc-pluto | building_characteristics | parcel | shared_identifier |
| chr-recs-2020 | building_characteristics | state_province | area_code |
| chr-tabula-episcope | building_characteristics | nation | area_code |
| chr-uk-epc | building_characteristics | building | shared_identifier |
| ctx-acs | context_coupling | census_block_group | area_code |
| ctx-cambium | context_coupling | utility_service_territory | area_code |
| ctx-egrid | context_coupling | utility_service_territory | area_code |
| ctx-lcz-global | context_coupling | grid_cell_fine | area_code |
| ctx-urdb | context_coupling | utility_service_territory | area_code |
| geo-3d-globfp | geometry_inventory | building | building_location |
| geo-3dbag | geometry_inventory | building | building_location |
| geo-china-rooftop-2023 | geometry_inventory | building | building_location |
| geo-cmab | geometry_inventory | building | building_location |
| geo-eubucco | geometry_inventory | building | building_location |
| geo-ghs-obat | geometry_inventory | building | building_location |
| geo-ghsl-built | geometry_inventory | grid_cell_fine | area_code |
| geo-globalbuildingatlas | geometry_inventory | building | building_location |
| geo-google-open-buildings-25d | geometry_inventory | grid_cell_fine | area_code |
| geo-google-open-buildings | geometry_inventory | building | building_location |
| geo-heris-raster-footprints | geometry_inventory | grid_cell_fine | area_code |
| geo-ms-global-footprints | geometry_inventory | building | building_location |
| geo-ms-us-footprints | geometry_inventory | building | building_location |
| geo-nyc-footprints | geometry_inventory | building | shared_identifier |
| geo-open-city-model | geometry_inventory | building | building_location |
| geo-osm | geometry_inventory | building | building_location |
| geo-overture-buildings | geometry_inventory | building | building_location |
| geo-plateau | geometry_inventory | building | building_location |
| geo-regrid-parcels | geometry_inventory | parcel | shared_identifier |
| geo-ubid | geometry_inventory | building | shared_identifier |
| geo-usa-structures | geometry_inventory | building | building_location |
| geo-usgs-3dep | geometry_inventory | grid_cell_fine | area_code |
| geo-ut-globus | geometry_inventory | building | building_location |
| geo-wsf3d | geometry_inventory | grid_cell_fine | area_code |
| nrg-ashrae-gepiii | calibration_validation | building | none |
| nrg-bdg2 | calibration_validation | building | none |
| nrg-desnz-subnational | calibration_validation | postal_code | area_code |
| nrg-eia-861 | calibration_validation | utility_service_territory | area_code |
| nrg-eia-930 | calibration_validation | utility_service_territory | area_code |
| nrg-eia-mer | calibration_validation | nation | area_code |
| nrg-eia-seds | calibration_validation | state_province | area_code |
| nrg-eurostat-energy-balances | calibration_validation | nation | area_code |
| nrg-ferc-714 | calibration_validation | utility_service_territory | area_code |
| nrg-ideal | calibration_validation | none | none |
| nrg-issda-cer | calibration_validation | none | none |
| nrg-lead | calibration_validation | building | none |
| nrg-london-lcl | calibration_validation | none | none |
| nrg-neea-rbsa-metering | calibration_validation | none | none |
| nrg-pecan-street | calibration_validation | none | none |
| nrg-plegma | calibration_validation | none | none |
| nrg-redd | calibration_validation | none | none |
| nrg-refit | calibration_validation | none | none |
| nrg-smart-umass | calibration_validation | none | none |
| nrg-uk-dale | calibration_validation | none | none |
| occ-ashrae-ob-db | operation_use | building | attribute_only |
| occ-atus | operation_use | county | area_code |
| occ-comfort-db2 | operation_use | building | area_code |
| occ-ecobee-dyd | operation_use | unknown | none |
| occ-hetus | operation_use | nation | area_code |
| occ-mobility | operation_use | county | area_code |
| occ-uk-tus | operation_use | unknown | none |
| sim-buildings-900k | reference_simulation | county | none |
| sim-comstock-eulp | reference_simulation | county | area_code |
| sim-model-america | reference_simulation | county | none |
| sim-resstock-eulp | reference_simulation | county | area_code |
| wx-argonne-future-weather | boundary_conditions | grid_cell_coarse | area_code |
| wx-bsrn | boundary_conditions | point_station | area_code |
| wx-climate-onebuilding | boundary_conditions | point_station | area_code |
| wx-cmip6 | boundary_conditions | grid_cell_coarse | area_code |
| wx-energyplus-weather | boundary_conditions | point_station | area_code |
| wx-era5-land | boundary_conditions | grid_cell_coarse | area_code |
| wx-era5 | boundary_conditions | grid_cell_coarse | area_code |
| wx-euro-cordex | boundary_conditions | grid_cell_coarse | area_code |
| wx-merra2 | boundary_conditions | grid_cell_coarse | area_code |
| wx-na-cordex | boundary_conditions | grid_cell_coarse | area_code |
| wx-nasa-power | boundary_conditions | grid_cell_coarse | area_code |
| wx-noaa-isd | boundary_conditions | point_station | area_code |
| wx-noaa-normals | boundary_conditions | point_station | area_code |
| wx-nsrdb | boundary_conditions | grid_cell_coarse | area_code |
| wx-pvgis | boundary_conditions | grid_cell_coarse | area_code |

## S25. Reproducibility map

Each table and figure is produced by one module of the released package (`python -m <module>`), from cached model outputs, without new model calls.

| Item | Module | Output |
|---|---|---|
| Fig. 1, Section 2.3, S24 | ubem_link.analytics | catalog_*.csv |
| Figs. 2 to 4 | ubem_link.schema_figures | figure files |
| Table 4 | ubem_link.standards | ai_readiness_audit.csv |
| Table 5, Figs. 5 and 6, S23 | ubem_link.design_report, ubem_link.revision_stats | bench_design_conditions.csv, stats_conditions.csv |
| Table 6 | ubem_link.design_report | bench_t3_conventions.csv |
| Fig. 7 | ubem_link.bench_report | bench_t2_coverage.csv |
| Table 7, Fig. 8, S15 to S18 | ubem_link.endtoend, ubem_link.downstream | endtoend_*.csv, downstream_*.csv |
| Table 8, Fig. 9, S19 to S21 | ubem_link.city | city_*.csv |
| Table 9, S22 | ubem_link.city_integration | city4_*.csv |
| S6 to S14 | ubem_link.revision_stats | stats_*.csv |
| S3 | scripts/make_docs.py (category profiles) | docs/category-profiles.md |