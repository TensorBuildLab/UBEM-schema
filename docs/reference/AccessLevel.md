---
search:
  boost: 2.0
---


# Enum: AccessLevel 




_How the data can be obtained._



<div data-search-exclude markdown="1">

URI: [ubem_link:AccessLevel](https://w3id.org/ubem-link/AccessLevel)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| open_download | None | Files can be downloaded by anyone without registration |
| open_api | None | Data can be retrieved by anyone through an open programmatic interface |
| registration_required | None | Free, but users must register or sign in |
| request_or_agreement | None | Access requires an application, a data-use agreement or approval |
| restricted_commercial | None | Access requires payment or is restricted to specific users |




## Slots

| Name | Description |
| ---  | --- |
| [access_level](access_level.md) | How the data can be obtained, from open download to restricted or commercial ... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: AccessLevel
description: How the data can be obtained.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  open_download:
    text: open_download
    description: Files can be downloaded by anyone without registration.
  open_api:
    text: open_api
    description: Data can be retrieved by anyone through an open programmatic interface.
  registration_required:
    text: registration_required
    description: Free, but users must register or sign in.
  request_or_agreement:
    text: request_or_agreement
    description: Access requires an application, a data-use agreement or approval.
  restricted_commercial:
    text: restricted_commercial
    description: Access requires payment or is restricted to specific users.

```
</details>

</div>