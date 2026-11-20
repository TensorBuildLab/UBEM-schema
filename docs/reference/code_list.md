---
search:
  boost: 5.0
---

# Slot: code_list 


_Codes of a categorical variable with their meanings._



<div data-search-exclude markdown="1">



URI: [ubem_link:code_list](https://w3id.org/ubem-link/code_list)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [VariableProfile](VariableProfile.md) | Variable-level (column-level) semantics |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [CodeEntry](CodeEntry.md) |
| Domain Of | [VariableProfile](VariableProfile.md) |
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
| self | ubem_link:code_list |
| native | ubem_link:code_list |




## LinkML Source

<details>
```yaml
name: code_list
description: Codes of a categorical variable with their meanings.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- VariableProfile
range: CodeEntry
multivalued: true
inlined: true
inlined_as_list: true

```
</details></div>