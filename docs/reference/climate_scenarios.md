---
search:
  boost: 5.0
---

# Slot: climate_scenarios 


_Emission or socio-economic scenarios of a projection (for example SSP2-4.5, RCP8.5)._



<div data-search-exclude markdown="1">



URI: [ubem_link:climate_scenarios](https://w3id.org/ubem-link/climate_scenarios)
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
| self | ubem_link:climate_scenarios |
| native | ubem_link:climate_scenarios |




## LinkML Source

<details>
```yaml
name: climate_scenarios
description: Emission or socio-economic scenarios of a projection (for example SSP2-4.5,
  RCP8.5).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- WeatherProfile
range: string
multivalued: true

```
</details></div>