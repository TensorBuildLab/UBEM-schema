---
search:
  boost: 5.0
---

# Slot: entity 


_What the variable or concept describes (building, household, system, meter, region, ...)._



<div data-search-exclude markdown="1">



URI: [ubem_link:entity](https://w3id.org/ubem-link/entity)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [VariableProfile](VariableProfile.md) | Variable-level (column-level) semantics |  no  |
| [UBEMConcept](UBEMConcept.md) | A concept in the UBEM-Link vocabulary: a quantity or attribute that a UBEM wo... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [EntityType](EntityType.md) |
| Domain Of | [VariableProfile](VariableProfile.md), [UBEMConcept](UBEMConcept.md) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:entity |
| native | ubem_link:entity |




## LinkML Source

<details>
```yaml
name: entity
description: What the variable or concept describes (building, household, system,
  meter, region, ...).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- VariableProfile
- UBEMConcept
range: EntityType

```
</details></div>