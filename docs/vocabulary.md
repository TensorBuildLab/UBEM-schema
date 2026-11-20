# Concept vocabulary

Generated from `schema/vocab/ubem_concepts.yaml`; do not edit by hand.

## record bookkeeping (`record`)

Variables that describe the data record rather than the building, such as identifiers, weights and flags.

| Concept | Definition | Canonical unit | Links |
|---|---|---|---|
| `record_identifier` record identifier | Identifier of a record, building, meter, station or respondent within the dataset. |  | 1 |
| `survey_weight` survey analysis weight | Final sampling weight that expands a sampled record to the population it represents. |  |  |
| `replicate_weight` replicate weight | Replicate weight used to estimate sampling variance (jackknife, balanced repeated replication). |  |  |
| `imputation_flag` imputation or quality flag | Indicator that another variable's value was imputed, edited, top-coded or suppressed. |  | 2 |
| `timestamp` timestamp | Date and time the observation refers to. |  | 3 |
| `survey_reference_detail` survey administration detail | Information about how the record was collected (respondent type, interview mode, data source), not about the building. |  | 1 |

## location (`location`)

Where the building, station or region is.

| Concept | Definition | Canonical unit | Links |
|---|---|---|---|
| `geographic_coordinates` geographic coordinates | Latitude and longitude (WGS84) of a building, station or grid cell centroid. |  | 6 |
| `administrative_region` administrative or statistical region | Region the record belongs to, such as country, census region or division, state, county, city, tract or postal code. |  | 6 |
| `climate_zone` climate zone | Climate classification of the location (ASHRAE/IECC climate zone, building America zone, Koppen class). |  | 2 |
| `urban_rural_indicator` urban or rural indicator | Classification of the location by settlement type or density. |  | 1 |

## weather and climate variable (`weather`)

Outdoor meteorological driver of building heat and mass balance.

| Concept | Definition | Canonical unit | Links |
|---|---|---|---|
| `dry_bulb_temperature` outdoor dry-bulb temperature | Outdoor air temperature measured by a thermometer shielded from radiation and moisture. | unit:DEG_C | 4 |
| `dew_point_temperature` outdoor dew-point temperature | Temperature to which outdoor air must be cooled at constant pressure to reach saturation. | unit:DEG_C | 2 |
| `relative_humidity` outdoor relative humidity | Ratio of the partial pressure of water vapor in outdoor air to its saturation pressure. | unit:PERCENT | 4 |
| `atmospheric_pressure` atmospheric station pressure | Atmospheric pressure at the station elevation. | unit:PA | 2 |
| `global_horizontal_irradiance` global horizontal irradiance | Total solar irradiance on a horizontal surface. | unit:W-PER-M2 | 4 |
| `direct_normal_irradiance` direct normal irradiance | Beam solar irradiance on a surface normal to the sun. | unit:W-PER-M2 | 3 |
| `diffuse_horizontal_irradiance` diffuse horizontal irradiance | Sky-diffuse solar irradiance on a horizontal surface. | unit:W-PER-M2 | 3 |
| `wind_speed` wind speed | Horizontal wind speed at the reference height. | unit:M-PER-SEC | 4 |
| `wind_direction` wind direction | Direction from which the wind blows, clockwise from north. | unit:DEG | 2 |
| `precipitation` precipitation | Liquid-equivalent precipitation depth over the time step. | unit:MilliM | 1 |
| `degree_days` heating or cooling degree days | Sum over a period of the difference between a base temperature and daily mean outdoor temperature. | unit:DEG_C | 2 |

## building geometry (`geometry`)

Size and shape of the building envelope.

| Concept | Definition | Canonical unit | Links |
|---|---|---|---|
| `footprint` building footprint | Polygon of the building's ground outline. |  | 1 |
| `building_height` building height | Height of the building from ground to roof (state reference points where known). | unit:M | 3 |
| `floors_above_ground` number of floors above ground | Count of storeys above grade. |  | 2 |
| `floors_below_ground` floors below ground or basement | Count or presence of storeys below grade, including basements. |  | 2 |
| `floor_to_ceiling_height` floor-to-ceiling height | Typical vertical distance between floor and ceiling. | unit:M | 1 |
| `building_shape` building plan shape | Plan shape of the building (rectangle, L, U, H, courtyard, other). |  | 1 |
| `roof_shape` roof shape or tilt | Roof geometry type or slope (flat, pitched, gable, hip). |  | 2 |
| `window_to_wall_ratio` window-to-wall ratio | Share of exterior wall area that is glazed. | unit:PERCENT | 2 |

## building characteristic (`characteristics`)

Non-geometric attribute of a building that determines its thermal and energy behavior.

