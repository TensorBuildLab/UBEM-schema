# Auto generated from meta_urban.yaml by pythongen.py version: 0.0.1
# Schema: meta_urban
#
# id: https://w3id.org/meta-urban/schema
# description: Meta-Urban describes open datasets used in urban building energy modeling (UBEM) at two levels. The dataset level (DatasetProfile) is an application profile of W3C DCAT 3 with UBEM-specific facets: the UBEM workflow role, statistical nature, spatial granularity, temporal resolution, access level and join keys. The variable level (VariableProfile) records what each column means for UBEM: the concept it maps to in the Meta-Urban vocabulary, its unit (QUDT), its code list, its aggregation semantics, and whether it is a survey weight or an imputation flag. Concepts (UBEMConcept) form a SKOS hierarchy and carry mappings to BEDES, Brick, CityGML Energy ADE and EnergyPlus input objects.
# license: CC-BY-4.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Float, Integer, String, Uri
from linkml_runtime.utils.metamodelcore import Bool, URI

metamodel_version = "1.12.0"
version = "2.0.0"

# Namespaces
BEDES = CurieNamespace('bedes', 'https://bedes.lbl.gov/node/')
BRICK = CurieNamespace('brick', 'https://brickschema.org/schema/Brick#')
CSVW = CurieNamespace('csvw', 'http://www.w3.org/ns/csvw#')
DCAT = CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#')
DCT = CurieNamespace('dct', 'http://purl.org/dc/terms/')
ENERGY = CurieNamespace('energy', 'http://www.sig3d.org/citygml/2.0/energy/1.0#')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
META_URBAN = CurieNamespace('meta_urban', 'https://w3id.org/meta-urban/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
QUANTITYKIND = CurieNamespace('quantitykind', 'http://qudt.org/vocab/quantitykind/')
QUDT = CurieNamespace('qudt', 'http://qudt.org/schema/qudt/')
REC = CurieNamespace('rec', 'https://w3id.org/rec#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
UNIT = CurieNamespace('unit', 'http://qudt.org/vocab/unit/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = META_URBAN


# Types

# Class references
class DatasetProfileId(extended_str):
    pass


class UBEMConceptId(extended_str):
    pass


@dataclass(repr=False)
class Catalog(YAMLRoot):
    """
    A collection of dataset profiles and the concept vocabulary they refer to.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Catalog"]
    class_class_curie: ClassVar[str] = "dcat:Catalog"
    class_name: ClassVar[str] = "Catalog"
    class_model_uri: ClassVar[URIRef] = META_URBAN.Catalog

    datasets: Optional[Union[dict[Union[str, DatasetProfileId], Union[dict, "DatasetProfile"]], list[Union[dict, "DatasetProfile"]]]] = empty_dict()
    concepts: Optional[Union[dict[Union[str, UBEMConceptId], Union[dict, "UBEMConcept"]], list[Union[dict, "UBEMConcept"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="datasets", slot_type=DatasetProfile, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="concepts", slot_type=UBEMConcept, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DatasetProfile(YAMLRoot):
    """
    Dataset-level description of one open dataset, sufficient to decide whether and how it can feed a UBEM workflow,
    and to join it with other datasets.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Dataset"]
    class_class_curie: ClassVar[str] = "dcat:Dataset"
    class_name: ClassVar[str] = "DatasetProfile"
    class_model_uri: ClassVar[URIRef] = META_URBAN.DatasetProfile

    id: Union[str, DatasetProfileId] = None
    title: str = None
    access_level: Union[str, "AccessLevel"] = None
    ubem_roles: Union[Union[str, "UBEMRole"], list[Union[str, "UBEMRole"]]] = None
    spatial_granularity: Union[str, "SpatialGranularity"] = None
    statistical_nature: Union[str, "StatisticalNature"] = None
    short_name: Optional[str] = None
    publisher: Optional[str] = None
    landing_page: Optional[Union[str, URI]] = None
    doi: Optional[str] = None
    citation: Optional[str] = None
    reference_paper_doi: Optional[str] = None
    license: Optional[str] = None
    distributions: Optional[Union[Union[dict, "Distribution"], list[Union[dict, "Distribution"]]]] = empty_list()
    content_types: Optional[Union[str, list[str]]] = empty_list()
    geographic_scope: Optional[Union[str, "GeographicScope"]] = None
    spatial_coverage: Optional[Union[dict, "SpatialCoverage"]] = None
    unit_of_observation: Optional[str] = None
    temporal_coverage: Optional[Union[dict, "TemporalCoverage"]] = None
    temporal_resolution: Optional[str] = None
    update_frequency: Optional[str] = None
    sampling_weights: Optional[str] = None
    record_count: Optional[int] = None
    record_count_note: Optional[str] = None
    join_keys: Optional[Union[Union[str, "JoinKey"], list[Union[str, "JoinKey"]]]] = empty_list()
    variables_documented: Optional[Union[bool, Bool]] = None
    machine_readable: Optional[Union[bool, Bool]] = None
    versioned: Optional[Union[bool, Bool]] = None
    persistent_identifier: Optional[Union[bool, Bool]] = None
    known_limitations: Optional[str] = None
    notes: Optional[str] = None
    verified: Optional[Union[dict, "Verification"]] = None
    variables: Optional[Union[Union[dict, "VariableProfile"], list[Union[dict, "VariableProfile"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DatasetProfileId):
            self.id = DatasetProfileId(self.id)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self._is_empty(self.access_level):
            self.MissingRequiredField("access_level")
        if not isinstance(self.access_level, AccessLevel):
            self.access_level = AccessLevel(self.access_level)

        if self._is_empty(self.ubem_roles):
            self.MissingRequiredField("ubem_roles")
        if not isinstance(self.ubem_roles, list):
            self.ubem_roles = [self.ubem_roles] if self.ubem_roles is not None else []
        self.ubem_roles = [v if isinstance(v, UBEMRole) else UBEMRole(v) for v in self.ubem_roles]

        if self._is_empty(self.spatial_granularity):
            self.MissingRequiredField("spatial_granularity")
        if not isinstance(self.spatial_granularity, SpatialGranularity):
            self.spatial_granularity = SpatialGranularity(self.spatial_granularity)

        if self._is_empty(self.statistical_nature):
            self.MissingRequiredField("statistical_nature")
        if not isinstance(self.statistical_nature, StatisticalNature):
            self.statistical_nature = StatisticalNature(self.statistical_nature)

        if self.short_name is not None and not isinstance(self.short_name, str):
            self.short_name = str(self.short_name)

        if self.publisher is not None and not isinstance(self.publisher, str):
            self.publisher = str(self.publisher)

        if self.landing_page is not None and not isinstance(self.landing_page, URI):
            self.landing_page = URI(self.landing_page)

        if self.doi is not None and not isinstance(self.doi, str):
            self.doi = str(self.doi)

        if self.citation is not None and not isinstance(self.citation, str):
            self.citation = str(self.citation)

        if self.reference_paper_doi is not None and not isinstance(self.reference_paper_doi, str):
            self.reference_paper_doi = str(self.reference_paper_doi)

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if not isinstance(self.distributions, list):
            self.distributions = [self.distributions] if self.distributions is not None else []
        self.distributions = [v if isinstance(v, Distribution) else Distribution(**as_dict(v)) for v in self.distributions]

        if not isinstance(self.content_types, list):
            self.content_types = [self.content_types] if self.content_types is not None else []
        self.content_types = [v if isinstance(v, str) else str(v) for v in self.content_types]

        if self.geographic_scope is not None and not isinstance(self.geographic_scope, GeographicScope):
            self.geographic_scope = GeographicScope(self.geographic_scope)

        if self.spatial_coverage is not None and not isinstance(self.spatial_coverage, SpatialCoverage):
            self.spatial_coverage = SpatialCoverage(**as_dict(self.spatial_coverage))

        if self.unit_of_observation is not None and not isinstance(self.unit_of_observation, str):
            self.unit_of_observation = str(self.unit_of_observation)

        if self.temporal_coverage is not None and not isinstance(self.temporal_coverage, TemporalCoverage):
            self.temporal_coverage = TemporalCoverage(**as_dict(self.temporal_coverage))

        if self.temporal_resolution is not None and not isinstance(self.temporal_resolution, str):
            self.temporal_resolution = str(self.temporal_resolution)

        if self.update_frequency is not None and not isinstance(self.update_frequency, str):
            self.update_frequency = str(self.update_frequency)

        if self.sampling_weights is not None and not isinstance(self.sampling_weights, str):
            self.sampling_weights = str(self.sampling_weights)

        if self.record_count is not None and not isinstance(self.record_count, int):
            self.record_count = int(self.record_count)

        if self.record_count_note is not None and not isinstance(self.record_count_note, str):
            self.record_count_note = str(self.record_count_note)

        if not isinstance(self.join_keys, list):
            self.join_keys = [self.join_keys] if self.join_keys is not None else []
        self.join_keys = [v if isinstance(v, JoinKey) else JoinKey(v) for v in self.join_keys]

        if self.variables_documented is not None and not isinstance(self.variables_documented, Bool):
            self.variables_documented = Bool(self.variables_documented)

        if self.machine_readable is not None and not isinstance(self.machine_readable, Bool):
            self.machine_readable = Bool(self.machine_readable)

        if self.versioned is not None and not isinstance(self.versioned, Bool):
            self.versioned = Bool(self.versioned)

        if self.persistent_identifier is not None and not isinstance(self.persistent_identifier, Bool):
            self.persistent_identifier = Bool(self.persistent_identifier)

        if self.known_limitations is not None and not isinstance(self.known_limitations, str):
            self.known_limitations = str(self.known_limitations)

        if self.notes is not None and not isinstance(self.notes, str):
            self.notes = str(self.notes)

        if self.verified is not None and not isinstance(self.verified, Verification):
            self.verified = Verification(**as_dict(self.verified))

        self._normalize_inlined_as_list(slot_name="variables", slot_type=VariableProfile, key_name="name", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Distribution(YAMLRoot):
    """
    One way of obtaining the data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Distribution"]
    class_class_curie: ClassVar[str] = "dcat:Distribution"
    class_name: ClassVar[str] = "Distribution"
    class_model_uri: ClassVar[URIRef] = META_URBAN.Distribution

    format: Optional[str] = None
    access_url: Optional[str] = None
    api: Optional[Union[bool, Bool]] = None
    registration_required: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.format is not None and not isinstance(self.format, str):
            self.format = str(self.format)

        if self.access_url is not None and not isinstance(self.access_url, str):
            self.access_url = str(self.access_url)

        if self.api is not None and not isinstance(self.api, Bool):
            self.api = Bool(self.api)

        if self.registration_required is not None and not isinstance(self.registration_required, Bool):
            self.registration_required = Bool(self.registration_required)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SpatialCoverage(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCT["Location"]
    class_class_curie: ClassVar[str] = "dct:Location"
    class_name: ClassVar[str] = "SpatialCoverage"
    class_model_uri: ClassVar[URIRef] = META_URBAN.SpatialCoverage

    countries: Optional[Union[str, list[str]]] = empty_list()
    description: Optional[str] = None
    bbox: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.countries, list):
            self.countries = [self.countries] if self.countries is not None else []
        self.countries = [v if isinstance(v, str) else str(v) for v in self.countries]

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.bbox is not None and not isinstance(self.bbox, str):
            self.bbox = str(self.bbox)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TemporalCoverage(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCT["PeriodOfTime"]
    class_class_curie: ClassVar[str] = "dct:PeriodOfTime"
    class_name: ClassVar[str] = "TemporalCoverage"
    class_model_uri: ClassVar[URIRef] = META_URBAN.TemporalCoverage

    start: Optional[str] = None
    end: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.start is not None and not isinstance(self.start, str):
            self.start = str(self.start)

        if self.end is not None and not isinstance(self.end, str):
            self.end = str(self.end)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Verification(YAMLRoot):
    """
    Provenance of the profile itself (who checked it, when, against which sources).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Activity"]
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "Verification"
    class_model_uri: ClassVar[URIRef] = META_URBAN.Verification

    date: Optional[str] = None
    by: Optional[str] = None
    sources_checked: Optional[Union[Union[str, URI], list[Union[str, URI]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.date is not None and not isinstance(self.date, str):
            self.date = str(self.date)

        if self.by is not None and not isinstance(self.by, str):
            self.by = str(self.by)

        if not isinstance(self.sources_checked, list):
            self.sources_checked = [self.sources_checked] if self.sources_checked is not None else []
        self.sources_checked = [v if isinstance(v, URI) else URI(v) for v in self.sources_checked]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class VariableProfile(YAMLRoot):
    """
    Variable-level (column-level) semantics. One VariableProfile per column of a tabular dataset, or per variable of a
    gridded dataset.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CSVW["Column"]
    class_class_curie: ClassVar[str] = "csvw:Column"
    class_name: ClassVar[str] = "VariableProfile"
    class_model_uri: ClassVar[URIRef] = META_URBAN.VariableProfile

    name: str = None
    label: Optional[str] = None
    description: Optional[str] = None
    datatype: Optional[Union[str, "VariableDatatype"]] = None
    concept: Optional[str] = None
    mapping_relation: Optional[Union[str, "MappingRelation"]] = None
    unit: Optional[str] = None
    unit_multiplier: Optional[float] = None
    aggregation: Optional[Union[str, "Aggregation"]] = None
    entity: Optional[Union[str, "EntityType"]] = None
    code_list: Optional[Union[Union[dict, "CodeEntry"], list[Union[dict, "CodeEntry"]]]] = empty_list()
    missing_codes: Optional[Union[str, list[str]]] = empty_list()
    is_weight: Optional[Union[bool, Bool]] = None
    is_imputation_flag: Optional[Union[bool, Bool]] = None
    flags_variable: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.datatype is not None and not isinstance(self.datatype, VariableDatatype):
            self.datatype = VariableDatatype(self.datatype)

        if self.concept is not None and not isinstance(self.concept, str):
            self.concept = str(self.concept)

        if self.mapping_relation is not None and not isinstance(self.mapping_relation, MappingRelation):
            self.mapping_relation = MappingRelation(self.mapping_relation)

        if self.unit is not None and not isinstance(self.unit, str):
            self.unit = str(self.unit)

        if self.unit_multiplier is not None and not isinstance(self.unit_multiplier, float):
            self.unit_multiplier = float(self.unit_multiplier)

        if self.aggregation is not None and not isinstance(self.aggregation, Aggregation):
            self.aggregation = Aggregation(self.aggregation)

        if self.entity is not None and not isinstance(self.entity, EntityType):
            self.entity = EntityType(self.entity)

        if not isinstance(self.code_list, list):
            self.code_list = [self.code_list] if self.code_list is not None else []
        self.code_list = [v if isinstance(v, CodeEntry) else CodeEntry(**as_dict(v)) for v in self.code_list]

        if not isinstance(self.missing_codes, list):
            self.missing_codes = [self.missing_codes] if self.missing_codes is not None else []
        self.missing_codes = [v if isinstance(v, str) else str(v) for v in self.missing_codes]

        if self.is_weight is not None and not isinstance(self.is_weight, Bool):
            self.is_weight = Bool(self.is_weight)

        if self.is_imputation_flag is not None and not isinstance(self.is_imputation_flag, Bool):
            self.is_imputation_flag = Bool(self.is_imputation_flag)

        if self.flags_variable is not None and not isinstance(self.flags_variable, str):
            self.flags_variable = str(self.flags_variable)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CodeEntry(YAMLRoot):
    """
    One code of a categorical variable and its meaning.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["Concept"]
    class_class_curie: ClassVar[str] = "skos:Concept"
    class_name: ClassVar[str] = "CodeEntry"
    class_model_uri: ClassVar[URIRef] = META_URBAN.CodeEntry

    code: Optional[str] = None
    label: Optional[str] = None
    concept_value: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.code is not None and not isinstance(self.code, str):
            self.code = str(self.code)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.concept_value is not None and not isinstance(self.concept_value, str):
            self.concept_value = str(self.concept_value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class UBEMConcept(YAMLRoot):
    """
    A concept in the Meta-Urban vocabulary: a quantity or attribute that a UBEM workflow consumes or produces (for
    example floor area, principal building activity, dry-bulb temperature, annual electricity use). Concepts form a
    hierarchy through `broader` and point to equivalent terms in other standards.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["Concept"]
    class_class_curie: ClassVar[str] = "skos:Concept"
    class_name: ClassVar[str] = "UBEMConcept"
    class_model_uri: ClassVar[URIRef] = META_URBAN.UBEMConcept

    id: Union[str, UBEMConceptId] = None
    pref_label: str = None
    definition: str = None
    alt_labels: Optional[Union[str, list[str]]] = empty_list()
    broader: Optional[Union[str, UBEMConceptId]] = None
    concept_role: Optional[Union[str, "UBEMRole"]] = None
    entity: Optional[Union[str, "EntityType"]] = None
    quantity_kind: Optional[str] = None
    canonical_unit: Optional[str] = None
    exact_match: Optional[Union[str, list[str]]] = empty_list()
    close_match: Optional[Union[str, list[str]]] = empty_list()
    broad_match: Optional[Union[str, list[str]]] = empty_list()
    narrow_match: Optional[Union[str, list[str]]] = empty_list()
    related_match: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, UBEMConceptId):
            self.id = UBEMConceptId(self.id)

        if self._is_empty(self.pref_label):
            self.MissingRequiredField("pref_label")
        if not isinstance(self.pref_label, str):
            self.pref_label = str(self.pref_label)

        if self._is_empty(self.definition):
            self.MissingRequiredField("definition")
        if not isinstance(self.definition, str):
            self.definition = str(self.definition)

        if not isinstance(self.alt_labels, list):
            self.alt_labels = [self.alt_labels] if self.alt_labels is not None else []
        self.alt_labels = [v if isinstance(v, str) else str(v) for v in self.alt_labels]

        if self.broader is not None and not isinstance(self.broader, UBEMConceptId):
            self.broader = UBEMConceptId(self.broader)

        if self.concept_role is not None and not isinstance(self.concept_role, UBEMRole):
            self.concept_role = UBEMRole(self.concept_role)

        if self.entity is not None and not isinstance(self.entity, EntityType):
            self.entity = EntityType(self.entity)

        if self.quantity_kind is not None and not isinstance(self.quantity_kind, str):
            self.quantity_kind = str(self.quantity_kind)

        if self.canonical_unit is not None and not isinstance(self.canonical_unit, str):
            self.canonical_unit = str(self.canonical_unit)

        if not isinstance(self.exact_match, list):
            self.exact_match = [self.exact_match] if self.exact_match is not None else []
        self.exact_match = [v if isinstance(v, str) else str(v) for v in self.exact_match]

        if not isinstance(self.close_match, list):
            self.close_match = [self.close_match] if self.close_match is not None else []
        self.close_match = [v if isinstance(v, str) else str(v) for v in self.close_match]

        if not isinstance(self.broad_match, list):
            self.broad_match = [self.broad_match] if self.broad_match is not None else []
        self.broad_match = [v if isinstance(v, str) else str(v) for v in self.broad_match]

        if not isinstance(self.narrow_match, list):
            self.narrow_match = [self.narrow_match] if self.narrow_match is not None else []
        self.narrow_match = [v if isinstance(v, str) else str(v) for v in self.narrow_match]

        if not isinstance(self.related_match, list):
            self.related_match = [self.related_match] if self.related_match is not None else []
        self.related_match = [v if isinstance(v, str) else str(v) for v in self.related_match]

        super().__post_init__(**kwargs)


# Enumerations
class UBEMRole(EnumDefinitionImpl):
    """
    The UBEM workflow step a dataset or concept serves.
    """
    boundary_conditions = PermissibleValue(
        text="boundary_conditions",
        description="Weather and climate drivers (observed, reanalysis, typical-year, projections).")
    geometry_inventory = PermissibleValue(
        text="geometry_inventory",
        description="Location and shape of buildings (footprints, heights, 3D models, parcels).")
    building_characteristics = PermissibleValue(
        text="building_characteristics",
        description="Non-geometric attributes (use type, vintage, envelope, systems, fuels, floor area).")
    operation_use = PermissibleValue(
        text="operation_use",
        description="Occupancy, schedules, occupant behavior, setpoints, plug loads.")
    calibration_validation = PermissibleValue(
        text="calibration_validation",
        description="Measured or reported energy use at any scale.")
    reference_simulation = PermissibleValue(
        text="reference_simulation",
        description="Synthetic building-stock model outputs and model libraries.")
    context_coupling = PermissibleValue(
        text="context_coupling",
        description="Socio-economic, land use, grid emissions, tariffs, urban microclimate.")

    _defn = EnumDefinition(
        name="UBEMRole",
        description="The UBEM workflow step a dataset or concept serves.",
    )

class GeographicScope(EnumDefinitionImpl):

    multinational = PermissibleValue(text="multinational")
    national = PermissibleValue(text="national")
    subnational = PermissibleValue(text="subnational")
    city = PermissibleValue(text="city")

    _defn = EnumDefinition(
        name="GeographicScope",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "global",
            PermissibleValue(text="global"))

class SpatialGranularity(EnumDefinitionImpl):
    """
    Ordered from finest to coarsest (see `rank` annotation).
    """
    point_station = PermissibleValue(text="point_station")
    building = PermissibleValue(text="building")
    parcel = PermissibleValue(text="parcel")
    grid_cell_fine = PermissibleValue(
        text="grid_cell_fine",
        description="<= 1 km")
    census_block_group = PermissibleValue(text="census_block_group")
    census_tract = PermissibleValue(text="census_tract")
    postal_code = PermissibleValue(text="postal_code")
    grid_cell_coarse = PermissibleValue(
        text="grid_cell_coarse",
        description="> 1 km")
    county = PermissibleValue(text="county")
    city = PermissibleValue(text="city")
    utility_service_territory = PermissibleValue(text="utility_service_territory")
    state_province = PermissibleValue(text="state_province")
    climate_zone = PermissibleValue(text="climate_zone")
    census_region_division = PermissibleValue(text="census_region_division")
    nation = PermissibleValue(text="nation")
    none = PermissibleValue(
        text="none",
        description="No location released")
    unknown = PermissibleValue(
        text="unknown",
        description="Could not be verified from public documentation")

    _defn = EnumDefinition(
        name="SpatialGranularity",
        description="Ordered from finest to coarsest (see `rank` annotation).",
    )

class StatisticalNature(EnumDefinitionImpl):

    census_complete = PermissibleValue(
        text="census_complete",
        description="Complete enumeration of a population.")
    sample_survey_weighted = PermissibleValue(
        text="sample_survey_weighted",
        description="Probability sample; estimates need weights.")
    administrative_record = PermissibleValue(
        text="administrative_record",
        description="""Records created by an administrative process (certificates, permits, disclosure, utility filings).""")
    measured_monitoring = PermissibleValue(
        text="measured_monitoring",
        description="Sensor or meter measurements.")
    remote_sensing_derived = PermissibleValue(
        text="remote_sensing_derived",
        description="Derived from satellite, aerial or lidar data with a model.")
    crowdsourced = PermissibleValue(
        text="crowdsourced",
        description="Volunteered geographic information.")
    reanalysis_model = PermissibleValue(
        text="reanalysis_model",
        description="Model-data assimilation product.")
    typical_year_synthetic = PermissibleValue(
        text="typical_year_synthetic",
        description="Typical meteorological year assembled from observations.")
    climate_projection = PermissibleValue(
        text="climate_projection",
        description="Output of climate models under scenarios.")
    simulation_synthetic = PermissibleValue(
        text="simulation_synthetic",
        description="Output of building energy simulation.")
    standard_or_code = PermissibleValue(
        text="standard_or_code",
        description="A standard, dictionary, code or reference model rather than observations.")
    compilation = PermissibleValue(
        text="compilation",
        description="Assembled from several of the above.")

    _defn = EnumDefinition(
        name="StatisticalNature",
    )

class AccessLevel(EnumDefinitionImpl):

    open_download = PermissibleValue(text="open_download")
    open_api = PermissibleValue(text="open_api")
    registration_required = PermissibleValue(text="registration_required")
    request_or_agreement = PermissibleValue(text="request_or_agreement")
    restricted_commercial = PermissibleValue(text="restricted_commercial")

    _defn = EnumDefinition(
        name="AccessLevel",
    )

class JoinKey(EnumDefinitionImpl):

    lat_lon = PermissibleValue(text="lat_lon")
    geometry = PermissibleValue(text="geometry")
    address = PermissibleValue(text="address")
    parcel_id = PermissibleValue(text="parcel_id")
    building_id = PermissibleValue(text="building_id")
    ubid = PermissibleValue(text="ubid")
    station_id = PermissibleValue(text="station_id")
    grid_cell = PermissibleValue(text="grid_cell")
    census_block_group = PermissibleValue(text="census_block_group")
    census_tract = PermissibleValue(text="census_tract")
    small_statistical_area = PermissibleValue(
        text="small_statistical_area",
        description="Non-U.S. small statistical areas such as UK LSOA/MSOA or national census grid ids")
    postal_code = PermissibleValue(text="postal_code")
    fips_county = PermissibleValue(text="fips_county")
    fips_state = PermissibleValue(text="fips_state")
    census_region_division = PermissibleValue(text="census_region_division")
    nuts_region = PermissibleValue(text="nuts_region")
    country_iso = PermissibleValue(text="country_iso")
    utility_id = PermissibleValue(text="utility_id")
    balancing_authority = PermissibleValue(text="balancing_authority")
    climate_zone_ashrae = PermissibleValue(text="climate_zone_ashrae")
    climate_zone_iecc = PermissibleValue(text="climate_zone_iecc")
    building_type = PermissibleValue(text="building_type")
    vintage = PermissibleValue(text="vintage")
    timestamp = PermissibleValue(text="timestamp")

    _defn = EnumDefinition(
        name="JoinKey",
    )

class VariableDatatype(EnumDefinitionImpl):

    integer = PermissibleValue(text="integer")
    float = PermissibleValue(text="float")
    string = PermissibleValue(text="string")
    categorical = PermissibleValue(text="categorical")
    boolean = PermissibleValue(text="boolean")
    datetime = PermissibleValue(text="datetime")
    geometry = PermissibleValue(text="geometry")
    identifier = PermissibleValue(text="identifier")

    _defn = EnumDefinition(
        name="VariableDatatype",
    )

class MappingRelation(EnumDefinitionImpl):

    exactMatch = PermissibleValue(
        text="exactMatch",
        meaning=SKOS["exactMatch"])
    closeMatch = PermissibleValue(
        text="closeMatch",
        meaning=SKOS["closeMatch"])
    broadMatch = PermissibleValue(
        text="broadMatch",
        meaning=SKOS["broadMatch"])
    narrowMatch = PermissibleValue(
        text="narrowMatch",
        meaning=SKOS["narrowMatch"])
    relatedMatch = PermissibleValue(
        text="relatedMatch",
        meaning=SKOS["relatedMatch"])

    _defn = EnumDefinition(
        name="MappingRelation",
    )

class Aggregation(EnumDefinitionImpl):
    """
    How a value relates to time.
    """
    static = PermissibleValue(
        text="static",
        description="Attribute that does not vary in the observation period.")
    instantaneous = PermissibleValue(text="instantaneous")
    total_over_period = PermissibleValue(text="total_over_period")
    average_over_period = PermissibleValue(text="average_over_period")
    count = PermissibleValue(text="count")
    share = PermissibleValue(text="share")

    _defn = EnumDefinition(
        name="Aggregation",
        description="How a value relates to time.",
    )

class EntityType(EnumDefinitionImpl):
    """
    What a concept or variable describes.
    """
    site = PermissibleValue(text="site")
    building = PermissibleValue(text="building")
    zone = PermissibleValue(text="zone")
    system = PermissibleValue(text="system")
    envelope = PermissibleValue(text="envelope")
    household = PermissibleValue(text="household")
    occupant = PermissibleValue(text="occupant")
    meter = PermissibleValue(text="meter")
    region = PermissibleValue(text="region")
    weather_station = PermissibleValue(text="weather_station")
    grid_cell = PermissibleValue(text="grid_cell")
    dataset_record = PermissibleValue(
        text="dataset_record",
        description="Record bookkeeping (identifiers, weights, flags).")

    _defn = EnumDefinition(
        name="EntityType",
        description="What a concept or variable describes.",
    )

# Slots
class slots:
    pass

slots.datasets = Slot(uri=META_URBAN.datasets, name="datasets", curie=META_URBAN.curie('datasets'),
                   model_uri=META_URBAN.datasets, domain=None, range=Optional[Union[dict[Union[str, DatasetProfileId], Union[dict, DatasetProfile]], list[Union[dict, DatasetProfile]]]])

slots.concepts = Slot(uri=META_URBAN.concepts, name="concepts", curie=META_URBAN.curie('concepts'),
                   model_uri=META_URBAN.concepts, domain=None, range=Optional[Union[dict[Union[str, UBEMConceptId], Union[dict, UBEMConcept]], list[Union[dict, UBEMConcept]]]])

slots.id = Slot(uri=META_URBAN.id, name="id", curie=META_URBAN.curie('id'),
                   model_uri=META_URBAN.id, domain=None, range=URIRef,
                   pattern=re.compile(r'^[a-z0-9][a-z0-9_.-]*$'))

slots.title = Slot(uri=DCT.title, name="title", curie=DCT.curie('title'),
                   model_uri=META_URBAN.title, domain=None, range=Optional[str])

slots.short_name = Slot(uri=SKOS.altLabel, name="short_name", curie=SKOS.curie('altLabel'),
                   model_uri=META_URBAN.short_name, domain=None, range=Optional[str])

slots.publisher = Slot(uri=DCT.publisher, name="publisher", curie=DCT.curie('publisher'),
                   model_uri=META_URBAN.publisher, domain=None, range=Optional[str])

slots.landing_page = Slot(uri=DCAT.landingPage, name="landing_page", curie=DCAT.curie('landingPage'),
                   model_uri=META_URBAN.landing_page, domain=None, range=Optional[Union[str, URI]])

slots.doi = Slot(uri=META_URBAN.doi, name="doi", curie=META_URBAN.curie('doi'),
                   model_uri=META_URBAN.doi, domain=None, range=Optional[str],
                   pattern=re.compile(r'^10\.\d{4,9}/\S+$'))

slots.citation = Slot(uri=DCT.bibliographicCitation, name="citation", curie=DCT.curie('bibliographicCitation'),
                   model_uri=META_URBAN.citation, domain=None, range=Optional[str])

slots.reference_paper_doi = Slot(uri=META_URBAN.reference_paper_doi, name="reference_paper_doi", curie=META_URBAN.curie('reference_paper_doi'),
                   model_uri=META_URBAN.reference_paper_doi, domain=None, range=Optional[str],
                   pattern=re.compile(r'^10\.\d{4,9}/\S+$'))

slots.license = Slot(uri=DCT.license, name="license", curie=DCT.curie('license'),
                   model_uri=META_URBAN.license, domain=None, range=Optional[str])

slots.access_level = Slot(uri=META_URBAN.access_level, name="access_level", curie=META_URBAN.curie('access_level'),
                   model_uri=META_URBAN.access_level, domain=None, range=Optional[Union[str, "AccessLevel"]])

slots.distributions = Slot(uri=DCAT.distribution, name="distributions", curie=DCAT.curie('distribution'),
                   model_uri=META_URBAN.distributions, domain=None, range=Optional[Union[Union[dict, Distribution], list[Union[dict, Distribution]]]])

slots.format = Slot(uri=DCT.format, name="format", curie=DCT.curie('format'),
                   model_uri=META_URBAN.format, domain=None, range=Optional[str])

slots.access_url = Slot(uri=DCAT.accessURL, name="access_url", curie=DCAT.curie('accessURL'),
                   model_uri=META_URBAN.access_url, domain=None, range=Optional[str])

slots.api = Slot(uri=META_URBAN.api, name="api", curie=META_URBAN.curie('api'),
                   model_uri=META_URBAN.api, domain=None, range=Optional[Union[bool, Bool]])

slots.registration_required = Slot(uri=META_URBAN.registration_required, name="registration_required", curie=META_URBAN.curie('registration_required'),
                   model_uri=META_URBAN.registration_required, domain=None, range=Optional[Union[bool, Bool]])

slots.ubem_roles = Slot(uri=META_URBAN.ubem_roles, name="ubem_roles", curie=META_URBAN.curie('ubem_roles'),
                   model_uri=META_URBAN.ubem_roles, domain=None, range=Optional[Union[Union[str, "UBEMRole"], list[Union[str, "UBEMRole"]]]])

slots.content_types = Slot(uri=DCAT.theme, name="content_types", curie=DCAT.curie('theme'),
                   model_uri=META_URBAN.content_types, domain=None, range=Optional[Union[str, list[str]]])

slots.geographic_scope = Slot(uri=META_URBAN.geographic_scope, name="geographic_scope", curie=META_URBAN.curie('geographic_scope'),
                   model_uri=META_URBAN.geographic_scope, domain=None, range=Optional[Union[str, "GeographicScope"]])

slots.spatial_coverage = Slot(uri=DCT.spatial, name="spatial_coverage", curie=DCT.curie('spatial'),
                   model_uri=META_URBAN.spatial_coverage, domain=None, range=Optional[Union[dict, SpatialCoverage]])

slots.countries = Slot(uri=META_URBAN.countries, name="countries", curie=META_URBAN.curie('countries'),
                   model_uri=META_URBAN.countries, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^([A-Z]{2}|GLOBAL|EU)$'))

slots.bbox = Slot(uri=DCAT.bbox, name="bbox", curie=DCAT.curie('bbox'),
                   model_uri=META_URBAN.bbox, domain=None, range=Optional[str])

slots.unit_of_observation = Slot(uri=META_URBAN.unit_of_observation, name="unit_of_observation", curie=META_URBAN.curie('unit_of_observation'),
                   model_uri=META_URBAN.unit_of_observation, domain=None, range=Optional[str])

slots.spatial_granularity = Slot(uri=META_URBAN.spatial_granularity, name="spatial_granularity", curie=META_URBAN.curie('spatial_granularity'),
                   model_uri=META_URBAN.spatial_granularity, domain=None, range=Optional[Union[str, "SpatialGranularity"]])

slots.temporal_coverage = Slot(uri=DCT.temporal, name="temporal_coverage", curie=DCT.curie('temporal'),
                   model_uri=META_URBAN.temporal_coverage, domain=None, range=Optional[Union[dict, TemporalCoverage]])

slots.start = Slot(uri=DCAT.startDate, name="start", curie=DCAT.curie('startDate'),
                   model_uri=META_URBAN.start, domain=None, range=Optional[str])

slots.end = Slot(uri=DCAT.endDate, name="end", curie=DCAT.curie('endDate'),
                   model_uri=META_URBAN.end, domain=None, range=Optional[str])

slots.temporal_resolution = Slot(uri=DCAT.temporalResolution, name="temporal_resolution", curie=DCAT.curie('temporalResolution'),
                   model_uri=META_URBAN.temporal_resolution, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(P(?!$)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(T(?=\d)(\d+H)?(\d+M)?(\d+(\.\d+)?S)?)?|static|irregular)$'))

slots.update_frequency = Slot(uri=DCT.accrualPeriodicity, name="update_frequency", curie=DCT.curie('accrualPeriodicity'),
                   model_uri=META_URBAN.update_frequency, domain=None, range=Optional[str])

slots.statistical_nature = Slot(uri=META_URBAN.statistical_nature, name="statistical_nature", curie=META_URBAN.curie('statistical_nature'),
                   model_uri=META_URBAN.statistical_nature, domain=None, range=Optional[Union[str, "StatisticalNature"]])

slots.sampling_weights = Slot(uri=META_URBAN.sampling_weights, name="sampling_weights", curie=META_URBAN.curie('sampling_weights'),
                   model_uri=META_URBAN.sampling_weights, domain=None, range=Optional[str])

slots.record_count = Slot(uri=META_URBAN.record_count, name="record_count", curie=META_URBAN.curie('record_count'),
                   model_uri=META_URBAN.record_count, domain=None, range=Optional[int])

slots.record_count_note = Slot(uri=META_URBAN.record_count_note, name="record_count_note", curie=META_URBAN.curie('record_count_note'),
                   model_uri=META_URBAN.record_count_note, domain=None, range=Optional[str])

slots.join_keys = Slot(uri=META_URBAN.join_keys, name="join_keys", curie=META_URBAN.curie('join_keys'),
                   model_uri=META_URBAN.join_keys, domain=None, range=Optional[Union[Union[str, "JoinKey"], list[Union[str, "JoinKey"]]]])

slots.variables_documented = Slot(uri=META_URBAN.variables_documented, name="variables_documented", curie=META_URBAN.curie('variables_documented'),
                   model_uri=META_URBAN.variables_documented, domain=None, range=Optional[Union[bool, Bool]])

slots.machine_readable = Slot(uri=META_URBAN.machine_readable, name="machine_readable", curie=META_URBAN.curie('machine_readable'),
                   model_uri=META_URBAN.machine_readable, domain=None, range=Optional[Union[bool, Bool]])

slots.versioned = Slot(uri=META_URBAN.versioned, name="versioned", curie=META_URBAN.curie('versioned'),
                   model_uri=META_URBAN.versioned, domain=None, range=Optional[Union[bool, Bool]])

slots.persistent_identifier = Slot(uri=META_URBAN.persistent_identifier, name="persistent_identifier", curie=META_URBAN.curie('persistent_identifier'),
                   model_uri=META_URBAN.persistent_identifier, domain=None, range=Optional[Union[bool, Bool]])

slots.known_limitations = Slot(uri=META_URBAN.known_limitations, name="known_limitations", curie=META_URBAN.curie('known_limitations'),
                   model_uri=META_URBAN.known_limitations, domain=None, range=Optional[str])

slots.notes = Slot(uri=META_URBAN.notes, name="notes", curie=META_URBAN.curie('notes'),
                   model_uri=META_URBAN.notes, domain=None, range=Optional[str])

slots.verified = Slot(uri=PROV.wasGeneratedBy, name="verified", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=META_URBAN.verified, domain=None, range=Optional[Union[dict, Verification]])

slots.date = Slot(uri=META_URBAN.date, name="date", curie=META_URBAN.curie('date'),
                   model_uri=META_URBAN.date, domain=None, range=Optional[str])

slots.by = Slot(uri=META_URBAN.by, name="by", curie=META_URBAN.curie('by'),
                   model_uri=META_URBAN.by, domain=None, range=Optional[str])

slots.sources_checked = Slot(uri=META_URBAN.sources_checked, name="sources_checked", curie=META_URBAN.curie('sources_checked'),
                   model_uri=META_URBAN.sources_checked, domain=None, range=Optional[Union[Union[str, URI], list[Union[str, URI]]]])

slots.variables = Slot(uri=META_URBAN.variables, name="variables", curie=META_URBAN.curie('variables'),
                   model_uri=META_URBAN.variables, domain=None, range=Optional[Union[Union[dict, VariableProfile], list[Union[dict, VariableProfile]]]])

slots.name = Slot(uri=CSVW.name, name="name", curie=CSVW.curie('name'),
                   model_uri=META_URBAN.name, domain=None, range=Optional[str])

slots.label = Slot(uri=SKOS.prefLabel, name="label", curie=SKOS.curie('prefLabel'),
                   model_uri=META_URBAN.label, domain=None, range=Optional[str])

slots.description = Slot(uri=DCT.description, name="description", curie=DCT.curie('description'),
                   model_uri=META_URBAN.description, domain=None, range=Optional[str])

slots.datatype = Slot(uri=META_URBAN.datatype, name="datatype", curie=META_URBAN.curie('datatype'),
                   model_uri=META_URBAN.datatype, domain=None, range=Optional[Union[str, "VariableDatatype"]])

slots.concept = Slot(uri=SKOS.related, name="concept", curie=SKOS.curie('related'),
                   model_uri=META_URBAN.concept, domain=None, range=Optional[str])

slots.mapping_relation = Slot(uri=META_URBAN.mapping_relation, name="mapping_relation", curie=META_URBAN.curie('mapping_relation'),
                   model_uri=META_URBAN.mapping_relation, domain=None, range=Optional[Union[str, "MappingRelation"]])

slots.unit = Slot(uri=QUDT.unit, name="unit", curie=QUDT.curie('unit'),
                   model_uri=META_URBAN.unit, domain=None, range=Optional[str])

slots.unit_multiplier = Slot(uri=META_URBAN.unit_multiplier, name="unit_multiplier", curie=META_URBAN.curie('unit_multiplier'),
                   model_uri=META_URBAN.unit_multiplier, domain=None, range=Optional[float])

slots.aggregation = Slot(uri=META_URBAN.aggregation, name="aggregation", curie=META_URBAN.curie('aggregation'),
                   model_uri=META_URBAN.aggregation, domain=None, range=Optional[Union[str, "Aggregation"]])

slots.entity = Slot(uri=META_URBAN.entity, name="entity", curie=META_URBAN.curie('entity'),
                   model_uri=META_URBAN.entity, domain=None, range=Optional[Union[str, "EntityType"]])

slots.code_list = Slot(uri=META_URBAN.code_list, name="code_list", curie=META_URBAN.curie('code_list'),
                   model_uri=META_URBAN.code_list, domain=None, range=Optional[Union[Union[dict, CodeEntry], list[Union[dict, CodeEntry]]]])

slots.code = Slot(uri=META_URBAN.code, name="code", curie=META_URBAN.curie('code'),
                   model_uri=META_URBAN.code, domain=None, range=Optional[str])

slots.concept_value = Slot(uri=META_URBAN.concept_value, name="concept_value", curie=META_URBAN.curie('concept_value'),
                   model_uri=META_URBAN.concept_value, domain=None, range=Optional[str])

slots.missing_codes = Slot(uri=META_URBAN.missing_codes, name="missing_codes", curie=META_URBAN.curie('missing_codes'),
                   model_uri=META_URBAN.missing_codes, domain=None, range=Optional[Union[str, list[str]]])

slots.is_weight = Slot(uri=META_URBAN.is_weight, name="is_weight", curie=META_URBAN.curie('is_weight'),
                   model_uri=META_URBAN.is_weight, domain=None, range=Optional[Union[bool, Bool]])

slots.is_imputation_flag = Slot(uri=META_URBAN.is_imputation_flag, name="is_imputation_flag", curie=META_URBAN.curie('is_imputation_flag'),
                   model_uri=META_URBAN.is_imputation_flag, domain=None, range=Optional[Union[bool, Bool]])

slots.flags_variable = Slot(uri=META_URBAN.flags_variable, name="flags_variable", curie=META_URBAN.curie('flags_variable'),
                   model_uri=META_URBAN.flags_variable, domain=None, range=Optional[str])

slots.pref_label = Slot(uri=SKOS.prefLabel, name="pref_label", curie=SKOS.curie('prefLabel'),
                   model_uri=META_URBAN.pref_label, domain=None, range=Optional[str])

slots.definition = Slot(uri=SKOS.definition, name="definition", curie=SKOS.curie('definition'),
                   model_uri=META_URBAN.definition, domain=None, range=Optional[str])

slots.alt_labels = Slot(uri=SKOS.altLabel, name="alt_labels", curie=SKOS.curie('altLabel'),
                   model_uri=META_URBAN.alt_labels, domain=None, range=Optional[Union[str, list[str]]])

slots.broader = Slot(uri=SKOS.broader, name="broader", curie=SKOS.curie('broader'),
                   model_uri=META_URBAN.broader, domain=None, range=Optional[Union[str, UBEMConceptId]])

slots.concept_role = Slot(uri=META_URBAN.concept_role, name="concept_role", curie=META_URBAN.curie('concept_role'),
                   model_uri=META_URBAN.concept_role, domain=None, range=Optional[Union[str, "UBEMRole"]])

slots.quantity_kind = Slot(uri=QUDT.hasQuantityKind, name="quantity_kind", curie=QUDT.curie('hasQuantityKind'),
                   model_uri=META_URBAN.quantity_kind, domain=None, range=Optional[str])

slots.canonical_unit = Slot(uri=META_URBAN.canonical_unit, name="canonical_unit", curie=META_URBAN.curie('canonical_unit'),
                   model_uri=META_URBAN.canonical_unit, domain=None, range=Optional[str])

slots.exact_match = Slot(uri=SKOS.exactMatch, name="exact_match", curie=SKOS.curie('exactMatch'),
                   model_uri=META_URBAN.exact_match, domain=None, range=Optional[Union[str, list[str]]])

slots.close_match = Slot(uri=SKOS.closeMatch, name="close_match", curie=SKOS.curie('closeMatch'),
                   model_uri=META_URBAN.close_match, domain=None, range=Optional[Union[str, list[str]]])

slots.related_match = Slot(uri=SKOS.relatedMatch, name="related_match", curie=SKOS.curie('relatedMatch'),
                   model_uri=META_URBAN.related_match, domain=None, range=Optional[Union[str, list[str]]])

slots.broad_match = Slot(uri=SKOS.broadMatch, name="broad_match", curie=SKOS.curie('broadMatch'),
                   model_uri=META_URBAN.broad_match, domain=None, range=Optional[Union[str, list[str]]])

slots.narrow_match = Slot(uri=SKOS.narrowMatch, name="narrow_match", curie=SKOS.curie('narrowMatch'),
                   model_uri=META_URBAN.narrow_match, domain=None, range=Optional[Union[str, list[str]]])

slots.DatasetProfile_id = Slot(uri=META_URBAN.id, name="DatasetProfile_id", curie=META_URBAN.curie('id'),
                   model_uri=META_URBAN.DatasetProfile_id, domain=DatasetProfile, range=Union[str, DatasetProfileId],
                   pattern=re.compile(r'^[a-z0-9][a-z0-9_.-]*$'))

slots.DatasetProfile_title = Slot(uri=DCT.title, name="DatasetProfile_title", curie=DCT.curie('title'),
                   model_uri=META_URBAN.DatasetProfile_title, domain=DatasetProfile, range=str)

slots.DatasetProfile_ubem_roles = Slot(uri=META_URBAN.ubem_roles, name="DatasetProfile_ubem_roles", curie=META_URBAN.curie('ubem_roles'),
                   model_uri=META_URBAN.DatasetProfile_ubem_roles, domain=DatasetProfile, range=Union[Union[str, "UBEMRole"], list[Union[str, "UBEMRole"]]])

slots.DatasetProfile_statistical_nature = Slot(uri=META_URBAN.statistical_nature, name="DatasetProfile_statistical_nature", curie=META_URBAN.curie('statistical_nature'),
                   model_uri=META_URBAN.DatasetProfile_statistical_nature, domain=DatasetProfile, range=Union[str, "StatisticalNature"])

slots.DatasetProfile_spatial_granularity = Slot(uri=META_URBAN.spatial_granularity, name="DatasetProfile_spatial_granularity", curie=META_URBAN.curie('spatial_granularity'),
                   model_uri=META_URBAN.DatasetProfile_spatial_granularity, domain=DatasetProfile, range=Union[str, "SpatialGranularity"])

slots.DatasetProfile_access_level = Slot(uri=META_URBAN.access_level, name="DatasetProfile_access_level", curie=META_URBAN.curie('access_level'),
                   model_uri=META_URBAN.DatasetProfile_access_level, domain=DatasetProfile, range=Union[str, "AccessLevel"])

slots.VariableProfile_name = Slot(uri=CSVW.name, name="VariableProfile_name", curie=CSVW.curie('name'),
                   model_uri=META_URBAN.VariableProfile_name, domain=VariableProfile, range=str)

slots.UBEMConcept_id = Slot(uri=META_URBAN.id, name="UBEMConcept_id", curie=META_URBAN.curie('id'),
                   model_uri=META_URBAN.UBEMConcept_id, domain=UBEMConcept, range=Union[str, UBEMConceptId],
                   pattern=re.compile(r'^[a-z0-9][a-z0-9_.-]*$'))

slots.UBEMConcept_pref_label = Slot(uri=SKOS.prefLabel, name="UBEMConcept_pref_label", curie=SKOS.curie('prefLabel'),
                   model_uri=META_URBAN.UBEMConcept_pref_label, domain=UBEMConcept, range=str)

slots.UBEMConcept_definition = Slot(uri=SKOS.definition, name="UBEMConcept_definition", curie=SKOS.curie('definition'),
                   model_uri=META_URBAN.UBEMConcept_definition, domain=UBEMConcept, range=str)

