---
search:
  boost: 5.0
---

# Slot: energy_carriers 


_Energy carriers reported._



<div data-search-exclude markdown="1">



URI: [ubem_link:energy_carriers](https://w3id.org/ubem-link/energy_carriers)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [EnergyProfile](EnergyProfile.md) | Measured or reported energy use for calibration and validation, from national... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [EnergyCarrier](EnergyCarrier.md) |
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
| self | ubem_link:energy_carriers |
| native | ubem_link:energy_carriers |




## LinkML Source

<details>
```yaml
name: energy_carriers
description: Energy carriers reported.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- EnergyProfile
range: EnergyCarrier
multivalued: true

```
</details></div>