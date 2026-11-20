---
search:
  boost: 2.0
---


# Enum: WeatherFileFormat 




_Format of released weather data._



<div data-search-exclude markdown="1">

URI: [ubem_link:WeatherFileFormat](https://w3id.org/ubem-link/WeatherFileFormat)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| epw | None | EnergyPlus weather file, readable by most simulation engines |
| tmy3_csv | None | TMY3 comma-separated format |
| netcdf | None | NetCDF gridded files |
| grib | None | GRIB gridded files |
| csv | None | Other tabular text files |
| api_json | None | Responses of a web API in JSON |
| other | None | Another format not listed here |




## Slots

| Name | Description |
| ---  | --- |
| [weather_file_format](weather_file_format.md) | Formats in which weather is released, which decide whether a simulation engin... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: WeatherFileFormat
description: Format of released weather data.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  epw:
    text: epw
    description: EnergyPlus weather file, readable by most simulation engines.
  tmy3_csv:
    text: tmy3_csv
    description: TMY3 comma-separated format.
  netcdf:
    text: netcdf
    description: NetCDF gridded files.
  grib:
    text: grib
    description: GRIB gridded files.
  csv:
    text: csv
    description: Other tabular text files.
  api_json:
    text: api_json
    description: Responses of a web API in JSON.
  other:
    text: other
    description: Another format not listed here.

```
</details>

</div>