---
search:
  boost: 5.0
---

# Slot: exact_match 


_Term in another standard with the same meaning (SKOS exactMatch)._



<div data-search-exclude markdown="1">



URI: [skos:exactMatch](http://www.w3.org/2004/02/skos/core#exactMatch)
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
| Slot URI | [skos:exactMatch](http://www.w3.org/2004/02/skos/core#exactMatch) |
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
| self | skos:exactMatch |
| native | ubem_link:exact_match |




## LinkML Source

<details>
```yaml
name: exact_match
description: Term in another standard with the same meaning (SKOS exactMatch).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: skos:exactMatch
domain_of:
- UBEMConcept
range: string
multivalued: true

```
</details></div>