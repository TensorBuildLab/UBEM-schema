# Meta-Urban open-data catalog

One YAML file per dataset in `datasets/`, following `TEMPLATE.yaml`. Each file is a `DatasetProfile`
instance of the Meta-Urban 2.0 schema (`../schema/meta_urban.yaml`). Validate with:

```bash
python -m meta_urban.validate catalog/datasets
```

## Inclusion criteria

1. The data can be obtained by anyone, at no cost, either directly or after free registration
   (`access_level` in `open_download`, `open_api`, `registration_required`). Datasets that need a data-use
   agreement or payment may be listed with `request_or_agreement` / `restricted_commercial` only when they are
   widely used in UBEM, so that the gap analysis can count them.
2. The data feed at least one UBEM workflow step (`ubem_roles`).
3. The data have national, multinational, or global scope, or are a city dataset that is a de facto
   reference (for example NYC Local Law 84). City portals in general are out of scope.
4. Every field is verified against the publisher's page or a peer-reviewed descriptor. Unknown means `null`.

## Faceted taxonomy (controlled values)

The 2023 taxonomy mixed three different things in one list: what the data describe (weather, geometry),
how coarse they are (macroscopic vs. microscopic energy data), and how they are distributed (data lake).
Version 2.0 separates them into independent facets.

### `ubem_roles` (UBEMRole): which UBEM workflow step the data feed
| value | meaning |
|---|---|
| `boundary_conditions` | Weather and climate drivers: observed, reanalysis, typical-year, future projections |
| `geometry_inventory` | Where buildings are and their shape: footprints, heights, 3D models, parcels |
| `building_characteristics` | Non-geometric attributes: use type, vintage, envelope, HVAC, fuel, floor area |
| `operation_use` | Occupancy, schedules, occupant behavior, setpoints, plug loads |
| `calibration_validation` | Measured or reported energy use at any scale |
| `reference_simulation` | Synthetic building-stock model outputs and model libraries (e.g., ComStock/ResStock) |
| `context_coupling` | Socio-economic, land use, grid emissions, tariffs, urban microclimate |

### `geographic_scope` (GeographicScope)
`global`, `multinational`, `national`, `subnational`, `city`

### `spatial_granularity` (SpatialGranularity): finest location detail released publicly
`point_station`, `building`, `parcel`, `grid_cell_fine` (<= 1 km), `grid_cell_coarse` (> 1 km),
`census_block_group`, `census_tract`, `postal_code`, `county`, `city`, `utility_service_territory`,
`state_province`, `census_region_division`, `climate_zone`, `nation`, `none`

### `statistical_nature` (StatisticalNature)
`census_complete`, `sample_survey_weighted`, `administrative_record`, `measured_monitoring`,
`remote_sensing_derived`, `crowdsourced`, `reanalysis_model`, `typical_year_synthetic`,
`climate_projection`, `simulation_synthetic`, `standard_or_code`, `compilation`

### `access_level` (AccessLevel)
`open_download`, `open_api`, `registration_required`, `request_or_agreement`, `restricted_commercial`

### `join_keys` (JoinKey): fields that let the dataset be linked to others
`lat_lon`, `geometry`, `address`, `parcel_id`, `building_id`, `ubid`, `station_id`, `grid_cell`,
`census_block_group`, `census_tract`, `postal_code`, `fips_county`, `fips_state`, `census_region_division`,
`nuts_region`, `country_iso`, `utility_id`, `balancing_authority`, `climate_zone_ashrae`,
`climate_zone_iecc`, `building_type`, `vintage`, `timestamp`

### `temporal_resolution`
ISO 8601 duration (`PT1M`, `PT15M`, `PT1H`, `P1D`, `P1M`, `P1Y`), or `static`, or `irregular`.
