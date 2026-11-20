---
search:
  boost: 2.0
---


# Enum: EnergyDataScale 




_Scale of energy data._



<div data-search-exclude markdown="1">

URI: [ubem_link:EnergyDataScale](https://w3id.org/ubem-link/EnergyDataScale)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| macroscopic | None | Aggregates over many buildings (national, state, utility or area totals) |
| microscopic | None | Individual buildings, meters, circuits or appliances |




## Slots

| Name | Description |
| ---  | --- |
| [energy_data_scale](energy_data_scale.md) | Macroscopic (aggregates over many buildings) or microscopic (buildings, meter... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: EnergyDataScale
description: Scale of energy data.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  macroscopic:
    text: macroscopic
    description: Aggregates over many buildings (national, state, utility or area
      totals).
  microscopic:
    text: microscopic
    description: Individual buildings, meters, circuits or appliances.

```
</details>

</div>