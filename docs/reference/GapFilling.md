---
search:
  boost: 2.0
---


# Enum: GapFilling 




_How missing or sub-interval values were filled._



<div data-search-exclude markdown="1">

URI: [ubem_link:GapFilling](https://w3id.org/ubem-link/GapFilling)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| none | None | Gaps are left as missing values |
| linear_interpolation | None | Gaps filled by linear interpolation in time |
| model_based | None | Gaps filled from a model, reanalysis or neighboring stations |
| unknown | None | Not stated by the publisher |




## Slots

| Name | Description |
| ---  | --- |
| [gap_filling](gap_filling.md) | How missing or sub-interval values were filled by the publisher |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: GapFilling
description: How missing or sub-interval values were filled.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  none:
    text: none
    description: Gaps are left as missing values.
  linear_interpolation:
    text: linear_interpolation
    description: Gaps filled by linear interpolation in time.
  model_based:
    text: model_based
    description: Gaps filled from a model, reanalysis or neighboring stations.
  unknown:
    text: unknown
    description: Not stated by the publisher.

```
</details>

</div>