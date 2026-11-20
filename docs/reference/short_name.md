---
search:
  boost: 5.0
---

# Slot: short_name 


_Common short name or acronym of the dataset (for example CBECS 2018)._



<div data-search-exclude markdown="1">



URI: [skos:altLabel](http://www.w3.org/2004/02/skos/core#altLabel)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetProfile](DatasetProfile.md) | Dataset-level description of one open dataset, sufficient to decide whether a... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [DatasetProfile](DatasetProfile.md) |
| Slot URI | [skos:altLabel](http://www.w3.org/2004/02/skos/core#altLabel) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | skos:altLabel |
| native | ubem_link:short_name |




## LinkML Source

<details>
```yaml
name: short_name
description: Common short name or acronym of the dataset (for example CBECS 2018).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: skos:altLabel
domain_of:
- DatasetProfile
range: string

```
</details></div>