---
search:
  boost: 5.0
---

# Slot: bbox 


_WGS84 bounding box "minLon,minLat,maxLon,maxLat" when meaningful._



<div data-search-exclude markdown="1">



URI: [dcat:bbox](http://www.w3.org/ns/dcat#bbox)
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
| Slot URI | [dcat:bbox](http://www.w3.org/ns/dcat#bbox) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dcat:bbox |
| native | ubem_link:bbox |




## LinkML Source

<details>
```yaml
name: bbox
description: WGS84 bounding box "minLon,minLat,maxLon,maxLat" when meaningful.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dcat:bbox
domain_of:
- SpatialCoverage
range: string

```
</details></div>