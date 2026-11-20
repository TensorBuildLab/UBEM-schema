---
search:
  boost: 5.0
---

# Slot: coordinate_reference_system 


_Coordinate reference system of the published geometry, as an EPSG code (for example EPSG:4326)._



<div data-search-exclude markdown="1">



URI: [ubem_link:coordinate_reference_system](https://w3id.org/ubem-link/coordinate_reference_system)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GeometryProfile](GeometryProfile.md) | Building stock geometry and inventory: footprints, heights, 3D city models an... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [GeometryProfile](GeometryProfile.md) |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^EPSG:[0-9]+$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:coordinate_reference_system |
| native | ubem_link:coordinate_reference_system |




## LinkML Source

<details>
```yaml
name: coordinate_reference_system
description: Coordinate reference system of the published geometry, as an EPSG code
  (for example EPSG:4326).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- GeometryProfile
range: string
pattern: ^EPSG:[0-9]+$

```
</details></div>