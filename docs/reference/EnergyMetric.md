---
search:
  boost: 2.0
---


# Enum: EnergyMetric 




_Kind of energy quantity._



<div data-search-exclude markdown="1">

URI: [ubem_link:EnergyMetric](https://w3id.org/ubem-link/EnergyMetric)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| site_energy | None | Energy delivered to the site |
| source_energy | None | Site energy plus upstream generation and delivery losses |
| primary_energy | None | Primary energy as defined in national statistics |
| end_use_energy | None | Energy by end use (heating, cooling, lighting,  |
| load_profile | None | Time series of demand |
| peak_demand | None | Maximum demand over a period |
| emissions | None | Greenhouse gas emissions |
| expenditure | None | Cost of the energy used |




## Slots

| Name | Description |
| ---  | --- |
| [energy_metrics](energy_metrics.md) | Kinds of energy quantity reported |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: EnergyMetric
description: Kind of energy quantity.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  site_energy:
    text: site_energy
    description: Energy delivered to the site.
  source_energy:
    text: source_energy
    description: Site energy plus upstream generation and delivery losses.
  primary_energy:
    text: primary_energy
    description: Primary energy as defined in national statistics.
  end_use_energy:
    text: end_use_energy
    description: Energy by end use (heating, cooling, lighting, ...).
  load_profile:
    text: load_profile
    description: Time series of demand.
  peak_demand:
    text: peak_demand
    description: Maximum demand over a period.
  emissions:
    text: emissions
    description: Greenhouse gas emissions.
  expenditure:
    text: expenditure
    description: Cost of the energy used.

```
</details>

</div>