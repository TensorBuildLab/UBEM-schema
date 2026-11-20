---
search:
  boost: 2.0
---


# Enum: ConventionType 




_What a dataset convention concerns._



<div data-search-exclude markdown="1">

URI: [ubem_link:ConventionType](https://w3id.org/ubem-link/ConventionType)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| missing_code | None | Codes that mean missing, not applicable, withheld or unknown |
| unit | None | The unit and multiplier of values |
| top_or_bottom_code | None | Codes that stand for ranges at the end of a scale |
| imputation_flag | None | How imputation flags are named and linked to their variables |
| weight | None | How weights are named and used |
| identifier_format | None | How identifiers and keys are written |
| do_not_use | None | A field the publisher says must not be used, or not for some purpose |
| definition | None | What a field includes or excludes |




## Slots

| Name | Description |
| ---  | --- |
| [convention_type](convention_type.md) | What the convention concerns, so that tools can apply it (missing codes, unit... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: ConventionType
description: What a dataset convention concerns.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  missing_code:
    text: missing_code
    description: Codes that mean missing, not applicable, withheld or unknown.
  unit:
    text: unit
    description: The unit and multiplier of values.
  top_or_bottom_code:
    text: top_or_bottom_code
    description: Codes that stand for ranges at the end of a scale.
  imputation_flag:
    text: imputation_flag
    description: How imputation flags are named and linked to their variables.
  weight:
    text: weight
    description: How weights are named and used.
  identifier_format:
    text: identifier_format
    description: How identifiers and keys are written.
  do_not_use:
    text: do_not_use
    description: A field the publisher says must not be used, or not for some purpose.
  definition:
    text: definition
    description: What a field includes or excludes.

```
</details>

</div>