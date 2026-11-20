---
search:
  boost: 5.0
---

# Slot: temporal_resolution 


_ISO 8601 duration of the finest time step, or "static" or "irregular"._



<div data-search-exclude markdown="1">



URI: [dcat:temporalResolution](http://www.w3.org/ns/dcat#temporalResolution)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetProfile](DatasetProfile.md) | Dataset-level description of one open dataset, sufficient to decide whether a... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [DatasetProfile](DatasetProfile.md) |
| Slot URI | [dcat:temporalResolution](http://www.w3.org/ns/dcat#temporalResolution) |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^(P(?!$)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(T(?=\d)(\d+H)?(\d+M)?(\d+(\.\d+)?S)?)?|static|irregular)$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dcat:temporalResolution |
| native | ubem_link:temporal_resolution |




## LinkML Source

<details>
```yaml
name: temporal_resolution
description: ISO 8601 duration of the finest time step, or "static" or "irregular".
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dcat:temporalResolution
domain_of:
- DatasetProfile
range: string
pattern: ^(P(?!$)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(T(?=\d)(\d+H)?(\d+M)?(\d+(\.\d+)?S)?)?|static|irregular)$

```
</details></div>