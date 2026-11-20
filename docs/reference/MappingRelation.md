---
search:
  boost: 2.0
---


# Enum: MappingRelation 




_SKOS mapping relation between a variable and a concept._



<div data-search-exclude markdown="1">

URI: [ubem_link:MappingRelation](https://w3id.org/ubem-link/MappingRelation)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| exactMatch | skos:exactMatch | The variable measures exactly the concept |
| closeMatch | skos:closeMatch | The variable measures nearly the concept and can be used in its place in most... |
| broadMatch | skos:broadMatch | The concept is more general than the variable |
| narrowMatch | skos:narrowMatch | The concept is more specific than the variable |
| relatedMatch | skos:relatedMatch | The variable is associated with the concept but does not measure it |




## Slots

| Name | Description |
| ---  | --- |
| [mapping_relation](mapping_relation.md) | SKOS relation between the variable and its concept (exact, close, broad, narr... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/ubem-link/schema






## LinkML Source

<details>
```yaml
name: MappingRelation
description: SKOS mapping relation between a variable and a concept.
from_schema: https://w3id.org/ubem-link/schema
rank: 1000
permissible_values:
  exactMatch:
    text: exactMatch
    description: The variable measures exactly the concept.
    meaning: skos:exactMatch
  closeMatch:
    text: closeMatch
    description: The variable measures nearly the concept and can be used in its place
      in most applications.
    meaning: skos:closeMatch
  broadMatch:
    text: broadMatch
    description: The concept is more general than the variable.
    meaning: skos:broadMatch
  narrowMatch:
    text: narrowMatch
    description: The concept is more specific than the variable.
    meaning: skos:narrowMatch
  relatedMatch:
    text: relatedMatch
    description: The variable is associated with the concept but does not measure
      it.
    meaning: skos:relatedMatch

```
</details>

</div>