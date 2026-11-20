---
search:
  boost: 2.0
---


# Enum: Aggregation 




_How a value relates to time._



<div data-search-exclude markdown="1">

URI: [ubem_link:Aggregation](https://w3id.org/ubem-link/Aggregation)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| static | None | Attribute that does not vary in the observation period |
| instantaneous | None | Value at a point in time (for example a temperature reading) |
| total_over_period | None | Sum over the reporting period (for example annual energy use) |
| average_over_period | None | Mean over the reporting period |
| count | None | Number of items (for example number of floors or occupants) |
| share | None | Fraction or percentage of a whole |




## Slots

| Name | Description |
| ---  | --- |
| [aggregation](aggregation.md) | How each value relates to time: static, instantaneous, total or average over ... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: Aggregation
description: How a value relates to time.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  static:
    text: static
    description: Attribute that does not vary in the observation period.
  instantaneous:
    text: instantaneous
    description: Value at a point in time (for example a temperature reading).
  total_over_period:
    text: total_over_period
    description: Sum over the reporting period (for example annual energy use).
  average_over_period:
    text: average_over_period
    description: Mean over the reporting period.
  count:
    text: count
    description: Number of items (for example number of floors or occupants).
  share:
    text: share
    description: Fraction or percentage of a whole.

```
</details>

</div>