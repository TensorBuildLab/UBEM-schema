---
search:
  boost: 5.0
---

# Slot: station_id_scheme 


_Identifier system of the stations (for example WMO, USAF-WBAN, GHCN)._



<div data-search-exclude markdown="1">



URI: [ubem_link:station_id_scheme](https://w3id.org/ubem-link/station_id_scheme)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [WeatherProfile](WeatherProfile.md) | Weather and climate data used as boundary conditions: observed station record... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [WeatherProfile](WeatherProfile.md) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:station_id_scheme |
| native | ubem_link:station_id_scheme |




## LinkML Source

<details>
```yaml
name: station_id_scheme
description: Identifier system of the stations (for example WMO, USAF-WBAN, GHCN).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- WeatherProfile
range: string

```
</details></div>