---
search:
  boost: 2.0
---


# Enum: VariableDatatype 




_Data type of a variable's values._



<div data-search-exclude markdown="1">

URI: [ubem_link:VariableDatatype](https://w3id.org/ubem-link/VariableDatatype)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| integer | None | Whole numbers, such as counts or years |
| float | None | Real numbers that may have decimals |
| string | None | Free text without a code list |
| categorical | None | Codes from a fixed list (see code_list) |
| boolean | None | True or false |
| datetime | None | Dates or date-times (ISO 8601) |
| geometry | None | Spatial geometries such as points, lines or polygons |
| identifier | None | Identifiers of records or entities |




## Slots

| Name | Description |
| ---  | --- |
| [datatype](datatype.md) | Data type of the variable's values |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: VariableDatatype
description: Data type of a variable's values.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  integer:
    text: integer
    description: Whole numbers, such as counts or years.
  float:
    text: float
    description: Real numbers that may have decimals.
  string:
    text: string
    description: Free text without a code list.
  categorical:
    text: categorical
    description: Codes from a fixed list (see code_list).
  boolean:
    text: boolean
    description: True or false.
  datetime:
    text: datetime
    description: Dates or date-times (ISO 8601).
  geometry:
    text: geometry
    description: Spatial geometries such as points, lines or polygons.
  identifier:
    text: identifier
    description: Identifiers of records or entities.

```
</details>

</div>