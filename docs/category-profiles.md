# Category profiles

Generated from `schema/ubem_link.yaml` by `scripts/make_docs.py`; do not edit by hand.

Category-specific part of a dataset profile: what a modeler must know about one kind of UBEM data before using it. There is one profile class per UBEM workflow role. Existing classifications of open UBEM data record this information as free-text checklists; here every field is typed with a closed value list, macroscopic and microscopic energy data share EnergyProfile and differ in energy_data_scale, and a data lake is a Catalog of profiles rather than a category.

Every category profile also has `provides_concepts` (ids of UBEM-Link concepts the dataset provides) and `metadata_standards` (standards the publisher already uses).

## WeatherProfile

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

## GeometryProfile

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

## OperationProfile

Key in a dataset profile: `operation_profile`; UBEM role: `operation_use`.

Occupancy, occupant behavior, schedules, setpoints and time use.

| Field | | Meaning | Allowed values |
|---|---|---|---|
| `behavior_types` | required, list | Kinds of occupant behavior or building operation recorded. | `occupancy_presence`, `hvac_operation`, `thermostat_setpoint`, `window_operation`, `lighting_operation`, `appliance_plug_loads`, `hot_water_use`, `thermal_comfort`, `time_use_activities`, `mobility` |
| `control_actions` | list | Occupant control actions recorded. | `thermostat_adjustment`, `hvac_on_off`, `lighting_on_off`, `window_open_close`, `shading_adjustment`, `appliance_on_off` |
| `collection_method` | list | How the behavior or operation data were collected. | `sensors_or_logs`, `connected_devices`, `survey_or_diary`, `field_study_compilation`, `mobile_location` |
| `building_sectors` | list | Building sectors covered. | `residential`, `commercial`, `industrial`, `all` |

## CharacteristicsProfile

Key in a dataset profile: `characteristics_profile`; UBEM role: `building_characteristics`.

Non-geometric building characteristics (use type, vintage, envelope, systems, fuels) from surveys, administrative records, certificates and dictionaries.

| Field | | Meaning | Allowed values |
|---|---|---|---|
| `data_form` | required, list | Whether the data are records of individual units (microdata or building records) or published distributions (aggregate tables). | `microdata`, `building_records`, `aggregate_tables`, `dictionary_or_standard`, `archetype_library` |
| `building_sectors` | list | Building sectors covered. | `residential`, `commercial`, `industrial`, `all` |
| `representativeness` |  | How the covered buildings relate to the building stock, which decides whether results generalize. | `probability_sample`, `complete_population`, `mandated_subset`, `voluntary_or_convenience`, `synthetic`, `unknown` |
| `coverage_threshold` |  | Size or other threshold that decides which buildings are covered (for example 'more than 25,000 ft²'). |  |
| `cross_tabulations` | list | For aggregate tables, the joint distributions published, each as concept ids joined by ' x '. |  |

## EnergyProfile

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

## SimulationProfile

Key in a dataset profile: `simulation_profile`; UBEM role: `reference_simulation`.

Reference simulations and model libraries: synthetic building-stock outputs and prototype models.

| Field | | Meaning | Allowed values |
|---|---|---|---|
| `simulation_engine` |  | Simulation engine that produced the data (for example EnergyPlus). |  |
| `stock_representation` |  | How the simulated building stock is represented. | `sampled_models`, `building_by_building`, `prototype_library` |
| `weather_basis` |  | Weather used for the simulations (for example AMY 2018, TMY3). |  |
| `building_sectors` | list | Building sectors covered. | `residential`, `commercial`, `industrial`, `all` |

## ContextProfile

Key in a dataset profile: `context_profile`; UBEM role: `context_coupling`.

Context and coupling data: socio-economic data, land use, grid emissions, tariffs and urban climate.

| Field | | Meaning | Allowed values |
|---|---|---|---|
| `context_kind` | list | Kind of context or coupling data. | `grid_emissions`, `energy_tariffs`, `land_use`, `socio_economic`, `urban_climate_zones` |

