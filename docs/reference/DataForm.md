---
search:
  boost: 2.0
---


# Enum: DataForm 




_Form in which characteristics are released._



<div data-search-exclude markdown="1">

URI: [ubem_link:DataForm](https://w3id.org/ubem-link/DataForm)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| microdata | None | One record per sampled unit (building or household), usually with weights |
| building_records | None | One record per identified real building or property (certificates, benchmarki... |
| aggregate_tables | None | Published distributions or totals, not records of units |
| dictionary_or_standard | None | A data dictionary, standard or exchange schema, not data |
| archetype_library | None | Typical buildings or model templates by type and vintage |




## Slots

| Name | Description |
| ---  | --- |
| [data_form](data_form.md) | Whether the data are records of individual units (microdata or building recor... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: DataForm
description: Form in which characteristics are released.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  microdata:
    text: microdata
    description: One record per sampled unit (building or household), usually with
      weights.
  building_records:
    text: building_records
    description: One record per identified real building or property (certificates,
      benchmarking, permits).
  aggregate_tables:
    text: aggregate_tables
    description: Published distributions or totals, not records of units.
  dictionary_or_standard:
    text: dictionary_or_standard
    description: A data dictionary, standard or exchange schema, not data.
  archetype_library:
    text: archetype_library
    description: Typical buildings or model templates by type and vintage.

```
</details>

</div>