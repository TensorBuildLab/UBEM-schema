---
search:
  boost: 5.0
---

# Slot: weather_file_format 


_Formats in which weather is released, which decide whether a simulation engine can read it directly._



<div data-search-exclude markdown="1">



URI: [ubem_link:weather_file_format](https://w3id.org/ubem-link/weather_file_format)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [WeatherProfile](WeatherProfile.md) | Weather and climate data used as boundary conditions: observed station record... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [WeatherFileFormat](WeatherFileFormat.md) |
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
| self | ubem_link:weather_file_format |
| native | ubem_link:weather_file_format |




## LinkML Source

<details>
```yaml
name: weather_file_format
description: Formats in which weather is released, which decide whether a simulation
  engine can read it directly.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- WeatherProfile
range: WeatherFileFormat
multivalued: true

```
</details></div>