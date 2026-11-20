---
search:
  boost: 5.0
---

# Slot: variables 


_Variable-level profiles of the dataset's columns._



<div data-search-exclude markdown="1">



URI: [ubem_link:variables](https://w3id.org/ubem-link/variables)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetProfile](DatasetProfile.md) | Dataset-level description of one open dataset, sufficient to decide whether a... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [VariableProfile](VariableProfile.md) |
| Domain Of | [DatasetProfile](DatasetProfile.md) |
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
| self | ubem_link:variables |
| native | ubem_link:variables |




## LinkML Source

<details>
```yaml
name: variables
description: Variable-level profiles of the dataset's columns.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- DatasetProfile
range: VariableProfile
multivalued: true
inlined: true
inlined_as_list: true

```
</details></div>