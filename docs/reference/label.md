---
search:
  boost: 5.0
---

# Slot: label 


_Short human-readable label of the variable as given in the codebook._



<div data-search-exclude markdown="1">



URI: [skos:prefLabel](http://www.w3.org/2004/02/skos/core#prefLabel)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [VariableProfile](VariableProfile.md) | Variable-level (column-level) semantics |  no  |
| [CodeEntry](CodeEntry.md) | One code of a categorical variable and its meaning |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [VariableProfile](VariableProfile.md), [CodeEntry](CodeEntry.md) |
| Slot URI | [skos:prefLabel](http://www.w3.org/2004/02/skos/core#prefLabel) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | skos:prefLabel |
| native | ubem_link:label |




## LinkML Source

<details>
```yaml
name: label
description: Short human-readable label of the variable as given in the codebook.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: skos:prefLabel
domain_of:
- VariableProfile
- CodeEntry
range: string

```
</details></div>