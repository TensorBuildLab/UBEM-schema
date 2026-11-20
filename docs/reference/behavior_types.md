---
search:
  boost: 5.0
---

# Slot: behavior_types 


_Kinds of occupant behavior or building operation recorded._



<div data-search-exclude markdown="1">



URI: [ubem_link:behavior_types](https://w3id.org/ubem-link/behavior_types)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [OperationProfile](OperationProfile.md) | Occupancy, occupant behavior, schedules, setpoints and time use |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [BehaviorType](BehaviorType.md) |
| Domain Of | [OperationProfile](OperationProfile.md) |
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
| self | ubem_link:behavior_types |
| native | ubem_link:behavior_types |




## LinkML Source

<details>
```yaml
name: behavior_types
description: Kinds of occupant behavior or building operation recorded.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- OperationProfile
range: BehaviorType
multivalued: true

```
</details></div>