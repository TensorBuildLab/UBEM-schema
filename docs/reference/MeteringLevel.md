---
search:
  boost: 2.0
---


# Enum: MeteringLevel 




_Finest level at which energy is measured or reported._



<div data-search-exclude markdown="1">

URI: [ubem_link:MeteringLevel](https://w3id.org/ubem-link/MeteringLevel)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| area_aggregate | None | Totals over an area or sector |
| utility_territory | None | Totals over a utility service territory or balancing authority |
| whole_building | None | One value per building or property |
| submeter_end_use | None | Submeters or end uses within a building |
| circuit_or_appliance | None | Circuits or individual appliances |




## Slots

| Name | Description |
| ---  | --- |
| [metering_level](metering_level.md) | Finest level at which energy is measured or reported |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: MeteringLevel
description: Finest level at which energy is measured or reported.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  area_aggregate:
    text: area_aggregate
    description: Totals over an area or sector.
  utility_territory:
    text: utility_territory
    description: Totals over a utility service territory or balancing authority.
  whole_building:
    text: whole_building
    description: One value per building or property.
  submeter_end_use:
    text: submeter_end_use
    description: Submeters or end uses within a building.
  circuit_or_appliance:
    text: circuit_or_appliance
    description: Circuits or individual appliances.

```
</details>

</div>