---
search:
  boost: 5.0
---

# Slot: time_basis 


_Clock to which timestamps refer (UTC, local standard time, or local time with daylight saving)._



<div data-search-exclude markdown="1">



URI: [ubem_link:time_basis](https://w3id.org/ubem-link/time_basis)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [WeatherProfile](WeatherProfile.md) | Weather and climate data used as boundary conditions: observed station record... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [TimeBasis](TimeBasis.md) |
| Domain Of | [WeatherProfile](WeatherProfile.md) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:time_basis |
| native | ubem_link:time_basis |




## LinkML Source

<details>
```yaml
name: time_basis
description: Clock to which timestamps refer (UTC, local standard time, or local time
  with daylight saving).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- WeatherProfile
range: TimeBasis

```
</details></div>