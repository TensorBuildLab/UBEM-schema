---
search:
  boost: 5.0
---

# Slot: control_actions 


_Occupant control actions recorded._



<div data-search-exclude markdown="1">



URI: [ubem_link:control_actions](https://w3id.org/ubem-link/control_actions)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [OperationProfile](OperationProfile.md) | Occupancy, occupant behavior, schedules, setpoints and time use |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [ControlAction](ControlAction.md) |
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
| self | ubem_link:control_actions |
| native | ubem_link:control_actions |




## LinkML Source

<details>
```yaml
name: control_actions
description: Occupant control actions recorded.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- OperationProfile
range: ControlAction
multivalued: true

```
</details></div>