---
search:
  boost: 2.0
---


# Enum: HeightReference 




_Reference points of a building height._



<div data-search-exclude markdown="1">

URI: [ubem_link:HeightReference](https://w3id.org/ubem-link/HeightReference)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| ground_to_roof_top | None | From ground level to the highest point of the roof |
| ground_to_eave | None | From ground level to the eave |
| ground_to_mean_roof | None | From ground level to the mean roof height |
| above_sea_level | None | Elevation above a vertical datum, not a building height |
| unknown | None | Not stated by the publisher |




## Slots

| Name | Description |
| ---  | --- |
| [height_reference](height_reference.md) | Reference points between which a building height is measured |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: HeightReference
description: Reference points of a building height.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  ground_to_roof_top:
    text: ground_to_roof_top
    description: From ground level to the highest point of the roof.
  ground_to_eave:
    text: ground_to_eave
    description: From ground level to the eave.
  ground_to_mean_roof:
    text: ground_to_mean_roof
    description: From ground level to the mean roof height.
  above_sea_level:
    text: above_sea_level
    description: Elevation above a vertical datum, not a building height.
  unknown:
    text: unknown
    description: Not stated by the publisher.

```
</details>

</div>