| Concept | Definition | Canonical unit | Links |
|---|---|---|---|
| `building_use_type` building use type | Principal activity or function of the building (office, retail, education, single-family, etc.). |  | 5 |
| `secondary_use` secondary use or mixed use detail | Additional activities in the building, or a finer subtype of its principal activity. |  |  |
| `gross_floor_area` gross floor area | Total floor area within the exterior walls, all storeys. | unit:M2 | 4 |
| `year_of_construction` year of construction | Year (or period) the building was completed. |  | 2 |
| `renovation` renovation or retrofit | Whether and how the building was renovated (envelope, systems, lighting, additions). |  | 1 |
| `wall_construction` exterior wall construction | Material or assembly type of exterior walls. |  | 2 |
| `roof_construction` roof construction | Material or assembly type of the roof. |  | 2 |
| `window_properties` window and glazing properties | Window type, number of panes, frame, coatings, tinting or shading. |  | 4 |
| `insulation` insulation level | Presence, level or upgrade of thermal insulation in walls, roof or floors. |  | 4 |
| `heating_system` space heating system | Type, presence or share of space heating equipment (furnace, boiler, heat pump, district heat). |  | 2 |
| `cooling_system` space cooling system | Type, presence or share of space cooling equipment (chiller, packaged unit, central AC, room AC). |  | 2 |
| `ventilation_system` ventilation and air distribution | Ventilation, economizer, variable-air-volume or air distribution features. |  | 7 |
| `water_heating_system` water heating system | Type, fuel or size of domestic or service hot-water equipment. |  | 3 |
| `lighting_system` lighting system | Lamp types, lit share of floor area, or lighting controls. |  | 3 |
| `plug_and_process_equipment` plug and process equipment | Presence or count of appliances, computers, refrigeration, cooking or other process equipment. |  | 3 |
| `energy_sources_used` energy sources used | Which fuels or energy carriers are used in the building, overall or for a given end use. |  | 2 |
| `onsite_generation` on-site generation or storage | On-site renewable or fossil generation, cogeneration, or energy storage. |  | 8 |
| `building_controls` building controls and energy management | Energy management systems, smart thermostats, demand response participation, or control strategies. |  | 3 |
| `dwelling_units` number of dwelling units | Number of housing units in the building. |  | 2 |
| `ownership_tenure` ownership, occupancy and tenure | Who owns or occupies the building and how (owner-occupied, rented, government, vacant share). |  | 4 |
| `rooms_and_spaces` rooms and space counts | Counts or shares of specific spaces (bedrooms, classrooms, seats, beds, server rooms). |  | 3 |

## gross floor area (`gross_floor_area`)

Total floor area within the exterior walls, all storeys.

| Concept | Definition | Canonical unit | Links |
|---|---|---|---|
| `floor_area_category` floor area category | Binned floor area class. |  |  |

## operation and use (`operation`)

How the building and its systems are used over time.

| Concept | Definition | Canonical unit | Links |
|---|---|---|---|
| `occupant_count` number of occupants | Number of people who work in, live in or occupy the building. |  | 3 |
| `operating_hours` operating hours and schedule | Hours or days per week the building or a space is open or occupied. |  | 2 |
| `thermostat_setpoint` thermostat setpoint | Indoor temperature setpoint for heating or cooling, occupied or unoccupied. | unit:DEG_C | 6 |
| `equipment_usage_behavior` equipment usage behavior | How often or how long occupants use appliances or systems. |  |  |
| `time_use_activity` time-use activity | Activity episodes of persons with time, duration and location. |  |  |
| `thermal_comfort_response` thermal comfort response | Occupant thermal sensation, preference or acceptability vote. |  |  |
| `occupant_control_action` occupant control action | Observed occupant interaction with building systems (window opening, light switching, blinds, thermostat change). |  |  |
| `indoor_environment` indoor environmental condition | Measured indoor temperature, humidity, CO2, illuminance or air quality. |  | 5 |
| `household_demographics` household or occupant demographics | Socio-demographic attributes of occupants (age, income, education, employment). |  | 3 |

## energy use (`energy`)

Energy consumed, demanded or paid for by a building, stock or region.

| Concept | Definition | Canonical unit | Links |
|---|---|---|---|
| `total_energy_consumption` total site energy consumption | Total site energy over a period, all carriers combined. | unit:KiloW-HR | 2 |
| `electricity_consumption` electricity consumption | Electricity used over a period. | unit:KiloW-HR | 2 |
| `natural_gas_consumption` natural gas consumption | Natural gas used over a period. | unit:KiloW-HR | 2 |
| `other_fuel_consumption` other fuel consumption | Fuel oil, propane, district heat or steam, wood or other carriers used over a period. | unit:KiloW-HR | 4 |
| `end_use_energy` end-use energy consumption | Energy attributed to one end use (heating, cooling, ventilation, water heating, lighting, cooking, refrigeration, office equipment, other). | unit:KiloW-HR | 2 |
| `energy_expenditure` energy expenditure | Money spent on energy over a period. | unit:CCY_USD | 1 |
| `energy_use_intensity` energy use intensity | Energy use per unit floor area over a year. | unit:KiloW-HR-PER-M2 | 1 |
| `load_timeseries` interval load or meter time series | Energy or power at sub-annual intervals from a meter, sub-meter or aggregate. | unit:KiloW | 3 |
| `peak_demand` peak demand | Maximum power over a period. | unit:KiloW | 3 |
| `primary_energy_or_emissions` primary energy or emissions | Source energy, primary energy or greenhouse gas emissions attributed to energy use. |  | 3 |

## context and coupling variable (`context`)

Non-building variable needed to interpret or couple UBEM results (grid, prices, land use, population).

| Concept | Definition | Canonical unit | Links |
|---|---|---|---|
| `grid_emission_factor` grid emission factor | Emissions per unit of electricity generated or consumed in a grid region. |  | 3 |
| `energy_price` energy price or tariff | Price per unit energy or demand, or tariff structure. |  | 2 |
| `land_use` land use or land cover | Land use class or land cover of the parcel or cell. |  |  |

