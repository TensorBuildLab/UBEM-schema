---
search:
  boost: 2.0
---


# Enum: BehaviorType 




_Kind of occupant behavior or building operation._



<div data-search-exclude markdown="1">

URI: [ubem_link:BehaviorType](https://w3id.org/ubem-link/BehaviorType)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| occupancy_presence | None | Whether or how many people are present |
| hvac_operation | None | Operation of heating, cooling or ventilation |
| thermostat_setpoint | None | Setpoints and their changes |
| window_operation | None | Opening and closing windows |
| lighting_operation | None | Switching or dimming lights |
| appliance_plug_loads | None | Use of appliances and plug loads |
| hot_water_use | None | Domestic hot water draws |
| thermal_comfort | None | Thermal sensation, preference or acceptability votes |
| time_use_activities | None | Activities of people over the day (time-use diaries) |
| mobility | None | Travel and location over the day |




## Slots

| Name | Description |
| ---  | --- |
| [behavior_types](behavior_types.md) | Kinds of occupant behavior or building operation recorded |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: BehaviorType
description: Kind of occupant behavior or building operation.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  occupancy_presence:
    text: occupancy_presence
    description: Whether or how many people are present.
  hvac_operation:
    text: hvac_operation
    description: Operation of heating, cooling or ventilation.
  thermostat_setpoint:
    text: thermostat_setpoint
    description: Setpoints and their changes.
  window_operation:
    text: window_operation
    description: Opening and closing windows.
  lighting_operation:
    text: lighting_operation
    description: Switching or dimming lights.
  appliance_plug_loads:
    text: appliance_plug_loads
    description: Use of appliances and plug loads.
  hot_water_use:
    text: hot_water_use
    description: Domestic hot water draws.
  thermal_comfort:
    text: thermal_comfort
    description: Thermal sensation, preference or acceptability votes.
  time_use_activities:
    text: time_use_activities
    description: Activities of people over the day (time-use diaries).
  mobility:
    text: mobility
    description: Travel and location over the day.

```
</details>

</div>