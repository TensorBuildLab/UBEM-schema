---
search:
  boost: 5.0
---

# Slot: building_sectors 


_Building sectors covered._



<div data-search-exclude markdown="1">



URI: [ubem_link:building_sectors](https://w3id.org/ubem-link/building_sectors)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [OperationProfile](OperationProfile.md) | Occupancy, occupant behavior, schedules, setpoints and time use |  no  |
| [CharacteristicsProfile](CharacteristicsProfile.md) | Non-geometric building characteristics (use type, vintage, envelope, systems,... |  no  |
| [SimulationProfile](SimulationProfile.md) | Reference simulations and model libraries: synthetic building-stock outputs a... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [BuildingSector](BuildingSector.md) |
| Domain Of | [OperationProfile](OperationProfile.md), [CharacteristicsProfile](CharacteristicsProfile.md), [SimulationProfile](SimulationProfile.md) |
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
| self | ubem_link:building_sectors |
| native | ubem_link:building_sectors |




## LinkML Source

<details>
```yaml
name: building_sectors
description: Building sectors covered.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- OperationProfile
- CharacteristicsProfile
- SimulationProfile
range: BuildingSector
multivalued: true

```
</details></div>