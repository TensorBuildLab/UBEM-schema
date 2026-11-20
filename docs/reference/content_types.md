---
search:
  boost: 5.0
---

# Slot: content_types 


_Kinds of content in the dataset (for example footprints, microdata, hourly loads)._



<div data-search-exclude markdown="1">



URI: [dcat:theme](http://www.w3.org/ns/dcat#theme)
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
| Slot URI | [dcat:theme](http://www.w3.org/ns/dcat#theme) |
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
| self | dcat:theme |
| native | ubem_link:content_types |




## LinkML Source

<details>
```yaml
name: content_types
description: Kinds of content in the dataset (for example footprints, microdata, hourly
  loads).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dcat:theme
domain_of:
- DatasetProfile
range: string
multivalued: true

```
</details></div>