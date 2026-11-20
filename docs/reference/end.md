---
search:
  boost: 5.0
---

# Slot: end 


_Last period covered (ISO 8601), or 'present' for an ongoing series._



<div data-search-exclude markdown="1">



URI: [dcat:endDate](http://www.w3.org/ns/dcat#endDate)
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
| Slot URI | [dcat:endDate](http://www.w3.org/ns/dcat#endDate) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dcat:endDate |
| native | ubem_link:end |




## LinkML Source

<details>
```yaml
name: end
description: Last period covered (ISO 8601), or 'present' for an ongoing series.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dcat:endDate
domain_of:
- TemporalCoverage
range: string

```
</details></div>