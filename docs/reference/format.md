---
search:
  boost: 5.0
---

# Slot: format 


_File format or media type of a distribution (for example CSV, GeoParquet, NetCDF)._



<div data-search-exclude markdown="1">



URI: [dct:format](http://purl.org/dc/terms/format)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Distribution](Distribution.md) | One way of obtaining the data |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [Distribution](Distribution.md) |
| Slot URI | [dct:format](http://purl.org/dc/terms/format) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dct:format |
| native | ubem_link:format |




## LinkML Source

<details>
```yaml
name: format
description: File format or media type of a distribution (for example CSV, GeoParquet,
  NetCDF).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dct:format
domain_of:
- Distribution
range: string

```
</details></div>