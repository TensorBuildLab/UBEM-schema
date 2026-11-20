---
search:
  boost: 5.0
---

# Slot: weather_year_type 


_Kind of weather year or series: actual series, actual or typical meteorological year, normals, or projection._



<div data-search-exclude markdown="1">



URI: [ubem_link:weather_year_type](https://w3id.org/ubem-link/weather_year_type)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [WeatherProfile](WeatherProfile.md) | Weather and climate data used as boundary conditions: observed station record... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [WeatherYearType](WeatherYearType.md) |
| Domain Of | [WeatherProfile](WeatherProfile.md) |
### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:weather_year_type |
| native | ubem_link:weather_year_type |




## LinkML Source

<details>
```yaml
name: weather_year_type
description: 'Kind of weather year or series: actual series, actual or typical meteorological
  year, normals, or projection.'
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- WeatherProfile
range: WeatherYearType
multivalued: true

```
</details></div>