---
search:
  boost: 2.0
---


# Enum: MeasurementBasis 




_How energy values were obtained._



<div data-search-exclude markdown="1">

URI: [ubem_link:MeasurementBasis](https://w3id.org/ubem-link/MeasurementBasis)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| metered | None | Measured by meters at the stated resolution |
| billed | None | From utility bills or supplier records |
| self_reported | None | Reported by owners or respondents (for example through benchmarking software) |
| modeled_or_estimated | None | Estimated by models, imputation or engineering calculation |
| mixed | None | A combination of the above |




## Slots

| Name | Description |
| ---  | --- |
| [measurement_basis](measurement_basis.md) | Whether values are metered, billed, self-reported or modeled |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: MeasurementBasis
description: How energy values were obtained.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  metered:
    text: metered
    description: Measured by meters at the stated resolution.
  billed:
    text: billed
    description: From utility bills or supplier records.
  self_reported:
    text: self_reported
    description: Reported by owners or respondents (for example through benchmarking
      software).
  modeled_or_estimated:
    text: modeled_or_estimated
    description: Estimated by models, imputation or engineering calculation.
  mixed:
    text: mixed
    description: A combination of the above.

```
</details>

</div>