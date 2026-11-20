---
search:
  boost: 2.0
---


# Enum: JoinKey 




_Keys in the public data through which records can be linked to other datasets._



<div data-search-exclude markdown="1">

URI: [ubem_link:JoinKey](https://w3id.org/ubem-link/JoinKey)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| lat_lon | None | Latitude and longitude of the record |
| geometry | None | A point, line or polygon geometry of the record |
| address | None | Street address of the building or site |
| parcel_id | None | Cadastral parcel or lot identifier shared with other datasets (for example BB... |
| building_id | None | Building identifier shared with other datasets (for example BIN, UPRN); not a... |
| ubid | None | Unique Building Identifier derived from the footprint |
| station_id | None | Identifier of a weather or measurement station (for example WMO or USAF id) |
| grid_cell | None | Identifier or coordinates of a raster or grid cell |
| census_block_group | None | U |
| census_tract | None | U |
| small_statistical_area | None | Non-U |
| postal_code | None | Postal or ZIP code |
| fips_county | None | U |
| fips_state | None | U |
| census_region_division | None | U |
| nuts_region | None | European NUTS region code |
| country_iso | None | ISO 3166 country code |
| utility_id | None | Identifier of an electric or gas utility (for example EIA utility id) |
| balancing_authority | None | Identifier of an electricity balancing authority |
| climate_zone_ashrae | None | ASHRAE Standard 169 climate zone |
| climate_zone_iecc | None | IECC climate zone |
| building_type | None | Building type or use class (attribute key for statistical matching only) |
| vintage | None | Construction period (attribute key for statistical matching only) |
| timestamp | None | Date and time of an observation |




## Slots

| Name | Description |
| ---  | --- |
| [join_keys](join_keys.md) | Keys present in the public data that allow records to be linked to other data... |
| [join_key](join_key.md) | Key type the variable holds, if it can link records to other datasets (for ex... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: JoinKey
description: Keys in the public data through which records can be linked to other
  datasets.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  lat_lon:
    text: lat_lon
    description: Latitude and longitude of the record.
  geometry:
    text: geometry
    description: A point, line or polygon geometry of the record.
  address:
    text: address
    description: Street address of the building or site.
  parcel_id:
    text: parcel_id
    description: Cadastral parcel or lot identifier shared with other datasets (for
      example BBL).
  building_id:
    text: building_id
    description: Building identifier shared with other datasets (for example BIN,
      UPRN); not a dataset-internal row id.
  ubid:
    text: ubid
    description: Unique Building Identifier derived from the footprint.
  station_id:
    text: station_id
    description: Identifier of a weather or measurement station (for example WMO or
      USAF id).
  grid_cell:
    text: grid_cell
    description: Identifier or coordinates of a raster or grid cell.
  census_block_group:
    text: census_block_group
    description: U.S. census block group code.
  census_tract:
    text: census_tract
    description: U.S. census tract code.
  small_statistical_area:
    text: small_statistical_area
    description: Non-U.S. small statistical areas such as UK LSOA/MSOA or national
      census grid ids
  postal_code:
    text: postal_code
    description: Postal or ZIP code.
  fips_county:
    text: fips_county
    description: U.S. FIPS county code.
  fips_state:
    text: fips_state
    description: U.S. FIPS state code.
  census_region_division:
    text: census_region_division
    description: U.S. census region or division code.
  nuts_region:
    text: nuts_region
    description: European NUTS region code.
  country_iso:
    text: country_iso
    description: ISO 3166 country code.
  utility_id:
    text: utility_id
    description: Identifier of an electric or gas utility (for example EIA utility
      id).
  balancing_authority:
    text: balancing_authority
    description: Identifier of an electricity balancing authority.
  climate_zone_ashrae:
    text: climate_zone_ashrae
    description: ASHRAE Standard 169 climate zone.
  climate_zone_iecc:
    text: climate_zone_iecc
    description: IECC climate zone.
  building_type:
    text: building_type
    description: Building type or use class (attribute key for statistical matching
      only).
  vintage:
    text: vintage
    description: Construction period (attribute key for statistical matching only).
  timestamp:
    text: timestamp
    description: Date and time of an observation.

```
</details>

</div>