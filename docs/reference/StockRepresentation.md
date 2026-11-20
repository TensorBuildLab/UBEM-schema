---
search:
  boost: 2.0
---


# Enum: StockRepresentation 




_How a simulated building stock is represented._



<div data-search-exclude markdown="1">

URI: [ubem_link:StockRepresentation](https://w3id.org/ubem-link/StockRepresentation)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| sampled_models | None | A statistical sample of building models weighted to the stock |
| building_by_building | None | One model per real building |
| prototype_library | None | Typical or prototype buildings by type, vintage and climate |




## Slots

| Name | Description |
| ---  | --- |
| [stock_representation](stock_representation.md) | How the simulated building stock is represented |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: StockRepresentation
description: How a simulated building stock is represented.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  sampled_models:
    text: sampled_models
    description: A statistical sample of building models weighted to the stock.
  building_by_building:
    text: building_by_building
    description: One model per real building.
  prototype_library:
    text: prototype_library
    description: Typical or prototype buildings by type, vintage and climate.

```
</details>

</div>