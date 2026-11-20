---
search:
  boost: 5.0
---

# Slot: temporal_coverage 


_Period the data describe._



<div data-search-exclude markdown="1">



URI: [dct:temporal](http://purl.org/dc/terms/temporal)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetProfile](DatasetProfile.md) | Dataset-level description of one open dataset, sufficient to decide whether a... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [TemporalCoverage](TemporalCoverage.md) |
| Domain Of | [DatasetProfile](DatasetProfile.md) |
| Slot URI | [dct:temporal](http://purl.org/dc/terms/temporal) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dct:temporal |
| native | ubem_link:temporal_coverage |




## LinkML Source

<details>
```yaml
name: temporal_coverage
description: Period the data describe.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dct:temporal
domain_of:
- DatasetProfile
range: TemporalCoverage
inlined: true

```
</details></div>