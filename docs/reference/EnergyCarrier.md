---
search:
  boost: 2.0
---


# Enum: EnergyCarrier 




_Energy carrier._



<div data-search-exclude markdown="1">

URI: [ubem_link:EnergyCarrier](https://w3id.org/ubem-link/EnergyCarrier)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| electricity | None | Electricity from the grid |
| natural_gas | None | Natural gas from a pipeline network |
| fuel_oil | None | Fuel oil and other petroleum liquids |
| propane | None | Propane and liquefied petroleum gas |
| district_energy | None | District steam, hot water or chilled water |
| biomass | None | Wood and other biomass |
| onsite_renewables | None | Energy generated on site, such as rooftop solar |
| all_carriers | None | Totals over all carriers only |




## Slots

| Name | Description |
| ---  | --- |
| [energy_carriers](energy_carriers.md) | Energy carriers reported |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: EnergyCarrier
description: Energy carrier.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  electricity:
    text: electricity
    description: Electricity from the grid.
  natural_gas:
    text: natural_gas
    description: Natural gas from a pipeline network.
  fuel_oil:
    text: fuel_oil
    description: Fuel oil and other petroleum liquids.
  propane:
    text: propane
    description: Propane and liquefied petroleum gas.
  district_energy:
    text: district_energy
    description: District steam, hot water or chilled water.
  biomass:
    text: biomass
    description: Wood and other biomass.
  onsite_renewables:
    text: onsite_renewables
    description: Energy generated on site, such as rooftop solar.
  all_carriers:
    text: all_carriers
    description: Totals over all carriers only.

```
</details>

</div>