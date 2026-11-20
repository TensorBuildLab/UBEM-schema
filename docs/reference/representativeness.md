---
search:
  boost: 2.0
---


# Enum: Representativeness 




_How the covered buildings relate to the building stock._



<div data-search-exclude markdown="1">

URI: [ubem_link:Representativeness](https://w3id.org/ubem-link/Representativeness)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| probability_sample | None | A probability sample; weighted estimates represent the stock |
| complete_population | None | All buildings of the area |
| mandated_subset | None | Buildings covered by a mandate (for example above a size threshold) |
| voluntary_or_convenience | None | Buildings that chose to participate or were available |
| synthetic | None | Modeled or typical buildings, not real ones |
| unknown | None | Not stated by the publisher |




## Slots

| Name | Description |
| ---  | --- |
| [representativeness](representativeness.md) | How the covered buildings relate to the building stock, which decides whether... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: Representativeness
description: How the covered buildings relate to the building stock.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  probability_sample:
    text: probability_sample
    description: A probability sample; weighted estimates represent the stock.
  complete_population:
    text: complete_population
    description: All buildings of the area.
  mandated_subset:
    text: mandated_subset
    description: Buildings covered by a mandate (for example above a size threshold).
  voluntary_or_convenience:
    text: voluntary_or_convenience
    description: Buildings that chose to participate or were available.
  synthetic:
    text: synthetic
    description: Modeled or typical buildings, not real ones.
  unknown:
    text: unknown
    description: Not stated by the publisher.

```
</details>

</div>