---
search:
  boost: 5.0
---

# Slot: id 


_Stable lowercase identifier of the record (letters, digits, '_', '.', '-')._



<div data-search-exclude markdown="1">



URI: [ubem_link:id](https://w3id.org/ubem-link/id)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetProfile](DatasetProfile.md) | Dataset-level description of one open dataset, sufficient to decide whether a... |  yes  |
| [UBEMConcept](UBEMConcept.md) | A concept in the UBEM-Link vocabulary: a quantity or attribute that a UBEM wo... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [DatasetProfile](DatasetProfile.md), [UBEMConcept](UBEMConcept.md) |
### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |


### Slot Characteristics

| Property | Value |
| --- | --- |
| Identifier | Yes |


### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^[a-z0-9][a-z0-9_.-]*$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:id |
| native | ubem_link:id |




## LinkML Source

<details>
```yaml
name: id
description: Stable lowercase identifier of the record (letters, digits, '_', '.',
  '-').
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
identifier: true
domain_of:
- DatasetProfile
- UBEMConcept
range: string
required: true
pattern: ^[a-z0-9][a-z0-9_.-]*$

```
</details></div>