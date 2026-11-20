---
search:
  boost: 5.0
---

# Slot: narrow_match 


_Term in another standard that is more specific (SKOS narrowMatch)._



<div data-search-exclude markdown="1">



URI: [skos:narrowMatch](http://www.w3.org/2004/02/skos/core#narrowMatch)
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
| Slot URI | [skos:narrowMatch](http://www.w3.org/2004/02/skos/core#narrowMatch) |
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
| self | skos:narrowMatch |
| native | ubem_link:narrow_match |




## LinkML Source

<details>
```yaml
name: narrow_match
description: Term in another standard that is more specific (SKOS narrowMatch).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: skos:narrowMatch
domain_of:
- UBEMConcept
range: string
multivalued: true

```
</details></div>