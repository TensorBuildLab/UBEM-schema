---
search:
  boost: 2.0
---


# Enum: TimeBasis 




_Clock to which timestamps refer._



<div data-search-exclude markdown="1">

URI: [ubem_link:TimeBasis](https://w3id.org/ubem-link/TimeBasis)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| utc | None | Coordinated Universal Time |
| local_standard_time | None | Local standard time without daylight saving (as in EPW files) |
| local_time_with_dst | None | Local civil time including daylight saving |
| unknown | None | Not stated by the publisher |




## Slots

| Name | Description |
| ---  | --- |
| [time_basis](time_basis.md) | Clock to which timestamps refer (UTC, local standard time, or local time with... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: TimeBasis
description: Clock to which timestamps refer.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  utc:
    text: utc
    description: Coordinated Universal Time.
  local_standard_time:
    text: local_standard_time
    description: Local standard time without daylight saving (as in EPW files).
  local_time_with_dst:
    text: local_time_with_dst
    description: Local civil time including daylight saving.
  unknown:
    text: unknown
    description: Not stated by the publisher.

```
</details>

</div>