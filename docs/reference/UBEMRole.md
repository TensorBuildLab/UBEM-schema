---
search:
  boost: 2.0
---


# Enum: UBEMRole 




_The UBEM workflow step a dataset or concept serves._



<div data-search-exclude markdown="1">

URI: [ubem_link:UBEMRole](https://w3id.org/ubem-link/UBEMRole)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| boundary_conditions | None | Weather and climate drivers (observed, reanalysis, typical-year, projections) |
| geometry_inventory | None | Location and shape of buildings (footprints, heights, 3D models, parcels) |
| building_characteristics | None | Non-geometric attributes (use type, vintage, envelope, systems, fuels, floor ... |
| operation_use | None | Occupancy, schedules, occupant behavior, setpoints, plug loads |
| calibration_validation | None | Measured or reported energy use at any scale |
| reference_simulation | None | Synthetic building-stock model outputs and model libraries |
| context_coupling | None | Socio-economic, land use, grid emissions, tariffs, urban microclimate |




## Slots

| Name | Description |
| ---  | --- |
| [ubem_roles](ubem_roles.md) | UBEM workflow steps the dataset feeds; first value is the primary role |
| [concept_role](concept_role.md) | UBEM workflow role the concept belongs to |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: UBEMRole
description: The UBEM workflow step a dataset or concept serves.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  boundary_conditions:
    text: boundary_conditions
    description: Weather and climate drivers (observed, reanalysis, typical-year,
      projections).
  geometry_inventory:
    text: geometry_inventory
    description: Location and shape of buildings (footprints, heights, 3D models,
      parcels).
  building_characteristics:
    text: building_characteristics
    description: Non-geometric attributes (use type, vintage, envelope, systems, fuels,
      floor area).
  operation_use:
    text: operation_use
    description: Occupancy, schedules, occupant behavior, setpoints, plug loads.
  calibration_validation:
    text: calibration_validation
    description: Measured or reported energy use at any scale.
  reference_simulation:
    text: reference_simulation
    description: Synthetic building-stock model outputs and model libraries.
  context_coupling:
    text: context_coupling
    description: Socio-economic, land use, grid emissions, tariffs, urban microclimate.

```
</details>

</div>