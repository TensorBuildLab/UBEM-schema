---
search:
  boost: 5.0
---

# Slot: reference_paper_doi 


_DOI of a peer-reviewed paper that describes the dataset._



<div data-search-exclude markdown="1">



URI: [ubem_link:reference_paper_doi](https://w3id.org/ubem-link/reference_paper_doi)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetProfile](DatasetProfile.md) | Dataset-level description of one open dataset, sufficient to decide whether a... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [DatasetProfile](DatasetProfile.md) |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^10\.\d{4,9}/\S+$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ubem_link:reference_paper_doi |
| native | ubem_link:reference_paper_doi |




## LinkML Source

<details>
```yaml
name: reference_paper_doi
description: DOI of a peer-reviewed paper that describes the dataset.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
domain_of:
- DatasetProfile
range: string
pattern: ^10\.\d{4,9}/\S+$

```
</details></div>