---
search:
  boost: 5.0
---

# Slot: description 


_Longer description of the variable, such as the question text._



<div data-search-exclude markdown="1">



URI: [dct:description](http://purl.org/dc/terms/description)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SpatialCoverage](SpatialCoverage.md) | Geographic area a dataset covers |  no  |
| [VariableProfile](VariableProfile.md) | Variable-level (column-level) semantics |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [SpatialCoverage](SpatialCoverage.md), [VariableProfile](VariableProfile.md) |
| Slot URI | [dct:description](http://purl.org/dc/terms/description) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dct:description |
| native | ubem_link:description |




## LinkML Source

<details>
```yaml
name: description
description: Longer description of the variable, such as the question text.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dct:description
domain_of:
- SpatialCoverage
- VariableProfile
range: string

```
</details></div>