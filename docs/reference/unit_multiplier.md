---
search:
  boost: 5.0
---

# Slot: unit_multiplier 


_Factor applied to raw values before the unit applies (e.g., 1000 for "thousand Btu")._



<div data-search-exclude markdown="1">



URI: [ubem_link:unit_multiplier](https://w3id.org/ubem-link/unit_multiplier)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Convention](Convention.md) | A rule the publisher applies to many variables at once, such as a naming patt... |  no  |
| [VariableProfile](VariableProfile.md) | Variable-level (column-level) semantics |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](Float.md) |
| Domain Of | [Convention](Convention.md), [VariableProfile](VariableProfile.md) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:unit_multiplier |
| native | ubem_link:unit_multiplier |




## LinkML Source

<details>
```yaml
name: unit_multiplier
description: Factor applied to raw values before the unit applies (e.g., 1000 for
  "thousand Btu").
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- Convention
- VariableProfile
range: float

```
</details></div>