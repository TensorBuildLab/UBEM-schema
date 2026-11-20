---
search:
  boost: 5.0
---

# Slot: spatial_coverage 


_Area the dataset covers, as countries and optional regions._



<div data-search-exclude markdown="1">



URI: [dct:spatial](http://purl.org/dc/terms/spatial)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetProfile](DatasetProfile.md) | Dataset-level description of one open dataset, sufficient to decide whether a... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [SpatialCoverage](SpatialCoverage.md) |
| Domain Of | [DatasetProfile](DatasetProfile.md) |
| Slot URI | [dct:spatial](http://purl.org/dc/terms/spatial) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dct:spatial |
| native | ubem_link:spatial_coverage |




## LinkML Source

<details>
```yaml
name: spatial_coverage
description: Area the dataset covers, as countries and optional regions.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dct:spatial
domain_of:
- DatasetProfile
range: SpatialCoverage
inlined: true

```
</details></div>