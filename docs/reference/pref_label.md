---
search:
  boost: 5.0
---

# Slot: pref_label 


_Preferred human-readable label of the concept._



<div data-search-exclude markdown="1">



URI: [skos:prefLabel](http://www.w3.org/2004/02/skos/core#prefLabel)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [UBEMConcept](UBEMConcept.md) | A concept in the UBEM-Link vocabulary: a quantity or attribute that a UBEM wo... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [UBEMConcept](UBEMConcept.md) |
| Slot URI | [skos:prefLabel](http://www.w3.org/2004/02/skos/core#prefLabel) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | skos:prefLabel |
| native | ubem_link:pref_label |




## LinkML Source

<details>
```yaml
name: pref_label
description: Preferred human-readable label of the concept.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: skos:prefLabel
domain_of:
- UBEMConcept
range: string

```
</details></div>