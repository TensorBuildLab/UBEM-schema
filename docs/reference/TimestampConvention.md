---
search:
  boost: 2.0
---


# Enum: TimestampConvention 




_What a timestamp marks within its interval._



<div data-search-exclude markdown="1">

URI: [ubem_link:TimestampConvention](https://w3id.org/ubem-link/TimestampConvention)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| interval_ending | None | The timestamp is the end of the interval (EPW hour 1 covers 00:00 to 01:00) |
| interval_beginning | None | The timestamp is the start of the interval |
| instantaneous | None | The value was observed at the timestamp |
| unknown | None | Not stated by the publisher |




## Slots

| Name | Description |
| ---  | --- |
| [timestamp_convention](timestamp_convention.md) | Whether a timestamp marks the end, the start or the instant of the interval i... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: TimestampConvention
description: What a timestamp marks within its interval.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  interval_ending:
    text: interval_ending
    description: The timestamp is the end of the interval (EPW hour 1 covers 00:00
      to 01:00).
  interval_beginning:
    text: interval_beginning
    description: The timestamp is the start of the interval.
  instantaneous:
    text: instantaneous
    description: The value was observed at the timestamp.
  unknown:
    text: unknown
    description: Not stated by the publisher.

```
</details>

</div>