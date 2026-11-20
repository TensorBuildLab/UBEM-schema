---
search:
  boost: 5.0
---

# Slot: countries 


_ISO 3166-1 alpha-2 codes, or GLOBAL._



<div data-search-exclude markdown="1">



URI: [ubem_link:countries](https://w3id.org/ubem-link/countries)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SpatialCoverage](SpatialCoverage.md) | Geographic area a dataset covers |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [SpatialCoverage](SpatialCoverage.md) |
### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |


### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^([A-Z]{2}|GLOBAL|EU)$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:countries |
| native | ubem_link:countries |




## LinkML Source

<details>
```yaml
name: countries
description: ISO 3166-1 alpha-2 codes, or GLOBAL.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- SpatialCoverage
range: string
multivalued: true
pattern: ^([A-Z]{2}|GLOBAL|EU)$

```
</details></div>