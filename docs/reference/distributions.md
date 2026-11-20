---
search:
  boost: 5.0
---

# Slot: distributions 


_The downloadable files or services through which the data are released._



<div data-search-exclude markdown="1">



URI: [dcat:distribution](http://www.w3.org/ns/dcat#distribution)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetProfile](DatasetProfile.md) | Dataset-level description of one open dataset, sufficient to decide whether a... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Distribution](Distribution.md) |
| Domain Of | [DatasetProfile](DatasetProfile.md) |
| Slot URI | [dcat:distribution](http://www.w3.org/ns/dcat#distribution) |
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
| self | dcat:distribution |
| native | ubem_link:distributions |




## LinkML Source

<details>
```yaml
name: distributions
description: The downloadable files or services through which the data are released.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dcat:distribution
domain_of:
- DatasetProfile
range: Distribution
multivalued: true
inlined: true
inlined_as_list: true

```
</details></div>