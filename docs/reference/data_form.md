---
search:
  boost: 5.0
---

# Slot: data_form 


_Whether the data are records of individual units (microdata or building records) or published distributions (aggregate tables)._



<div data-search-exclude markdown="1">



URI: [ubem_link:data_form](https://w3id.org/ubem-link/data_form)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CharacteristicsProfile](CharacteristicsProfile.md) | Non-geometric building characteristics (use type, vintage, envelope, systems,... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DataForm](DataForm.md) |
| Domain Of | [CharacteristicsProfile](CharacteristicsProfile.md) |
### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:data_form |
| native | ubem_link:data_form |




## LinkML Source

<details>
```yaml
name: data_form
description: Whether the data are records of individual units (microdata or building
  records) or published distributions (aggregate tables).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- CharacteristicsProfile
range: DataForm
multivalued: true

```
</details></div>