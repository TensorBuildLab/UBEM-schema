---
search:
  boost: 2.0
---


# Enum: HeightSource 




_How building heights were obtained._



<div data-search-exclude markdown="1">

URI: [ubem_link:HeightSource](https://w3id.org/ubem-link/HeightSource)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| lidar | None | Measured from airborne laser scanning |
| photogrammetry | None | Measured from stereo or oblique imagery |
| plans_or_records | None | Taken from building plans or administrative records |
| model_estimated | None | Estimated by a statistical or machine-learning model |
| derived_from_floors | None | Computed from the number of floors and an assumed floor height |
| none | None | The dataset has no building heights |




## Slots

| Name | Description |
| ---  | --- |
| [height_source](height_source.md) | How building heights were obtained |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: HeightSource
description: How building heights were obtained.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  lidar:
    text: lidar
    description: Measured from airborne laser scanning.
  photogrammetry:
    text: photogrammetry
    description: Measured from stereo or oblique imagery.
  plans_or_records:
    text: plans_or_records
    description: Taken from building plans or administrative records.
  model_estimated:
    text: model_estimated
    description: Estimated by a statistical or machine-learning model.
  derived_from_floors:
    text: derived_from_floors
    description: Computed from the number of floors and an assumed floor height.
  none:
    text: none
    description: The dataset has no building heights.

```
</details>

</div>