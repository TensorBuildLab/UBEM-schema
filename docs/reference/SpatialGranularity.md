---
search:
  boost: 2.0
---


# Enum: SpatialGranularity 




_Ordered from finest to coarsest (see `rank` annotation)._



<div data-search-exclude markdown="1">

URI: [ubem_link:SpatialGranularity](https://w3id.org/ubem-link/SpatialGranularity)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| point_station | None | Individual measurement points such as weather stations |
| building | None | Individual buildings or footprints |
| parcel | None | Individual land parcels or lots |
| grid_cell_fine | None | Raster or model grid cells of 1 km or finer |
| census_block_group | None | U |
| census_tract | None | U |
| postal_code | None | Postal or ZIP codes |
| grid_cell_coarse | None | Raster or model grid cells coarser than 1 km |
| county | None | Counties or equivalent second-level administrative units |
| city | None | Cities or municipalities |
| utility_service_territory | None | Service territories of electric or gas utilities |
| state_province | None | States, provinces or equivalent first-level administrative units |
| climate_zone | None | Climate zones (for example ASHRAE or IECC zones) |
| census_region_division | None | U |
| nation | None | Whole countries, with no finer location |
| none | None | No location released |
| unknown | None | Could not be verified from public documentation |




## Slots

| Name | Description |
| ---  | --- |
| [spatial_granularity](spatial_granularity.md) | Finest location detail released publicly |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: SpatialGranularity
description: Ordered from finest to coarsest (see `rank` annotation).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  point_station:
    text: point_station
    description: Individual measurement points such as weather stations.
    annotations:
      rank:
        tag: rank
        value: 1
  building:
    text: building
    description: Individual buildings or footprints.
    annotations:
      rank:
        tag: rank
        value: 1
  parcel:
    text: parcel
    description: Individual land parcels or lots.
    annotations:
      rank:
        tag: rank
        value: 2
  grid_cell_fine:
    text: grid_cell_fine
    description: Raster or model grid cells of 1 km or finer.
    annotations:
      rank:
        tag: rank
        value: 3
  census_block_group:
    text: census_block_group
    description: U.S. census block groups (about 600 to 3,000 people).
    annotations:
      rank:
        tag: rank
        value: 4
  census_tract:
    text: census_tract
    description: U.S. census tracts (about 4,000 people).
    annotations:
      rank:
        tag: rank
        value: 5
  postal_code:
    text: postal_code
    description: Postal or ZIP codes.
    annotations:
      rank:
        tag: rank
        value: 5
  grid_cell_coarse:
    text: grid_cell_coarse
    description: Raster or model grid cells coarser than 1 km.
    annotations:
      rank:
        tag: rank
        value: 6
  county:
    text: county
    description: Counties or equivalent second-level administrative units.
    annotations:
      rank:
        tag: rank
        value: 7
  city:
    text: city
    description: Cities or municipalities.
    annotations:
      rank:
        tag: rank
        value: 7
  utility_service_territory:
    text: utility_service_territory
    description: Service territories of electric or gas utilities.
    annotations:
      rank:
        tag: rank
        value: 8
  state_province:
    text: state_province
    description: States, provinces or equivalent first-level administrative units.
    annotations:
      rank:
        tag: rank
        value: 9
  climate_zone:
    text: climate_zone
    description: Climate zones (for example ASHRAE or IECC zones).
    annotations:
      rank:
        tag: rank
        value: 10
  census_region_division:
    text: census_region_division
    description: U.S. census regions or divisions.
    annotations:
      rank:
        tag: rank
        value: 10
  nation:
    text: nation
    description: Whole countries, with no finer location.
    annotations:
      rank:
        tag: rank
        value: 11
  none:
    text: none
    description: No location released
    annotations:
      rank:
        tag: rank
        value: 12
  unknown:
    text: unknown
    description: Could not be verified from public documentation
    annotations:
      rank:
        tag: rank
        value: 99

```
</details>

</div>