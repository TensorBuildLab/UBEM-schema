---
search:
  boost: 5.0
---

# Slot: datasets 


_Dataset profiles held in the catalog._



<div data-search-exclude markdown="1">



URI: [ubem_link:datasets](https://w3id.org/ubem-link/datasets)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Catalog](Catalog.md) | A collection of dataset profiles and the concept vocabulary they refer to |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DatasetProfile](DatasetProfile.md) |
| Domain Of | [Catalog](Catalog.md) |
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
| self | ubem_link:datasets |
| native | ubem_link:datasets |




## LinkML Source

<details>
```yaml
name: datasets
description: Dataset profiles held in the catalog.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- Catalog
range: DatasetProfile
multivalued: true
inlined: true
inlined_as_list: true

```
</details></div>