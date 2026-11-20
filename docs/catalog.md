# Catalog of open UBEM datasets

Generated from `catalog/datasets/`; do not edit by hand. Search it with `ubem-link catalog --role ... --key ... --granularity ...`.

| Primary role | Datasets |
|---|---|
| `geometry_inventory` | 24 |
| `calibration_validation` | 21 |
| `building_characteristics` | 16 |
| `boundary_conditions` | 15 |
| `operation_use` | 7 |
| `reference_simulation` | 5 |
| `context_coupling` | 5 |

| Id | Dataset | Roles | Finest granularity | Join keys |
|---|---|---|---|---|
| `chr-ahs` | AHS PUF | building_characteristics | census_region_division | census_region_division, building_type |
| `chr-bedes` | BEDES | building_characteristics | none |  |
| `chr-bps` | Census BPS | building_characteristics, context_coupling | city | fips_state, fips_county, building_type |
| `chr-buildingsync` | BuildingSync | building_characteristics | none |  |
| `chr-cbecs-2018` | CBECS 2018 | building_characteristics, calibration_validation | census_region_division | census_region_division, building_type |
| `chr-doe-bpd` | DOE BPD | building_characteristics, calibration_validation | none | building_type, climate_zone_ashrae |
| `chr-doe-prototypes` | DOE prototype buildings | reference_simulation, building_characteristics | climate_zone | climate_zone_ashrae, building_type, vintage |
| `chr-energy-codes-status` | BECP state code status | building_characteristics, context_coupling | state_province |  |
| `chr-eu-bso` | EU BSO | building_characteristics, calibration_validation | nation | country_iso, building_type |
| `chr-france-dpe` | France DPE (existing dwellings) | building_characteristics, calibration_validation | building | address, postal_code, building_type, vintage |
| `chr-germany-zensus-2022` | Germany Zensus 2022 grid | building_characteristics, context_coupling | grid_cell_fine | grid_cell, vintage |
| `chr-hotmaps` | Hotmaps building stock | building_characteristics | grid_cell_fine | grid_cell, country_iso, nuts_region, vintage |
| `chr-ireland-ber` | Ireland BER Research Tool | building_characteristics | unknown |  |
| `chr-nyc-ll84` | NYC LL84 benchmarking | calibration_validation, building_characteristics | building | building_id, parcel_id, address, postal_code, lat_lon, building_type |
| `chr-nyc-pluto` | NYC PLUTO | building_characteristics, context_coupling | parcel | parcel_id, lat_lon, census_tract, postal_code, building_type |
| `chr-recs-2020` | RECS 2020 | building_characteristics, operation_use, calibration_validation | state_province | fips_state, census_region_division, climate_zone_iecc, building_type |
| `chr-tabula-episcope` | TABULA WebTool | building_characteristics, reference_simulation | nation | country_iso, building_type, vintage |
| `chr-uk-epc` | UK EPC (England and Wales) | building_characteristics, calibration_validation | building | address, postal_code, building_type, vintage |
| `ctx-acs` | ACS | context_coupling | census_block_group | census_block_group, census_tract, fips_county, fips_state, postal_code |
| `ctx-cambium` | Cambium | context_coupling | utility_service_territory | balancing_authority, fips_state, timestamp |
| `ctx-egrid` | eGRID | context_coupling | utility_service_territory | balancing_authority, fips_state, utility_id |
| `ctx-lcz-global` | Global LCZ map | context_coupling | grid_cell_fine | lat_lon, grid_cell |
| `ctx-urdb` | URDB | context_coupling | utility_service_territory | utility_id |
| `geo-3d-globfp` | 3D-GloBFP | geometry_inventory | building | geometry, lat_lon |
| `geo-3dbag` | 3D BAG | geometry_inventory | building | geometry, lat_lon, building_id |
| `geo-china-rooftop-2023` | China rooftop (90 cities) | geometry_inventory | building | geometry, lat_lon |
| `geo-cmab` | CMAB | geometry_inventory, building_characteristics | building | geometry, lat_lon, building_type, vintage |
| `geo-eubucco` | EUBUCCO | geometry_inventory, building_characteristics | building | geometry, lat_lon, building_id, building_type, vintage |
| `geo-ghs-obat` | GHS-OBAT | geometry_inventory, building_characteristics | building | geometry, lat_lon, building_id, vintage, building_type |
| `geo-ghsl-built` | GHS-BUILT-S/H | geometry_inventory | grid_cell_fine | grid_cell, lat_lon |
| `geo-globalbuildingatlas` | GlobalBuildingAtlas | geometry_inventory | building | geometry, lat_lon |
| `geo-google-open-buildings-25d` | Open Buildings 2.5D Temporal | geometry_inventory | grid_cell_fine | grid_cell, lat_lon |
| `geo-google-open-buildings` | Google Open Buildings v3 | geometry_inventory | building | geometry, lat_lon |
| `geo-heris-raster-footprints` | Heris rasterized footprints | geometry_inventory | grid_cell_fine | grid_cell, lat_lon |
| `geo-ms-global-footprints` | MS Global ML Building Footprints | geometry_inventory | building | geometry, lat_lon |
| `geo-ms-us-footprints` | MS US Building Footprints | geometry_inventory | building | geometry, lat_lon |
| `geo-nyc-footprints` | NYC building footprints | geometry_inventory | building | building_id, parcel_id, geometry |
| `geo-open-city-model` | Open City Model | geometry_inventory | building | geometry, lat_lon |
| `geo-osm` | OSM buildings | geometry_inventory, building_characteristics | building | geometry, lat_lon, building_id |
| `geo-overture-buildings` | Overture buildings | geometry_inventory, building_characteristics | building | geometry, lat_lon, building_id |
| `geo-plateau` | PLATEAU | geometry_inventory, building_characteristics | building | geometry, lat_lon, building_id |
| `geo-regrid-parcels` | Regrid parcels | geometry_inventory | parcel | parcel_id, address, geometry, lat_lon, fips_county |
| `geo-ubid` | UBID | geometry_inventory | building | ubid |
| `geo-usa-structures` | USA Structures | geometry_inventory | building | geometry, lat_lon, building_id |
| `geo-usgs-3dep` | USGS 3DEP | geometry_inventory | grid_cell_fine | lat_lon, geometry |
| `geo-ut-globus` | UT-GLOBUS | geometry_inventory | building | geometry, lat_lon |
| `geo-wsf3d` | WSF 3D | geometry_inventory | grid_cell_fine | grid_cell, lat_lon |
| `nrg-ashrae-gepiii` | ASHRAE GEPIII | calibration_validation | building | building_id, timestamp |
| `nrg-bdg2` | BDG2 | calibration_validation | building | building_id, timestamp |
| `nrg-desnz-subnational` | DESNZ subnational energy | calibration_validation | postal_code | postal_code, small_statistical_area, country_iso |
| `nrg-eia-861` | EIA-861 | calibration_validation | utility_service_territory | utility_id, fips_state, balancing_authority, timestamp |
| `nrg-eia-930` | EIA-930 | calibration_validation | utility_service_territory | balancing_authority, timestamp |
| `nrg-eia-mer` | EIA MER | calibration_validation | nation | timestamp, country_iso |
| `nrg-eia-seds` | EIA SEDS | calibration_validation | state_province | fips_state, timestamp |
| `nrg-eurostat-energy-balances` | Eurostat energy balances | calibration_validation | nation | country_iso, timestamp |
| `nrg-ferc-714` | FERC-714 | calibration_validation | utility_service_territory | balancing_authority, utility_id, timestamp |
| `nrg-ideal` | IDEAL | calibration_validation, operation_use | none | building_id, timestamp |
| `nrg-issda-cer` | ISSDA CER smart meter trial | calibration_validation | none | timestamp |
| `nrg-lead` | LEAD1.0 | calibration_validation | building | building_id, timestamp |
| `nrg-london-lcl` | Low Carbon London | calibration_validation | none | timestamp |
| `nrg-neea-rbsa-metering` | NEEA RBSA metering | calibration_validation, operation_use | none | building_id, timestamp |
| `nrg-pecan-street` | Pecan Street Dataport | calibration_validation, operation_use | none | building_id, timestamp |
| `nrg-plegma` | Plegma | calibration_validation, operation_use | none | building_id, timestamp |
| `nrg-redd` | REDD | calibration_validation, operation_use | none | timestamp |
| `nrg-refit` | REFIT | calibration_validation, operation_use | none | timestamp |
| `nrg-smart-umass` | Smart* | calibration_validation, operation_use | none | timestamp |
| `nrg-uk-dale` | UK-DALE | calibration_validation, operation_use | none | timestamp |
| `occ-ashrae-ob-db` | ASHRAE OB Database | operation_use, calibration_validation | building | building_type |
| `occ-atus` | ATUS | operation_use | county | fips_state, timestamp |
| `occ-comfort-db2` | ASHRAE Comfort DB II | operation_use, calibration_validation | building | building_type, climate_zone_ashrae |
| `occ-ecobee-dyd` | ecobee DYD | operation_use | unknown |  |
| `occ-hetus` | HETUS 2010 | operation_use | nation | country_iso, timestamp |
| `occ-mobility` | Google Community Mobility | operation_use, context_coupling | county | country_iso, fips_county, timestamp |
| `occ-uk-tus` | UKTUS 2014-15 | operation_use | unknown | timestamp |
| `sim-buildings-900k` | Buildings-900K | reference_simulation | county | building_id, timestamp |
| `sim-comstock-eulp` | ComStock | reference_simulation, calibration_validation | county | building_id, fips_county, building_type, vintage, climate_zone_ashrae, timestamp |
| `sim-model-america` | Model America (AutoBEM) | reference_simulation | county |  |
| `sim-resstock-eulp` | ResStock | reference_simulation, calibration_validation | county | building_id, fips_county, building_type, vintage, climate_zone_ashrae, timestamp |
| `wx-argonne-future-weather` | Argonne 12-km future weather (ClimRR) | boundary_conditions | grid_cell_coarse | lat_lon, grid_cell, timestamp |
| `wx-bsrn` | BSRN | boundary_conditions | point_station | station_id, lat_lon, timestamp |
| `wx-climate-onebuilding` | Climate.OneBuilding | boundary_conditions | point_station | lat_lon, station_id, country_iso, climate_zone_ashrae |
| `wx-cmip6` | CMIP6 | boundary_conditions | grid_cell_coarse | lat_lon, grid_cell, timestamp |
| `wx-energyplus-weather` | EnergyPlus weather | boundary_conditions | point_station | lat_lon, station_id, climate_zone_ashrae |
| `wx-era5-land` | ERA5-Land | boundary_conditions | grid_cell_coarse | lat_lon, grid_cell, timestamp |
| `wx-era5` | ERA5 | boundary_conditions | grid_cell_coarse | lat_lon, grid_cell, timestamp |
| `wx-euro-cordex` | EURO-CORDEX | boundary_conditions | grid_cell_coarse | lat_lon, grid_cell, timestamp |
| `wx-merra2` | MERRA-2 | boundary_conditions | grid_cell_coarse | lat_lon, grid_cell, timestamp |
| `wx-na-cordex` | NA-CORDEX | boundary_conditions | grid_cell_coarse | lat_lon, grid_cell, timestamp |
| `wx-nasa-power` | NASA POWER | boundary_conditions | grid_cell_coarse | lat_lon, grid_cell, timestamp |
| `wx-noaa-isd` | NOAA ISD | boundary_conditions | point_station | station_id, lat_lon, timestamp |
| `wx-noaa-normals` | NOAA Climate Normals 1991-2020 | boundary_conditions | point_station | station_id, lat_lon, fips_county |
| `wx-nsrdb` | NSRDB | boundary_conditions | grid_cell_coarse | lat_lon, grid_cell, timestamp |
| `wx-pvgis` | PVGIS | boundary_conditions | grid_cell_coarse | lat_lon, grid_cell, timestamp |
