---
search:
  boost: 5.0
---

# Slot: related_match 


_Term in another standard that is associated but not equivalent (SKOS relatedMatch)._



<div data-search-exclude markdown="1">



URI: [skos:relatedMatch](http://www.w3.org/2004/02/skos/core#relatedMatch)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [UBEMConcept](UBEMConcept.md) | A concept in the UBEM-Link vocabulary: a quantity or attribute that a UBEM wo... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [UBEMConcept](UBEMConcept.md) |
| Slot URI | [skos:relatedMatch](http://www.w3.org/2004/02/skos/core#relatedMatch) |
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
| self | skos:relatedMatch |
| native | ubem_link:related_match |




## LinkML Source

<details>
```yaml
name: related_match
description: Term in another standard that is associated but not equivalent (SKOS
  relatedMatch).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: skos:relatedMatch
domain_of:
- UBEMConcept
range: string
multivalued: true

```
</details></div>