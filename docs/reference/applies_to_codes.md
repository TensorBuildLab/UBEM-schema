---
search:
  boost: 5.0
---

# Slot: applies_to_codes 


_Codes or code labels that must all occur in a variable's documented codes for the convention to apply (machine-readable scope by code list, for example Yes, No and Don't know for yes/no questions)._



<div data-search-exclude markdown="1">



URI: [ubem_link:applies_to_codes](https://w3id.org/ubem-link/applies_to_codes)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Convention](Convention.md) | A rule the publisher applies to many variables at once, such as a naming patt... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [Convention](Convention.md) |
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
| self | ubem_link:applies_to_codes |
| native | ubem_link:applies_to_codes |




## LinkML Source

<details>
```yaml
name: applies_to_codes
description: Codes or code labels that must all occur in a variable's documented codes
  for the convention to apply (machine-readable scope by code list, for example Yes,
  No and Don't know for yes/no questions).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- Convention
range: string
multivalued: true

```
</details></div>