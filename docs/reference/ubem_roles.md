---
search:
  boost: 5.0
---

# Slot: ubem_roles 


_UBEM workflow steps the dataset feeds; first value is the primary role._



<div data-search-exclude markdown="1">



URI: [ubem_link:ubem_roles](https://w3id.org/ubem-link/ubem_roles)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetProfile](DatasetProfile.md) | Dataset-level description of one open dataset, sufficient to decide whether a... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [UBEMRole](UBEMRole.md) |
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
| self | ubem_link:ubem_roles |
| native | ubem_link:ubem_roles |




## LinkML Source

<details>
```yaml
name: ubem_roles
description: UBEM workflow steps the dataset feeds; first value is the primary role.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- DatasetProfile
range: UBEMRole
multivalued: true

```
</details></div>