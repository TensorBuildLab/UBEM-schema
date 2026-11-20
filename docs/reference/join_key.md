---
search:
  boost: 5.0
---

# Slot: join_key 


_Key type the variable holds, if it can link records to other datasets (for example parcel_id for a tax-lot number)._



<div data-search-exclude markdown="1">



URI: [ubem_link:join_key](https://w3id.org/ubem-link/join_key)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [VariableProfile](VariableProfile.md) | Variable-level (column-level) semantics |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [JoinKey](JoinKey.md) |
| Domain Of | [VariableProfile](VariableProfile.md) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:join_key |
| native | ubem_link:join_key |




## LinkML Source

<details>
```yaml
name: join_key
description: Key type the variable holds, if it can link records to other datasets
  (for example parcel_id for a tax-lot number).
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- VariableProfile
range: JoinKey

```
</details></div>