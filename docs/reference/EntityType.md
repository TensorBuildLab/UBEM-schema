---
search:
  boost: 2.0
---


# Enum: EntityType 




_What a concept or variable describes._



<div data-search-exclude markdown="1">

URI: [ubem_link:EntityType](https://w3id.org/ubem-link/EntityType)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| site | None | A property or campus that may contain several buildings |
| building | None | A single building |
| zone | None | A thermal zone or space within a building |
| system | None | A building system or piece of equipment (HVAC, water heating, lighting,  |
| envelope | None | Walls, roofs, windows and other parts of the building envelope |
| household | None | A household occupying a housing unit |
| occupant | None | A person using a building |
| meter | None | An energy or water meter |
| region | None | A geographic area |
| weather_station | None | A weather or climate observation station |
| grid_cell | None | A cell of a raster or model grid |
| dataset_record | None | Record bookkeeping (identifiers, weights, flags) |




## Slots

| Name | Description |
| ---  | --- |
| [entity](entity.md) | What the variable or concept describes (building, household, system, meter, r... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: EntityType
description: What a concept or variable describes.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  site:
    text: site
    description: A property or campus that may contain several buildings.
  building:
    text: building
    description: A single building.
  zone:
    text: zone
    description: A thermal zone or space within a building.
  system:
    text: system
    description: A building system or piece of equipment (HVAC, water heating, lighting,
      ...).
  envelope:
    text: envelope
    description: Walls, roofs, windows and other parts of the building envelope.
  household:
    text: household
    description: A household occupying a housing unit.
  occupant:
    text: occupant
    description: A person using a building.
  meter:
    text: meter
    description: An energy or water meter.
  region:
    text: region
    description: A geographic area.
  weather_station:
    text: weather_station
    description: A weather or climate observation station.
  grid_cell:
    text: grid_cell
    description: A cell of a raster or model grid.
  dataset_record:
    text: dataset_record
    description: Record bookkeeping (identifiers, weights, flags).

```
</details>

</div>