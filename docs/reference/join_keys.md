---
search:
  boost: 5.0
---

# Slot: join_keys 


_Keys present in the public data that allow records to be linked to other datasets._



<div data-search-exclude markdown="1">



URI: [ubem_link:join_keys](https://w3id.org/ubem-link/join_keys)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetProfile](DatasetProfile.md) | Dataset-level description of one open dataset, sufficient to decide whether a... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [JoinKey](JoinKey.md) |
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
| self | ubem_link:join_keys |
| native | ubem_link:join_keys |




## LinkML Source

<details>
```yaml
name: join_keys
description: Keys present in the public data that allow records to be linked to other
  datasets.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- DatasetProfile
range: JoinKey
multivalued: true

```
</details></div>