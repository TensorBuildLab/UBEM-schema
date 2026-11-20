---
search:
  boost: 5.0
---

# Slot: access_url 


_URL from which a distribution can be accessed or downloaded._



<div data-search-exclude markdown="1">



URI: [dcat:accessURL](http://www.w3.org/ns/dcat#accessURL)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Distribution](Distribution.md) | One way of obtaining the data |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [Distribution](Distribution.md) |
| Slot URI | [dcat:accessURL](http://www.w3.org/ns/dcat#accessURL) |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dcat:accessURL |
| native | ubem_link:access_url |




## LinkML Source

<details>
```yaml
name: access_url
description: URL from which a distribution can be accessed or downloaded.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
slot_uri: dcat:accessURL
domain_of:
- Distribution
range: string

```
</details></div>