---
search:
  boost: 5.0
---

# Slot: metadata_standards 


_Metadata standards or schemas the publisher already uses (for example Brick, BuildingSync, DDI-Codebook, CityGML)._



<div data-search-exclude markdown="1">



URI: [ubem_link:metadata_standards](https://w3id.org/ubem-link/metadata_standards)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CategoryProfile](CategoryProfile.md) | Category-specific part of a dataset profile: what a modeler must know about o... |  no  |
| [WeatherProfile](WeatherProfile.md) | Weather and climate data used as boundary conditions: observed station record... |  no  |
| [GeometryProfile](GeometryProfile.md) | Building stock geometry and inventory: footprints, heights, 3D city models an... |  no  |
| [OperationProfile](OperationProfile.md) | Occupancy, occupant behavior, schedules, setpoints and time use |  no  |
| [CharacteristicsProfile](CharacteristicsProfile.md) | Non-geometric building characteristics (use type, vintage, envelope, systems,... |  no  |
| [EnergyProfile](EnergyProfile.md) | Measured or reported energy use for calibration and validation, from national... |  no  |
| [SimulationProfile](SimulationProfile.md) | Reference simulations and model libraries: synthetic building-stock outputs a... |  no  |
| [ContextProfile](ContextProfile.md) | Context and coupling data: socio-economic data, land use, grid emissions, tar... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [CategoryProfile](CategoryProfile.md) |
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
| self | ubem_link:metadata_standards |
| native | ubem_link:metadata_standards |




## LinkML Source

<details>
```yaml
name: metadata_standards
description: Metadata standards or schemas the publisher already uses (for example
  Brick, BuildingSync, DDI-Codebook, CityGML).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- CategoryProfile
range: string
multivalued: true

```
</details></div>