---
search:
  boost: 2.0
---


# Enum: LevelOfDetail 




_CityGML level of detail._



<div data-search-exclude markdown="1">

URI: [ubem_link:LevelOfDetail](https://w3id.org/ubem-link/LevelOfDetail)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| lod0 | None | Footprint or roof-edge polygon |
| lod1 | None | Block model: footprint extruded to one height |
| lod2 | None | Roof shapes and wall surfaces |
| lod3 | None | Architectural model with openings such as windows and doors |
| lod4 | None | Interior structures (CityGML 2 |




## Slots

| Name | Description |
| ---  | --- |
| [levels_of_detail](levels_of_detail.md) | CityGML levels of detail provided |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: LevelOfDetail
description: CityGML level of detail.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  lod0:
    text: lod0
    description: Footprint or roof-edge polygon.
  lod1:
    text: lod1
    description: 'Block model: footprint extruded to one height.'
  lod2:
    text: lod2
    description: Roof shapes and wall surfaces.
  lod3:
    text: lod3
    description: Architectural model with openings such as windows and doors.
  lod4:
    text: lod4
    description: Interior structures (CityGML 2.0 only).

```
</details>

</div>