---
search:
  boost: 2.0
---


# Enum: CollectionMethod 




_How behavior or operation data were collected._



<div data-search-exclude markdown="1">

URI: [ubem_link:CollectionMethod](https://w3id.org/ubem-link/CollectionMethod)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| sensors_or_logs | None | Sensors, building automation logs or meters |
| connected_devices | None | Smart thermostats or other connected devices |
| survey_or_diary | None | Questionnaires or time-use diaries |
| field_study_compilation | None | Compilation of separate field studies |
| mobile_location | None | Mobile phone or other location traces |




## Slots

| Name | Description |
| ---  | --- |
| [collection_method](collection_method.md) | How the behavior or operation data were collected |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: CollectionMethod
description: How behavior or operation data were collected.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  sensors_or_logs:
    text: sensors_or_logs
    description: Sensors, building automation logs or meters.
  connected_devices:
    text: connected_devices
    description: Smart thermostats or other connected devices.
  survey_or_diary:
    text: survey_or_diary
    description: Questionnaires or time-use diaries.
  field_study_compilation:
    text: field_study_compilation
    description: Compilation of separate field studies.
  mobile_location:
    text: mobile_location
    description: Mobile phone or other location traces.

```
</details>

</div>