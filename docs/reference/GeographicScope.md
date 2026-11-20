---
search:
  boost: 2.0
---


# Enum: GeographicScope 




_Extent of the area a dataset covers._



<div data-search-exclude markdown="1">

URI: [ubem_link:GeographicScope](https://w3id.org/ubem-link/GeographicScope)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| global | None | Covers (nearly) the whole world |
| multinational | None | Covers several countries, such as the European Union |
| national | None | Covers one country |
| subnational | None | Covers part of a country, such as a state, province or utility territory |
| city | None | Covers one city or metropolitan area |




## Slots

| Name | Description |
| ---  | --- |
| [geographic_scope](geographic_scope.md) | Extent of the area covered, from city to global |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: GeographicScope
description: Extent of the area a dataset covers.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  global:
    text: global
    description: Covers (nearly) the whole world.
  multinational:
    text: multinational
    description: Covers several countries, such as the European Union.
  national:
    text: national
    description: Covers one country.
  subnational:
    text: subnational
    description: Covers part of a country, such as a state, province or utility territory.
  city:
    text: city
    description: Covers one city or metropolitan area.

```
</details>

</div>