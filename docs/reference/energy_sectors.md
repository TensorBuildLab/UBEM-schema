---
search:
  boost: 5.0
---

# Slot: energy_sectors 


_Energy-using sectors covered._



<div data-search-exclude markdown="1">



URI: [ubem_link:energy_sectors](https://w3id.org/ubem-link/energy_sectors)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [EnergyProfile](EnergyProfile.md) | Measured or reported energy use for calibration and validation, from national... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [EnergySector](EnergySector.md) |
| Domain Of | [EnergyProfile](EnergyProfile.md) |
### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:energy_sectors |
| native | ubem_link:energy_sectors |




## LinkML Source

<details>
```yaml
name: energy_sectors
description: Energy-using sectors covered.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- EnergyProfile
range: EnergySector
multivalued: true

```
</details></div>