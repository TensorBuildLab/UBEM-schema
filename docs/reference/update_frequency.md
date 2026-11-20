---
search:
  boost: 5.0
---

# Slot: update_frequency 


_How often the publisher releases new data (for example annual, irregular)._



<div data-search-exclude markdown="1">



URI: [dct:accrualPeriodicity](http://purl.org/dc/terms/accrualPeriodicity)
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
| Slot URI | [dct:accrualPeriodicity](http://purl.org/dc/terms/accrualPeriodicity) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dct:accrualPeriodicity |
| native | ubem_link:update_frequency |




## LinkML Source

<details>
```yaml
name: update_frequency
description: How often the publisher releases new data (for example annual, irregular).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dct:accrualPeriodicity
domain_of:
- DatasetProfile
range: string

```
</details></div>