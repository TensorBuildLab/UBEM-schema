---
search:
  boost: 5.0
---

# Slot: start 


_First period covered (ISO 8601 year, month or date)._



<div data-search-exclude markdown="1">



URI: [dcat:startDate](http://www.w3.org/ns/dcat#startDate)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TemporalCoverage](TemporalCoverage.md) | Period of time a dataset covers |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [TemporalCoverage](TemporalCoverage.md) |
| Slot URI | [dcat:startDate](http://www.w3.org/ns/dcat#startDate) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dcat:startDate |
| native | ubem_link:start |




## LinkML Source

<details>
```yaml
name: start
description: First period covered (ISO 8601 year, month or date).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dcat:startDate
domain_of:
- TemporalCoverage
range: string

```
</details></div>