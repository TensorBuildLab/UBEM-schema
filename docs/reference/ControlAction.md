---
search:
  boost: 2.0
---


# Enum: ControlAction 




_Occupant control action._



<div data-search-exclude markdown="1">

URI: [ubem_link:ControlAction](https://w3id.org/ubem-link/ControlAction)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| thermostat_adjustment | None | Changing a thermostat setpoint |
| hvac_on_off | None | Switching heating, cooling or fans |
| lighting_on_off | None | Switching or dimming lights |
| window_open_close | None | Opening or closing a window |
| shading_adjustment | None | Moving blinds or shades |
| appliance_on_off | None | Switching an appliance |




## Slots

| Name | Description |
| ---  | --- |
| [control_actions](control_actions.md) | Occupant control actions recorded |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: ControlAction
description: Occupant control action.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  thermostat_adjustment:
    text: thermostat_adjustment
    description: Changing a thermostat setpoint.
  hvac_on_off:
    text: hvac_on_off
    description: Switching heating, cooling or fans.
  lighting_on_off:
    text: lighting_on_off
    description: Switching or dimming lights.
  window_open_close:
    text: window_open_close
    description: Opening or closing a window.
  shading_adjustment:
    text: shading_adjustment
    description: Moving blinds or shades.
  appliance_on_off:
    text: appliance_on_off
    description: Switching an appliance.

```
</details>

</div>