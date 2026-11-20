---
search:
  boost: 2.0
---


# Enum: GeometryDimension 




_Geometric representation of buildings._



<div data-search-exclude markdown="1">

URI: [ubem_link:GeometryDimension](https://w3id.org/ubem-link/GeometryDimension)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| point | None | Building locations as points only |
| footprint_2d | None | Building outlines without height |
| footprint_with_height | None | Building outlines with a height attribute (2 |
| solid_3d | None | Three-dimensional building solids or surfaces (CityGML LoD1 or higher) |
| raster | None | Gridded built-up surface, volume or height |
| parcel_polygon | None | Parcel or lot outlines, not buildings |




## Slots

| Name | Description |
| ---  | --- |
| [geometry_dimension](geometry_dimension.md) | Geometric representation of buildings, from points and footprints to 3D solid... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: GeometryDimension
description: Geometric representation of buildings.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  point:
    text: point
    description: Building locations as points only.
  footprint_2d:
    text: footprint_2d
    description: Building outlines without height.
  footprint_with_height:
    text: footprint_with_height
    description: Building outlines with a height attribute (2.5D, extrudable to CityGML
      LoD1).
  solid_3d:
    text: solid_3d
    description: Three-dimensional building solids or surfaces (CityGML LoD1 or higher).
  raster:
    text: raster
    description: Gridded built-up surface, volume or height.
  parcel_polygon:
    text: parcel_polygon
    description: Parcel or lot outlines, not buildings.

```
</details>

</div>