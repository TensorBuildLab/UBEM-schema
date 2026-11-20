---
search:
  boost: 5.0
---

# Slot: building_id_scheme 


_Building identifier system used (for example BIN, UPRN, BAG, UBID); null if none._



<div data-search-exclude markdown="1">



URI: [ubem_link:building_id_scheme](https://w3id.org/ubem-link/building_id_scheme)
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










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:building_id_scheme |
| native | ubem_link:building_id_scheme |




## LinkML Source

<details>
```yaml
name: building_id_scheme
description: Building identifier system used (for example BIN, UPRN, BAG, UBID); null
  if none.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- GeometryProfile
range: string

```
</details></div>