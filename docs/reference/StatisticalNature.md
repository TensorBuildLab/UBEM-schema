---
search:
  boost: 2.0
---


# Enum: StatisticalNature 




_How the data were generated; decides the statistical treatment they need._



<div data-search-exclude markdown="1">

URI: [ubem_link:StatisticalNature](https://w3id.org/ubem-link/StatisticalNature)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| census_complete | None | Complete enumeration of a population |
| sample_survey_weighted | None | Probability sample; estimates need weights |
| administrative_record | None | Records created by an administrative process (certificates, permits, disclosu... |
| measured_monitoring | None | Sensor or meter measurements |
| remote_sensing_derived | None | Derived from satellite, aerial or lidar data with a model |
| crowdsourced | None | Volunteered geographic information |
| reanalysis_model | None | Model-data assimilation product |
| typical_year_synthetic | None | Typical meteorological year assembled from observations |
| climate_projection | None | Output of climate models under scenarios |
| simulation_synthetic | None | Output of building energy simulation |
| standard_or_code | None | A standard, dictionary, code or reference model rather than observations |
| compilation | None | Assembled from several of the above |




## Slots

| Name | Description |
| ---  | --- |
| [statistical_nature](statistical_nature.md) | How the data were generated, which decides how they may be analyzed (for exam... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: StatisticalNature
description: How the data were generated; decides the statistical treatment they need.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  census_complete:
    text: census_complete
    description: Complete enumeration of a population.
  sample_survey_weighted:
    text: sample_survey_weighted
    description: Probability sample; estimates need weights.
  administrative_record:
    text: administrative_record
    description: Records created by an administrative process (certificates, permits,
      disclosure, utility filings).
  measured_monitoring:
    text: measured_monitoring
    description: Sensor or meter measurements.
  remote_sensing_derived:
    text: remote_sensing_derived
    description: Derived from satellite, aerial or lidar data with a model.
  crowdsourced:
    text: crowdsourced
    description: Volunteered geographic information.
  reanalysis_model:
    text: reanalysis_model
    description: Model-data assimilation product.
  typical_year_synthetic:
    text: typical_year_synthetic
    description: Typical meteorological year assembled from observations.
  climate_projection:
    text: climate_projection
    description: Output of climate models under scenarios.
  simulation_synthetic:
    text: simulation_synthetic
    description: Output of building energy simulation.
  standard_or_code:
    text: standard_or_code
    description: A standard, dictionary, code or reference model rather than observations.
  compilation:
    text: compilation
    description: Assembled from several of the above.

```
</details>

</div>