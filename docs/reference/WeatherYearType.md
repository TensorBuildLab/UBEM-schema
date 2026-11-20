---
search:
  boost: 2.0
---


# Enum: WeatherYearType 




_Kind of weather year or weather series._



<div data-search-exclude markdown="1">

URI: [ubem_link:WeatherYearType](https://w3id.org/ubem-link/WeatherYearType)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| actual_series | None | Observed or reanalysis time series of actual weather over one or more years |
| actual_meteorological_year | None | Simulation-ready file of one actual year (AMY) |
| typical_meteorological_year | None | Typical year assembled from months of several years (TMY, TMYx, IWEC) |
| climate_normals | None | Long-term averages such as 30-year normals |
| future_typical_year | None | Typical year for a future period, morphed or downscaled from climate models |
| projection_series | None | Time series from climate model projections |
| design_conditions | None | Design-day statistics for sizing equipment |




## Slots

| Name | Description |
| ---  | --- |
| [weather_year_type](weather_year_type.md) | Kind of weather year or series: actual series, actual or typical meteorologic... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: WeatherYearType
description: Kind of weather year or weather series.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  actual_series:
    text: actual_series
    description: Observed or reanalysis time series of actual weather over one or
      more years.
  actual_meteorological_year:
    text: actual_meteorological_year
    description: Simulation-ready file of one actual year (AMY).
  typical_meteorological_year:
    text: typical_meteorological_year
    description: Typical year assembled from months of several years (TMY, TMYx, IWEC).
  climate_normals:
    text: climate_normals
    description: Long-term averages such as 30-year normals.
  future_typical_year:
    text: future_typical_year
    description: Typical year for a future period, morphed or downscaled from climate
      models.
  projection_series:
    text: projection_series
    description: Time series from climate model projections.
  design_conditions:
    text: design_conditions
    description: Design-day statistics for sizing equipment.

```
</details>

</div>