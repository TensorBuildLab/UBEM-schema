# Auto generated from ubem_link.yaml by pythongen.py version: 0.0.1
# Schema: ubem_link
#
# id: https://w3id.org/ubem-link/schema
# description: UBEM-Link describes open datasets used in urban building energy modeling (UBEM) at two levels. The dataset level (DatasetProfile) is an application profile of W3C DCAT 3 with UBEM-specific facets: the UBEM workflow role, statistical nature, spatial granularity, temporal resolution, access level and join keys. The variable level (VariableProfile) records what each column means for UBEM: the concept it maps to in the UBEM-Link vocabulary, its unit (QUDT), its code list, its aggregation semantics, and whether it is a survey weight or an imputation flag. Concepts (UBEMConcept) form a SKOS hierarchy and carry mappings to BEDES, Brick, CityGML Energy ADE and EnergyPlus input objects. Between the two levels, one category profile per UBEM workflow role (WeatherProfile, GeometryProfile, OperationProfile, CharacteristicsProfile, EnergyProfile, SimulationProfile, ContextProfile) records what a modeler must know about that kind of data. The roles and category profiles refine an earlier seven-category taxonomy of open UBEM data (weather information; building stock GIS; occupant behavior; building characteristics; macroscopic energy; microscopic energy; comprehensive data lakes) and its per-category metadata table.
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
version = "1.0.0"

# Namespaces
BEDES = CurieNamespace('bedes', 'https://bedes.lbl.gov/node/')
BRICK = CurieNamespace('brick', 'https://brickschema.org/schema/Brick#')
CSVW = CurieNamespace('csvw', 'http://www.w3.org/ns/csvw#')
DCAT = CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#')
DCT = CurieNamespace('dct', 'http://purl.org/dc/terms/')
ENERGY = CurieNamespace('energy', 'http://www.sig3d.org/citygml/2.0/energy/1.0#')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
QUANTITYKIND = CurieNamespace('quantitykind', 'http://qudt.org/vocab/quantitykind/')
QUDT = CurieNamespace('qudt', 'http://qudt.org/schema/qudt/')
REC = CurieNamespace('rec', 'https://w3id.org/rec#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
UBEM_LINK = CurieNamespace('ubem_link', 'https://w3id.org/ubem-link/')
UNIT = CurieNamespace('unit', 'http://qudt.org/vocab/unit/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = UBEM_LINK


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
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.Catalog

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
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.DatasetProfile

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
    conventions: Optional[Union[Union[dict, "Convention"], list[Union[dict, "Convention"]]]] = empty_list()
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
    weather_profile: Optional[Union[dict, "WeatherProfile"]] = None
    geometry_profile: Optional[Union[dict, "GeometryProfile"]] = None
    operation_profile: Optional[Union[dict, "OperationProfile"]] = None
    characteristics_profile: Optional[Union[dict, "CharacteristicsProfile"]] = None
    energy_profile: Optional[Union[dict, "EnergyProfile"]] = None
    simulation_profile: Optional[Union[dict, "SimulationProfile"]] = None
    context_profile: Optional[Union[dict, "ContextProfile"]] = None
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

        self._normalize_inlined_as_list(slot_name="conventions", slot_type=Convention, key_name="rule", keyed=False)

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

        if self.weather_profile is not None and not isinstance(self.weather_profile, WeatherProfile):
            self.weather_profile = WeatherProfile(**as_dict(self.weather_profile))

        if self.geometry_profile is not None and not isinstance(self.geometry_profile, GeometryProfile):
            self.geometry_profile = GeometryProfile(**as_dict(self.geometry_profile))

        if self.operation_profile is not None and not isinstance(self.operation_profile, OperationProfile):
            self.operation_profile = OperationProfile(**as_dict(self.operation_profile))

        if self.characteristics_profile is not None and not isinstance(self.characteristics_profile, CharacteristicsProfile):
            self.characteristics_profile = CharacteristicsProfile(**as_dict(self.characteristics_profile))

        if self.energy_profile is not None and not isinstance(self.energy_profile, EnergyProfile):
            self.energy_profile = EnergyProfile(**as_dict(self.energy_profile))

        if self.simulation_profile is not None and not isinstance(self.simulation_profile, SimulationProfile):
            self.simulation_profile = SimulationProfile(**as_dict(self.simulation_profile))

        if self.context_profile is not None and not isinstance(self.context_profile, ContextProfile):
            self.context_profile = ContextProfile(**as_dict(self.context_profile))

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
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.Distribution

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
    """
    Geographic area a dataset covers.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCT["Location"]
    class_class_curie: ClassVar[str] = "dct:Location"
    class_name: ClassVar[str] = "SpatialCoverage"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.SpatialCoverage

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
    """
    Period of time a dataset covers.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCT["PeriodOfTime"]
    class_class_curie: ClassVar[str] = "dct:PeriodOfTime"
    class_name: ClassVar[str] = "TemporalCoverage"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.TemporalCoverage

    start: Optional[str] = None
    end: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.start is not None and not isinstance(self.start, str):
            self.start = str(self.start)

        if self.end is not None and not isinstance(self.end, str):
            self.end = str(self.end)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Convention(YAMLRoot):
    """
    A rule the publisher applies to many variables at once, such as a naming pattern for imputation flags, a code that
    means "not applicable", or a unit used for all energy totals. Conventions are usually stated once in a user guide
    and never in the individual codebook entries, so a person or an AI system reading one entry cannot infer them; the
    profile states them explicitly.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = UBEM_LINK["Convention"]
    class_class_curie: ClassVar[str] = "ubem_link:Convention"
    class_name: ClassVar[str] = "Convention"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.Convention

    rule: str = None
    convention_type: Optional[Union[str, "ConventionType"]] = None
    applies_to: Optional[str] = None
    applies_to_variables: Optional[Union[str, list[str]]] = empty_list()
    applies_to_pattern: Optional[str] = None
    applies_to_codes: Optional[Union[str, list[str]]] = empty_list()
    example: Optional[str] = None
    missing_codes: Optional[Union[str, list[str]]] = empty_list()
    unit: Optional[str] = None
    unit_multiplier: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.rule):
            self.MissingRequiredField("rule")
        if not isinstance(self.rule, str):
            self.rule = str(self.rule)

        if self.convention_type is not None and not isinstance(self.convention_type, ConventionType):
            self.convention_type = ConventionType(self.convention_type)

        if self.applies_to is not None and not isinstance(self.applies_to, str):
            self.applies_to = str(self.applies_to)

        if not isinstance(self.applies_to_variables, list):
            self.applies_to_variables = [self.applies_to_variables] if self.applies_to_variables is not None else []
        self.applies_to_variables = [v if isinstance(v, str) else str(v) for v in self.applies_to_variables]

        if self.applies_to_pattern is not None and not isinstance(self.applies_to_pattern, str):
            self.applies_to_pattern = str(self.applies_to_pattern)

        if not isinstance(self.applies_to_codes, list):
            self.applies_to_codes = [self.applies_to_codes] if self.applies_to_codes is not None else []
        self.applies_to_codes = [v if isinstance(v, str) else str(v) for v in self.applies_to_codes]

        if self.example is not None and not isinstance(self.example, str):
            self.example = str(self.example)

        if not isinstance(self.missing_codes, list):
            self.missing_codes = [self.missing_codes] if self.missing_codes is not None else []
        self.missing_codes = [v if isinstance(v, str) else str(v) for v in self.missing_codes]

        if self.unit is not None and not isinstance(self.unit, str):
            self.unit = str(self.unit)

        if self.unit_multiplier is not None and not isinstance(self.unit_multiplier, float):
            self.unit_multiplier = float(self.unit_multiplier)

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
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.Verification

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
class CategoryProfile(YAMLRoot):
    """
    Category-specific part of a dataset profile: what a modeler must know about one kind of UBEM data before using it.
    There is one profile class per UBEM workflow role. Existing classifications of open UBEM data record this
    information as free-text checklists; here every field is typed with a closed value list, macroscopic and
    microscopic energy data share EnergyProfile and differ in energy_data_scale, and a data lake is a Catalog of
    profiles rather than a category.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = UBEM_LINK["CategoryProfile"]
    class_class_curie: ClassVar[str] = "ubem_link:CategoryProfile"
    class_name: ClassVar[str] = "CategoryProfile"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.CategoryProfile

    provides_concepts: Optional[Union[str, list[str]]] = empty_list()
    metadata_standards: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.provides_concepts, list):
            self.provides_concepts = [self.provides_concepts] if self.provides_concepts is not None else []
        self.provides_concepts = [v if isinstance(v, str) else str(v) for v in self.provides_concepts]

        if not isinstance(self.metadata_standards, list):
            self.metadata_standards = [self.metadata_standards] if self.metadata_standards is not None else []
        self.metadata_standards = [v if isinstance(v, str) else str(v) for v in self.metadata_standards]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class WeatherProfile(CategoryProfile):
    """
    Weather and climate data used as boundary conditions: observed station records, reanalyses, typical and actual
    meteorological years, and climate projections.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = UBEM_LINK["WeatherProfile"]
    class_class_curie: ClassVar[str] = "ubem_link:WeatherProfile"
    class_name: ClassVar[str] = "WeatherProfile"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.WeatherProfile

    weather_year_type: Union[Union[str, "WeatherYearType"], list[Union[str, "WeatherYearType"]]] = None
    weather_file_format: Optional[Union[Union[str, "WeatherFileFormat"], list[Union[str, "WeatherFileFormat"]]]] = empty_list()
    timestamp_convention: Optional[Union[str, "TimestampConvention"]] = None
    time_basis: Optional[Union[str, "TimeBasis"]] = None
    gap_filling: Optional[Union[str, "GapFilling"]] = None
    grid_resolution_km: Optional[float] = None
    station_id_scheme: Optional[str] = None
    climate_scenarios: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.weather_year_type):
            self.MissingRequiredField("weather_year_type")
        if not isinstance(self.weather_year_type, list):
            self.weather_year_type = [self.weather_year_type] if self.weather_year_type is not None else []
        self.weather_year_type = [v if isinstance(v, WeatherYearType) else WeatherYearType(v) for v in self.weather_year_type]

        if not isinstance(self.weather_file_format, list):
            self.weather_file_format = [self.weather_file_format] if self.weather_file_format is not None else []
        self.weather_file_format = [v if isinstance(v, WeatherFileFormat) else WeatherFileFormat(v) for v in self.weather_file_format]

        if self.timestamp_convention is not None and not isinstance(self.timestamp_convention, TimestampConvention):
            self.timestamp_convention = TimestampConvention(self.timestamp_convention)

        if self.time_basis is not None and not isinstance(self.time_basis, TimeBasis):
            self.time_basis = TimeBasis(self.time_basis)

        if self.gap_filling is not None and not isinstance(self.gap_filling, GapFilling):
            self.gap_filling = GapFilling(self.gap_filling)

        if self.grid_resolution_km is not None and not isinstance(self.grid_resolution_km, float):
            self.grid_resolution_km = float(self.grid_resolution_km)

        if self.station_id_scheme is not None and not isinstance(self.station_id_scheme, str):
            self.station_id_scheme = str(self.station_id_scheme)

        if not isinstance(self.climate_scenarios, list):
            self.climate_scenarios = [self.climate_scenarios] if self.climate_scenarios is not None else []
        self.climate_scenarios = [v if isinstance(v, str) else str(v) for v in self.climate_scenarios]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GeometryProfile(CategoryProfile):
    """
    Building stock geometry and inventory: footprints, heights, 3D city models and parcels.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = UBEM_LINK["GeometryProfile"]
    class_class_curie: ClassVar[str] = "ubem_link:GeometryProfile"
    class_name: ClassVar[str] = "GeometryProfile"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.GeometryProfile

    geometry_dimension: Union[str, "GeometryDimension"] = None
    levels_of_detail: Optional[Union[Union[str, "LevelOfDetail"], list[Union[str, "LevelOfDetail"]]]] = empty_list()
    height_source: Optional[Union[Union[str, "HeightSource"], list[Union[str, "HeightSource"]]]] = empty_list()
    height_reference: Optional[Union[str, "HeightReference"]] = None
    coordinate_reference_system: Optional[str] = None
    crs_linear_unit: Optional[str] = None
    building_id_scheme: Optional[str] = None
    minimum_building_size: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.geometry_dimension):
            self.MissingRequiredField("geometry_dimension")
        if not isinstance(self.geometry_dimension, GeometryDimension):
            self.geometry_dimension = GeometryDimension(self.geometry_dimension)

        if not isinstance(self.levels_of_detail, list):
            self.levels_of_detail = [self.levels_of_detail] if self.levels_of_detail is not None else []
        self.levels_of_detail = [v if isinstance(v, LevelOfDetail) else LevelOfDetail(v) for v in self.levels_of_detail]

        if not isinstance(self.height_source, list):
            self.height_source = [self.height_source] if self.height_source is not None else []
        self.height_source = [v if isinstance(v, HeightSource) else HeightSource(v) for v in self.height_source]

        if self.height_reference is not None and not isinstance(self.height_reference, HeightReference):
            self.height_reference = HeightReference(self.height_reference)

        if self.coordinate_reference_system is not None and not isinstance(self.coordinate_reference_system, str):
            self.coordinate_reference_system = str(self.coordinate_reference_system)

        if self.crs_linear_unit is not None and not isinstance(self.crs_linear_unit, str):
            self.crs_linear_unit = str(self.crs_linear_unit)

        if self.building_id_scheme is not None and not isinstance(self.building_id_scheme, str):
            self.building_id_scheme = str(self.building_id_scheme)

        if self.minimum_building_size is not None and not isinstance(self.minimum_building_size, str):
            self.minimum_building_size = str(self.minimum_building_size)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OperationProfile(CategoryProfile):
    """
    Occupancy, occupant behavior, schedules, setpoints and time use.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = UBEM_LINK["OperationProfile"]
    class_class_curie: ClassVar[str] = "ubem_link:OperationProfile"
    class_name: ClassVar[str] = "OperationProfile"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.OperationProfile

    behavior_types: Union[Union[str, "BehaviorType"], list[Union[str, "BehaviorType"]]] = None
    control_actions: Optional[Union[Union[str, "ControlAction"], list[Union[str, "ControlAction"]]]] = empty_list()
    collection_method: Optional[Union[Union[str, "CollectionMethod"], list[Union[str, "CollectionMethod"]]]] = empty_list()
    building_sectors: Optional[Union[Union[str, "BuildingSector"], list[Union[str, "BuildingSector"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.behavior_types):
            self.MissingRequiredField("behavior_types")
        if not isinstance(self.behavior_types, list):
            self.behavior_types = [self.behavior_types] if self.behavior_types is not None else []
        self.behavior_types = [v if isinstance(v, BehaviorType) else BehaviorType(v) for v in self.behavior_types]

        if not isinstance(self.control_actions, list):
            self.control_actions = [self.control_actions] if self.control_actions is not None else []
        self.control_actions = [v if isinstance(v, ControlAction) else ControlAction(v) for v in self.control_actions]

        if not isinstance(self.collection_method, list):
            self.collection_method = [self.collection_method] if self.collection_method is not None else []
        self.collection_method = [v if isinstance(v, CollectionMethod) else CollectionMethod(v) for v in self.collection_method]

        if not isinstance(self.building_sectors, list):
            self.building_sectors = [self.building_sectors] if self.building_sectors is not None else []
        self.building_sectors = [v if isinstance(v, BuildingSector) else BuildingSector(v) for v in self.building_sectors]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CharacteristicsProfile(CategoryProfile):
    """
    Non-geometric building characteristics (use type, vintage, envelope, systems, fuels) from surveys, administrative
    records, certificates and dictionaries.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = UBEM_LINK["CharacteristicsProfile"]
    class_class_curie: ClassVar[str] = "ubem_link:CharacteristicsProfile"
    class_name: ClassVar[str] = "CharacteristicsProfile"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.CharacteristicsProfile

    data_form: Union[Union[str, "DataForm"], list[Union[str, "DataForm"]]] = None
    building_sectors: Optional[Union[Union[str, "BuildingSector"], list[Union[str, "BuildingSector"]]]] = empty_list()
    representativeness: Optional[Union[str, "Representativeness"]] = None
    coverage_threshold: Optional[str] = None
    cross_tabulations: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.data_form):
            self.MissingRequiredField("data_form")
        if not isinstance(self.data_form, list):
            self.data_form = [self.data_form] if self.data_form is not None else []
        self.data_form = [v if isinstance(v, DataForm) else DataForm(v) for v in self.data_form]

        if not isinstance(self.building_sectors, list):
            self.building_sectors = [self.building_sectors] if self.building_sectors is not None else []
        self.building_sectors = [v if isinstance(v, BuildingSector) else BuildingSector(v) for v in self.building_sectors]

        if self.representativeness is not None and not isinstance(self.representativeness, Representativeness):
            self.representativeness = Representativeness(self.representativeness)

        if self.coverage_threshold is not None and not isinstance(self.coverage_threshold, str):
            self.coverage_threshold = str(self.coverage_threshold)

        if not isinstance(self.cross_tabulations, list):
            self.cross_tabulations = [self.cross_tabulations] if self.cross_tabulations is not None else []
        self.cross_tabulations = [v if isinstance(v, str) else str(v) for v in self.cross_tabulations]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EnergyProfile(CategoryProfile):
    """
    Measured or reported energy use for calibration and validation, from national balances (macroscopic) to buildings,
    meters and appliances (microscopic).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = UBEM_LINK["EnergyProfile"]
    class_class_curie: ClassVar[str] = "ubem_link:EnergyProfile"
    class_name: ClassVar[str] = "EnergyProfile"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.EnergyProfile

    energy_data_scale: Union[str, "EnergyDataScale"] = None
    energy_sectors: Optional[Union[Union[str, "EnergySector"], list[Union[str, "EnergySector"]]]] = empty_list()
    energy_carriers: Optional[Union[Union[str, "EnergyCarrier"], list[Union[str, "EnergyCarrier"]]]] = empty_list()
    energy_metrics: Optional[Union[Union[str, "EnergyMetric"], list[Union[str, "EnergyMetric"]]]] = empty_list()
    metering_level: Optional[Union[str, "MeteringLevel"]] = None
    measurement_basis: Optional[Union[str, "MeasurementBasis"]] = None
    weather_normalized_available: Optional[Union[bool, Bool]] = None
    reporting_period: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.energy_data_scale):
            self.MissingRequiredField("energy_data_scale")
        if not isinstance(self.energy_data_scale, EnergyDataScale):
            self.energy_data_scale = EnergyDataScale(self.energy_data_scale)

        if not isinstance(self.energy_sectors, list):
            self.energy_sectors = [self.energy_sectors] if self.energy_sectors is not None else []
        self.energy_sectors = [v if isinstance(v, EnergySector) else EnergySector(v) for v in self.energy_sectors]

        if not isinstance(self.energy_carriers, list):
            self.energy_carriers = [self.energy_carriers] if self.energy_carriers is not None else []
        self.energy_carriers = [v if isinstance(v, EnergyCarrier) else EnergyCarrier(v) for v in self.energy_carriers]

        if not isinstance(self.energy_metrics, list):
            self.energy_metrics = [self.energy_metrics] if self.energy_metrics is not None else []
        self.energy_metrics = [v if isinstance(v, EnergyMetric) else EnergyMetric(v) for v in self.energy_metrics]

        if self.metering_level is not None and not isinstance(self.metering_level, MeteringLevel):
            self.metering_level = MeteringLevel(self.metering_level)

        if self.measurement_basis is not None and not isinstance(self.measurement_basis, MeasurementBasis):
            self.measurement_basis = MeasurementBasis(self.measurement_basis)

        if self.weather_normalized_available is not None and not isinstance(self.weather_normalized_available, Bool):
            self.weather_normalized_available = Bool(self.weather_normalized_available)

        if self.reporting_period is not None and not isinstance(self.reporting_period, str):
            self.reporting_period = str(self.reporting_period)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SimulationProfile(CategoryProfile):
    """
    Reference simulations and model libraries: synthetic building-stock outputs and prototype models.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = UBEM_LINK["SimulationProfile"]
    class_class_curie: ClassVar[str] = "ubem_link:SimulationProfile"
    class_name: ClassVar[str] = "SimulationProfile"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.SimulationProfile

    simulation_engine: Optional[str] = None
    stock_representation: Optional[Union[str, "StockRepresentation"]] = None
    weather_basis: Optional[str] = None
    building_sectors: Optional[Union[Union[str, "BuildingSector"], list[Union[str, "BuildingSector"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.simulation_engine is not None and not isinstance(self.simulation_engine, str):
            self.simulation_engine = str(self.simulation_engine)

        if self.stock_representation is not None and not isinstance(self.stock_representation, StockRepresentation):
            self.stock_representation = StockRepresentation(self.stock_representation)

        if self.weather_basis is not None and not isinstance(self.weather_basis, str):
            self.weather_basis = str(self.weather_basis)

        if not isinstance(self.building_sectors, list):
            self.building_sectors = [self.building_sectors] if self.building_sectors is not None else []
        self.building_sectors = [v if isinstance(v, BuildingSector) else BuildingSector(v) for v in self.building_sectors]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContextProfile(CategoryProfile):
    """
    Context and coupling data: socio-economic data, land use, grid emissions, tariffs and urban climate.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = UBEM_LINK["ContextProfile"]
    class_class_curie: ClassVar[str] = "ubem_link:ContextProfile"
    class_name: ClassVar[str] = "ContextProfile"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.ContextProfile

    context_kind: Optional[Union[Union[str, "ContextKind"], list[Union[str, "ContextKind"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.context_kind, list):
            self.context_kind = [self.context_kind] if self.context_kind is not None else []
        self.context_kind = [v if isinstance(v, ContextKind) else ContextKind(v) for v in self.context_kind]

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
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.VariableProfile

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
    is_replicate_weight: Optional[Union[bool, Bool]] = None
    is_imputation_flag: Optional[Union[bool, Bool]] = None
    flags_variable: Optional[str] = None
    join_key: Optional[Union[str, "JoinKey"]] = None
    do_not_use: Optional[Union[bool, Bool]] = None
    profiled_by: Optional[str] = None
    confidence: Optional[float] = None
    review_flags: Optional[Union[str, list[str]]] = empty_list()

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

        if self.is_replicate_weight is not None and not isinstance(self.is_replicate_weight, Bool):
            self.is_replicate_weight = Bool(self.is_replicate_weight)

        if self.is_imputation_flag is not None and not isinstance(self.is_imputation_flag, Bool):
            self.is_imputation_flag = Bool(self.is_imputation_flag)

        if self.flags_variable is not None and not isinstance(self.flags_variable, str):
            self.flags_variable = str(self.flags_variable)

        if self.join_key is not None and not isinstance(self.join_key, JoinKey):
            self.join_key = JoinKey(self.join_key)

        if self.do_not_use is not None and not isinstance(self.do_not_use, Bool):
            self.do_not_use = Bool(self.do_not_use)

        if self.profiled_by is not None and not isinstance(self.profiled_by, str):
            self.profiled_by = str(self.profiled_by)

        if self.confidence is not None and not isinstance(self.confidence, float):
            self.confidence = float(self.confidence)

        if not isinstance(self.review_flags, list):
            self.review_flags = [self.review_flags] if self.review_flags is not None else []
        self.review_flags = [v if isinstance(v, str) else str(v) for v in self.review_flags]

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
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.CodeEntry

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
    A concept in the UBEM-Link vocabulary: a quantity or attribute that a UBEM workflow consumes or produces (for
    example floor area, principal building activity, dry-bulb temperature, annual electricity use). Concepts form a
    hierarchy through `broader` and point to equivalent terms in other standards.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["Concept"]
    class_class_curie: ClassVar[str] = "skos:Concept"
    class_name: ClassVar[str] = "UBEMConcept"
    class_model_uri: ClassVar[URIRef] = UBEM_LINK.UBEMConcept

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
    """
    Extent of the area a dataset covers.
    """
    multinational = PermissibleValue(
        text="multinational",
        description="Covers several countries, such as the European Union.")
    national = PermissibleValue(
        text="national",
        description="Covers one country.")
    subnational = PermissibleValue(
        text="subnational",
        description="Covers part of a country, such as a state, province or utility territory.")
    city = PermissibleValue(
        text="city",
        description="Covers one city or metropolitan area.")

    _defn = EnumDefinition(
        name="GeographicScope",
        description="Extent of the area a dataset covers.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "global",
            PermissibleValue(
                text="global",
                description="Covers (nearly) the whole world."))

class SpatialGranularity(EnumDefinitionImpl):
    """
    Ordered from finest to coarsest (see `rank` annotation).
    """
    point_station = PermissibleValue(
        text="point_station",
        description="Individual measurement points such as weather stations.")
    building = PermissibleValue(
        text="building",
        description="Individual buildings or footprints.")
    parcel = PermissibleValue(
        text="parcel",
        description="Individual land parcels or lots.")
    grid_cell_fine = PermissibleValue(
        text="grid_cell_fine",
        description="Raster or model grid cells of 1 km or finer.")
    census_block_group = PermissibleValue(
        text="census_block_group",
        description="U.S. census block groups (about 600 to 3,000 people).")
    census_tract = PermissibleValue(
        text="census_tract",
        description="U.S. census tracts (about 4,000 people).")
    postal_code = PermissibleValue(
        text="postal_code",
        description="Postal or ZIP codes.")
    grid_cell_coarse = PermissibleValue(
        text="grid_cell_coarse",
        description="Raster or model grid cells coarser than 1 km.")
    county = PermissibleValue(
        text="county",
        description="Counties or equivalent second-level administrative units.")
    city = PermissibleValue(
        text="city",
        description="Cities or municipalities.")
    utility_service_territory = PermissibleValue(
        text="utility_service_territory",
        description="Service territories of electric or gas utilities.")
    state_province = PermissibleValue(
        text="state_province",
        description="States, provinces or equivalent first-level administrative units.")
    climate_zone = PermissibleValue(
        text="climate_zone",
        description="Climate zones (for example ASHRAE or IECC zones).")
    census_region_division = PermissibleValue(
        text="census_region_division",
        description="U.S. census regions or divisions.")
    nation = PermissibleValue(
        text="nation",
        description="Whole countries, with no finer location.")
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
    """
    How the data were generated; decides the statistical treatment they need.
    """
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
        description="How the data were generated; decides the statistical treatment they need.",
    )

class AccessLevel(EnumDefinitionImpl):
    """
    How the data can be obtained.
    """
    open_download = PermissibleValue(
        text="open_download",
        description="Files can be downloaded by anyone without registration.")
    open_api = PermissibleValue(
        text="open_api",
        description="Data can be retrieved by anyone through an open programmatic interface.")
    registration_required = PermissibleValue(
        text="registration_required",
        description="Free, but users must register or sign in.")
    request_or_agreement = PermissibleValue(
        text="request_or_agreement",
        description="Access requires an application, a data-use agreement or approval.")
    restricted_commercial = PermissibleValue(
        text="restricted_commercial",
        description="Access requires payment or is restricted to specific users.")

    _defn = EnumDefinition(
        name="AccessLevel",
        description="How the data can be obtained.",
    )

class JoinKey(EnumDefinitionImpl):
    """
    Keys in the public data through which records can be linked to other datasets.
    """
    lat_lon = PermissibleValue(
        text="lat_lon",
        description="Latitude and longitude of the record.")
    geometry = PermissibleValue(
        text="geometry",
        description="A point, line or polygon geometry of the record.")
    address = PermissibleValue(
        text="address",
        description="Street address of the building or site.")
    parcel_id = PermissibleValue(
        text="parcel_id",
        description="Cadastral parcel or lot identifier shared with other datasets (for example BBL).")
    building_id = PermissibleValue(
        text="building_id",
        description="""Building identifier shared with other datasets (for example BIN, UPRN); not a dataset-internal row id.""")
    ubid = PermissibleValue(
        text="ubid",
        description="Unique Building Identifier derived from the footprint.")
    station_id = PermissibleValue(
        text="station_id",
        description="Identifier of a weather or measurement station (for example WMO or USAF id).")
    grid_cell = PermissibleValue(
        text="grid_cell",
        description="Identifier or coordinates of a raster or grid cell.")
    census_block_group = PermissibleValue(
        text="census_block_group",
        description="U.S. census block group code.")
    census_tract = PermissibleValue(
        text="census_tract",
        description="U.S. census tract code.")
    small_statistical_area = PermissibleValue(
        text="small_statistical_area",
        description="Non-U.S. small statistical areas such as UK LSOA/MSOA or national census grid ids")
    postal_code = PermissibleValue(
        text="postal_code",
        description="Postal or ZIP code.")
    fips_county = PermissibleValue(
        text="fips_county",
        description="U.S. FIPS county code.")
    fips_state = PermissibleValue(
        text="fips_state",
        description="U.S. FIPS state code.")
    census_region_division = PermissibleValue(
        text="census_region_division",
        description="U.S. census region or division code.")
    nuts_region = PermissibleValue(
        text="nuts_region",
        description="European NUTS region code.")
    country_iso = PermissibleValue(
        text="country_iso",
        description="ISO 3166 country code.")
    utility_id = PermissibleValue(
        text="utility_id",
        description="Identifier of an electric or gas utility (for example EIA utility id).")
    balancing_authority = PermissibleValue(
        text="balancing_authority",
        description="Identifier of an electricity balancing authority.")
    climate_zone_ashrae = PermissibleValue(
        text="climate_zone_ashrae",
        description="ASHRAE Standard 169 climate zone.")
    climate_zone_iecc = PermissibleValue(
        text="climate_zone_iecc",
        description="IECC climate zone.")
    building_type = PermissibleValue(
        text="building_type",
        description="Building type or use class (attribute key for statistical matching only).")
    vintage = PermissibleValue(
        text="vintage",
        description="Construction period (attribute key for statistical matching only).")
    timestamp = PermissibleValue(
        text="timestamp",
        description="Date and time of an observation.")

    _defn = EnumDefinition(
        name="JoinKey",
        description="Keys in the public data through which records can be linked to other datasets.",
    )

class VariableDatatype(EnumDefinitionImpl):
    """
    Data type of a variable's values.
    """
    integer = PermissibleValue(
        text="integer",
        description="Whole numbers, such as counts or years.")
    float = PermissibleValue(
        text="float",
        description="Real numbers that may have decimals.")
    string = PermissibleValue(
        text="string",
        description="Free text without a code list.")
    categorical = PermissibleValue(
        text="categorical",
        description="Codes from a fixed list (see code_list).")
    boolean = PermissibleValue(
        text="boolean",
        description="True or false.")
    datetime = PermissibleValue(
        text="datetime",
        description="Dates or date-times (ISO 8601).")
    geometry = PermissibleValue(
        text="geometry",
        description="Spatial geometries such as points, lines or polygons.")
    identifier = PermissibleValue(
        text="identifier",
        description="Identifiers of records or entities.")

    _defn = EnumDefinition(
        name="VariableDatatype",
        description="Data type of a variable's values.",
    )

class MappingRelation(EnumDefinitionImpl):
    """
    SKOS mapping relation between a variable and a concept.
    """
    exactMatch = PermissibleValue(
        text="exactMatch",
        description="The variable measures exactly the concept.",
        meaning=SKOS["exactMatch"])
    closeMatch = PermissibleValue(
        text="closeMatch",
        description="The variable measures nearly the concept and can be used in its place in most applications.",
        meaning=SKOS["closeMatch"])
    broadMatch = PermissibleValue(
        text="broadMatch",
        description="The concept is more general than the variable.",
        meaning=SKOS["broadMatch"])
    narrowMatch = PermissibleValue(
        text="narrowMatch",
        description="The concept is more specific than the variable.",
        meaning=SKOS["narrowMatch"])
    relatedMatch = PermissibleValue(
        text="relatedMatch",
        description="The variable is associated with the concept but does not measure it.",
        meaning=SKOS["relatedMatch"])

    _defn = EnumDefinition(
        name="MappingRelation",
        description="SKOS mapping relation between a variable and a concept.",
    )

class Aggregation(EnumDefinitionImpl):
    """
    How a value relates to time.
    """
    static = PermissibleValue(
        text="static",
        description="Attribute that does not vary in the observation period.")
    instantaneous = PermissibleValue(
        text="instantaneous",
        description="Value at a point in time (for example a temperature reading).")
    total_over_period = PermissibleValue(
        text="total_over_period",
        description="Sum over the reporting period (for example annual energy use).")
    average_over_period = PermissibleValue(
        text="average_over_period",
        description="Mean over the reporting period.")
    count = PermissibleValue(
        text="count",
        description="Number of items (for example number of floors or occupants).")
    share = PermissibleValue(
        text="share",
        description="Fraction or percentage of a whole.")

    _defn = EnumDefinition(
        name="Aggregation",
        description="How a value relates to time.",
    )

class EntityType(EnumDefinitionImpl):
    """
    What a concept or variable describes.
    """
    site = PermissibleValue(
        text="site",
        description="A property or campus that may contain several buildings.")
    building = PermissibleValue(
        text="building",
        description="A single building.")
    zone = PermissibleValue(
        text="zone",
        description="A thermal zone or space within a building.")
    system = PermissibleValue(
        text="system",
        description="A building system or piece of equipment (HVAC, water heating, lighting, ...).")
    envelope = PermissibleValue(
        text="envelope",
        description="Walls, roofs, windows and other parts of the building envelope.")
    household = PermissibleValue(
        text="household",
        description="A household occupying a housing unit.")
    occupant = PermissibleValue(
        text="occupant",
        description="A person using a building.")
    meter = PermissibleValue(
        text="meter",
        description="An energy or water meter.")
    region = PermissibleValue(
        text="region",
        description="A geographic area.")
    weather_station = PermissibleValue(
        text="weather_station",
        description="A weather or climate observation station.")
    grid_cell = PermissibleValue(
        text="grid_cell",
        description="A cell of a raster or model grid.")
    dataset_record = PermissibleValue(
        text="dataset_record",
        description="Record bookkeeping (identifiers, weights, flags).")

    _defn = EnumDefinition(
        name="EntityType",
        description="What a concept or variable describes.",
    )

class WeatherYearType(EnumDefinitionImpl):
    """
    Kind of weather year or weather series.
    """
    actual_series = PermissibleValue(
        text="actual_series",
        description="Observed or reanalysis time series of actual weather over one or more years.")
    actual_meteorological_year = PermissibleValue(
        text="actual_meteorological_year",
        description="Simulation-ready file of one actual year (AMY).")
    typical_meteorological_year = PermissibleValue(
        text="typical_meteorological_year",
        description="Typical year assembled from months of several years (TMY, TMYx, IWEC).")
    climate_normals = PermissibleValue(
        text="climate_normals",
        description="Long-term averages such as 30-year normals.")
    future_typical_year = PermissibleValue(
        text="future_typical_year",
        description="Typical year for a future period, morphed or downscaled from climate models.")
    projection_series = PermissibleValue(
        text="projection_series",
        description="Time series from climate model projections.")
    design_conditions = PermissibleValue(
        text="design_conditions",
        description="Design-day statistics for sizing equipment.")

    _defn = EnumDefinition(
        name="WeatherYearType",
        description="Kind of weather year or weather series.",
    )

class WeatherFileFormat(EnumDefinitionImpl):
    """
    Format of released weather data.
    """
    epw = PermissibleValue(
        text="epw",
        description="EnergyPlus weather file, readable by most simulation engines.")
    tmy3_csv = PermissibleValue(
        text="tmy3_csv",
        description="TMY3 comma-separated format.")
    netcdf = PermissibleValue(
        text="netcdf",
        description="NetCDF gridded files.")
    grib = PermissibleValue(
        text="grib",
        description="GRIB gridded files.")
    csv = PermissibleValue(
        text="csv",
        description="Other tabular text files.")
    api_json = PermissibleValue(
        text="api_json",
        description="Responses of a web API in JSON.")
    other = PermissibleValue(
        text="other",
        description="Another format not listed here.")

    _defn = EnumDefinition(
        name="WeatherFileFormat",
        description="Format of released weather data.",
    )

class TimestampConvention(EnumDefinitionImpl):
    """
    What a timestamp marks within its interval.
    """
    interval_ending = PermissibleValue(
        text="interval_ending",
        description="The timestamp is the end of the interval (EPW hour 1 covers 00:00 to 01:00).")
    interval_beginning = PermissibleValue(
        text="interval_beginning",
        description="The timestamp is the start of the interval.")
    instantaneous = PermissibleValue(
        text="instantaneous",
        description="The value was observed at the timestamp.")
    unknown = PermissibleValue(
        text="unknown",
        description="Not stated by the publisher.")

    _defn = EnumDefinition(
        name="TimestampConvention",
        description="What a timestamp marks within its interval.",
    )

class TimeBasis(EnumDefinitionImpl):
    """
    Clock to which timestamps refer.
    """
    utc = PermissibleValue(
        text="utc",
        description="Coordinated Universal Time.")
    local_standard_time = PermissibleValue(
        text="local_standard_time",
        description="Local standard time without daylight saving (as in EPW files).")
    local_time_with_dst = PermissibleValue(
        text="local_time_with_dst",
        description="Local civil time including daylight saving.")
    unknown = PermissibleValue(
        text="unknown",
        description="Not stated by the publisher.")

    _defn = EnumDefinition(
        name="TimeBasis",
        description="Clock to which timestamps refer.",
    )

class GapFilling(EnumDefinitionImpl):
    """
    How missing or sub-interval values were filled.
    """
    none = PermissibleValue(
        text="none",
        description="Gaps are left as missing values.")
    linear_interpolation = PermissibleValue(
        text="linear_interpolation",
        description="Gaps filled by linear interpolation in time.")
    model_based = PermissibleValue(
        text="model_based",
        description="Gaps filled from a model, reanalysis or neighboring stations.")
    unknown = PermissibleValue(
        text="unknown",
        description="Not stated by the publisher.")

    _defn = EnumDefinition(
        name="GapFilling",
        description="How missing or sub-interval values were filled.",
    )

class GeometryDimension(EnumDefinitionImpl):
    """
    Geometric representation of buildings.
    """
    point = PermissibleValue(
        text="point",
        description="Building locations as points only.")
    footprint_2d = PermissibleValue(
        text="footprint_2d",
        description="Building outlines without height.")
    footprint_with_height = PermissibleValue(
        text="footprint_with_height",
        description="Building outlines with a height attribute (2.5D, extrudable to CityGML LoD1).")
    solid_3d = PermissibleValue(
        text="solid_3d",
        description="Three-dimensional building solids or surfaces (CityGML LoD1 or higher).")
    raster = PermissibleValue(
        text="raster",
        description="Gridded built-up surface, volume or height.")
    parcel_polygon = PermissibleValue(
        text="parcel_polygon",
        description="Parcel or lot outlines, not buildings.")

    _defn = EnumDefinition(
        name="GeometryDimension",
        description="Geometric representation of buildings.",
    )

class LevelOfDetail(EnumDefinitionImpl):
    """
    CityGML level of detail.
    """
    lod0 = PermissibleValue(
        text="lod0",
        description="Footprint or roof-edge polygon.")
    lod1 = PermissibleValue(
        text="lod1",
        description="Block model: footprint extruded to one height.")
    lod2 = PermissibleValue(
        text="lod2",
        description="Roof shapes and wall surfaces.")
    lod3 = PermissibleValue(
        text="lod3",
        description="Architectural model with openings such as windows and doors.")
    lod4 = PermissibleValue(
        text="lod4",
        description="Interior structures (CityGML 2.0 only).")

    _defn = EnumDefinition(
        name="LevelOfDetail",
        description="CityGML level of detail.",
    )

class HeightSource(EnumDefinitionImpl):
    """
    How building heights were obtained.
    """
    lidar = PermissibleValue(
        text="lidar",
        description="Measured from airborne laser scanning.")
    photogrammetry = PermissibleValue(
        text="photogrammetry",
        description="Measured from stereo or oblique imagery.")
    plans_or_records = PermissibleValue(
        text="plans_or_records",
        description="Taken from building plans or administrative records.")
    model_estimated = PermissibleValue(
        text="model_estimated",
        description="Estimated by a statistical or machine-learning model.")
    derived_from_floors = PermissibleValue(
        text="derived_from_floors",
        description="Computed from the number of floors and an assumed floor height.")
    none = PermissibleValue(
        text="none",
        description="The dataset has no building heights.")

    _defn = EnumDefinition(
        name="HeightSource",
        description="How building heights were obtained.",
    )

class HeightReference(EnumDefinitionImpl):
    """
    Reference points of a building height.
    """
    ground_to_roof_top = PermissibleValue(
        text="ground_to_roof_top",
        description="From ground level to the highest point of the roof.")
    ground_to_eave = PermissibleValue(
        text="ground_to_eave",
        description="From ground level to the eave.")
    ground_to_mean_roof = PermissibleValue(
        text="ground_to_mean_roof",
        description="From ground level to the mean roof height.")
    above_sea_level = PermissibleValue(
        text="above_sea_level",
        description="Elevation above a vertical datum, not a building height.")
    unknown = PermissibleValue(
        text="unknown",
        description="Not stated by the publisher.")

    _defn = EnumDefinition(
        name="HeightReference",
        description="Reference points of a building height.",
    )

class BehaviorType(EnumDefinitionImpl):
    """
    Kind of occupant behavior or building operation.
    """
    occupancy_presence = PermissibleValue(
        text="occupancy_presence",
        description="Whether or how many people are present.")
    hvac_operation = PermissibleValue(
        text="hvac_operation",
        description="Operation of heating, cooling or ventilation.")
    thermostat_setpoint = PermissibleValue(
        text="thermostat_setpoint",
        description="Setpoints and their changes.")
    window_operation = PermissibleValue(
        text="window_operation",
        description="Opening and closing windows.")
    lighting_operation = PermissibleValue(
        text="lighting_operation",
        description="Switching or dimming lights.")
    appliance_plug_loads = PermissibleValue(
        text="appliance_plug_loads",
        description="Use of appliances and plug loads.")
    hot_water_use = PermissibleValue(
        text="hot_water_use",
        description="Domestic hot water draws.")
    thermal_comfort = PermissibleValue(
        text="thermal_comfort",
        description="Thermal sensation, preference or acceptability votes.")
    time_use_activities = PermissibleValue(
        text="time_use_activities",
        description="Activities of people over the day (time-use diaries).")
    mobility = PermissibleValue(
        text="mobility",
        description="Travel and location over the day.")

    _defn = EnumDefinition(
        name="BehaviorType",
        description="Kind of occupant behavior or building operation.",
    )

class ControlAction(EnumDefinitionImpl):
    """
    Occupant control action.
    """
    thermostat_adjustment = PermissibleValue(
        text="thermostat_adjustment",
        description="Changing a thermostat setpoint.")
    hvac_on_off = PermissibleValue(
        text="hvac_on_off",
        description="Switching heating, cooling or fans.")
    lighting_on_off = PermissibleValue(
        text="lighting_on_off",
        description="Switching or dimming lights.")
    window_open_close = PermissibleValue(
        text="window_open_close",
        description="Opening or closing a window.")
    shading_adjustment = PermissibleValue(
        text="shading_adjustment",
        description="Moving blinds or shades.")
    appliance_on_off = PermissibleValue(
        text="appliance_on_off",
        description="Switching an appliance.")

    _defn = EnumDefinition(
        name="ControlAction",
        description="Occupant control action.",
    )

class CollectionMethod(EnumDefinitionImpl):
    """
    How behavior or operation data were collected.
    """
    sensors_or_logs = PermissibleValue(
        text="sensors_or_logs",
        description="Sensors, building automation logs or meters.")
    connected_devices = PermissibleValue(
        text="connected_devices",
        description="Smart thermostats or other connected devices.")
    survey_or_diary = PermissibleValue(
        text="survey_or_diary",
        description="Questionnaires or time-use diaries.")
    field_study_compilation = PermissibleValue(
        text="field_study_compilation",
        description="Compilation of separate field studies.")
    mobile_location = PermissibleValue(
        text="mobile_location",
        description="Mobile phone or other location traces.")

    _defn = EnumDefinition(
        name="CollectionMethod",
        description="How behavior or operation data were collected.",
    )

class BuildingSector(EnumDefinitionImpl):
    """
    Building sector.
    """
    residential = PermissibleValue(
        text="residential",
        description="Dwellings and residential buildings.")
    commercial = PermissibleValue(
        text="commercial",
        description="Commercial, public and institutional buildings.")
    industrial = PermissibleValue(
        text="industrial",
        description="Industrial and manufacturing buildings.")
    all = PermissibleValue(
        text="all",
        description="All building sectors.")

    _defn = EnumDefinition(
        name="BuildingSector",
        description="Building sector.",
    )

class DataForm(EnumDefinitionImpl):
    """
    Form in which characteristics are released.
    """
    microdata = PermissibleValue(
        text="microdata",
        description="One record per sampled unit (building or household), usually with weights.")
    building_records = PermissibleValue(
        text="building_records",
        description="One record per identified real building or property (certificates, benchmarking, permits).")
    aggregate_tables = PermissibleValue(
        text="aggregate_tables",
        description="Published distributions or totals, not records of units.")
    dictionary_or_standard = PermissibleValue(
        text="dictionary_or_standard",
        description="A data dictionary, standard or exchange schema, not data.")
    archetype_library = PermissibleValue(
        text="archetype_library",
        description="Typical buildings or model templates by type and vintage.")

    _defn = EnumDefinition(
        name="DataForm",
        description="Form in which characteristics are released.",
    )

class Representativeness(EnumDefinitionImpl):
    """
    How the covered buildings relate to the building stock.
    """
    probability_sample = PermissibleValue(
        text="probability_sample",
        description="A probability sample; weighted estimates represent the stock.")
    complete_population = PermissibleValue(
        text="complete_population",
        description="All buildings of the area.")
    mandated_subset = PermissibleValue(
        text="mandated_subset",
        description="Buildings covered by a mandate (for example above a size threshold).")
    voluntary_or_convenience = PermissibleValue(
        text="voluntary_or_convenience",
        description="Buildings that chose to participate or were available.")
    synthetic = PermissibleValue(
        text="synthetic",
        description="Modeled or typical buildings, not real ones.")
    unknown = PermissibleValue(
        text="unknown",
        description="Not stated by the publisher.")

    _defn = EnumDefinition(
        name="Representativeness",
        description="How the covered buildings relate to the building stock.",
    )

class EnergyDataScale(EnumDefinitionImpl):
    """
    Scale of energy data.
    """
    macroscopic = PermissibleValue(
        text="macroscopic",
        description="Aggregates over many buildings (national, state, utility or area totals).")
    microscopic = PermissibleValue(
        text="microscopic",
        description="Individual buildings, meters, circuits or appliances.")

    _defn = EnumDefinition(
        name="EnergyDataScale",
        description="Scale of energy data.",
    )

class EnergySector(EnumDefinitionImpl):
    """
    Energy-using sector.
    """
    residential = PermissibleValue(
        text="residential",
        description="Households and residential buildings.")
    commercial = PermissibleValue(
        text="commercial",
        description="Commercial and public buildings.")
    industrial = PermissibleValue(
        text="industrial",
        description="Industry and manufacturing.")
    transportation = PermissibleValue(
        text="transportation",
        description="Transportation of people and goods.")
    all = PermissibleValue(
        text="all",
        description="All sectors or the whole economy.")

    _defn = EnumDefinition(
        name="EnergySector",
        description="Energy-using sector.",
    )

class EnergyCarrier(EnumDefinitionImpl):
    """
    Energy carrier.
    """
    electricity = PermissibleValue(
        text="electricity",
        description="Electricity from the grid.")
    natural_gas = PermissibleValue(
        text="natural_gas",
        description="Natural gas from a pipeline network.")
    fuel_oil = PermissibleValue(
        text="fuel_oil",
        description="Fuel oil and other petroleum liquids.")
    propane = PermissibleValue(
        text="propane",
        description="Propane and liquefied petroleum gas.")
    district_energy = PermissibleValue(
        text="district_energy",
        description="District steam, hot water or chilled water.")
    biomass = PermissibleValue(
        text="biomass",
        description="Wood and other biomass.")
    onsite_renewables = PermissibleValue(
        text="onsite_renewables",
        description="Energy generated on site, such as rooftop solar.")
    all_carriers = PermissibleValue(
        text="all_carriers",
        description="Totals over all carriers only.")

    _defn = EnumDefinition(
        name="EnergyCarrier",
        description="Energy carrier.",
    )

class EnergyMetric(EnumDefinitionImpl):
    """
    Kind of energy quantity.
    """
    site_energy = PermissibleValue(
        text="site_energy",
        description="Energy delivered to the site.")
    source_energy = PermissibleValue(
        text="source_energy",
        description="Site energy plus upstream generation and delivery losses.")
    primary_energy = PermissibleValue(
        text="primary_energy",
        description="Primary energy as defined in national statistics.")
    end_use_energy = PermissibleValue(
        text="end_use_energy",
        description="Energy by end use (heating, cooling, lighting, ...).")
    load_profile = PermissibleValue(
        text="load_profile",
        description="Time series of demand.")
    peak_demand = PermissibleValue(
        text="peak_demand",
        description="Maximum demand over a period.")
    emissions = PermissibleValue(
        text="emissions",
        description="Greenhouse gas emissions.")
    expenditure = PermissibleValue(
        text="expenditure",
        description="Cost of the energy used.")

    _defn = EnumDefinition(
        name="EnergyMetric",
        description="Kind of energy quantity.",
    )

class MeteringLevel(EnumDefinitionImpl):
    """
    Finest level at which energy is measured or reported.
    """
    area_aggregate = PermissibleValue(
        text="area_aggregate",
        description="Totals over an area or sector.")
    utility_territory = PermissibleValue(
        text="utility_territory",
        description="Totals over a utility service territory or balancing authority.")
    whole_building = PermissibleValue(
        text="whole_building",
        description="One value per building or property.")
    submeter_end_use = PermissibleValue(
        text="submeter_end_use",
        description="Submeters or end uses within a building.")
    circuit_or_appliance = PermissibleValue(
        text="circuit_or_appliance",
        description="Circuits or individual appliances.")

    _defn = EnumDefinition(
        name="MeteringLevel",
        description="Finest level at which energy is measured or reported.",
    )

class MeasurementBasis(EnumDefinitionImpl):
    """
    How energy values were obtained.
    """
    metered = PermissibleValue(
        text="metered",
        description="Measured by meters at the stated resolution.")
    billed = PermissibleValue(
        text="billed",
        description="From utility bills or supplier records.")
    self_reported = PermissibleValue(
        text="self_reported",
        description="Reported by owners or respondents (for example through benchmarking software).")
    modeled_or_estimated = PermissibleValue(
        text="modeled_or_estimated",
        description="Estimated by models, imputation or engineering calculation.")
    mixed = PermissibleValue(
        text="mixed",
        description="A combination of the above.")

    _defn = EnumDefinition(
        name="MeasurementBasis",
        description="How energy values were obtained.",
    )

class StockRepresentation(EnumDefinitionImpl):
    """
    How a simulated building stock is represented.
    """
    sampled_models = PermissibleValue(
        text="sampled_models",
        description="A statistical sample of building models weighted to the stock.")
    building_by_building = PermissibleValue(
        text="building_by_building",
        description="One model per real building.")
    prototype_library = PermissibleValue(
        text="prototype_library",
        description="Typical or prototype buildings by type, vintage and climate.")

    _defn = EnumDefinition(
        name="StockRepresentation",
        description="How a simulated building stock is represented.",
    )

class ContextKind(EnumDefinitionImpl):
    """
    Kind of context or coupling data.
    """
    grid_emissions = PermissibleValue(
        text="grid_emissions",
        description="Emission factors of electricity supply.")
    energy_tariffs = PermissibleValue(
        text="energy_tariffs",
        description="Energy prices and tariffs.")
    land_use = PermissibleValue(
        text="land_use",
        description="Land use and zoning.")
    socio_economic = PermissibleValue(
        text="socio_economic",
        description="Population, income and housing statistics.")
    urban_climate_zones = PermissibleValue(
        text="urban_climate_zones",
        description="Local climate zones and urban form classes.")

    _defn = EnumDefinition(
        name="ContextKind",
        description="Kind of context or coupling data.",
    )

class ConventionType(EnumDefinitionImpl):
    """
    What a dataset convention concerns.
    """
    missing_code = PermissibleValue(
        text="missing_code",
        description="Codes that mean missing, not applicable, withheld or unknown.")
    unit = PermissibleValue(
        text="unit",
        description="The unit and multiplier of values.")
    top_or_bottom_code = PermissibleValue(
        text="top_or_bottom_code",
        description="Codes that stand for ranges at the end of a scale.")
    imputation_flag = PermissibleValue(
        text="imputation_flag",
        description="How imputation flags are named and linked to their variables.")
    weight = PermissibleValue(
        text="weight",
        description="How weights are named and used.")
    identifier_format = PermissibleValue(
        text="identifier_format",
        description="How identifiers and keys are written.")
    do_not_use = PermissibleValue(
        text="do_not_use",
        description="A field the publisher says must not be used, or not for some purpose.")
    definition = PermissibleValue(
        text="definition",
        description="What a field includes or excludes.")

    _defn = EnumDefinition(
        name="ConventionType",
        description="What a dataset convention concerns.",
    )

# Slots
class slots:
    pass

slots.datasets = Slot(uri=UBEM_LINK.datasets, name="datasets", curie=UBEM_LINK.curie('datasets'),
                   model_uri=UBEM_LINK.datasets, domain=None, range=Optional[Union[dict[Union[str, DatasetProfileId], Union[dict, DatasetProfile]], list[Union[dict, DatasetProfile]]]])

slots.concepts = Slot(uri=UBEM_LINK.concepts, name="concepts", curie=UBEM_LINK.curie('concepts'),
                   model_uri=UBEM_LINK.concepts, domain=None, range=Optional[Union[dict[Union[str, UBEMConceptId], Union[dict, UBEMConcept]], list[Union[dict, UBEMConcept]]]])

slots.id = Slot(uri=UBEM_LINK.id, name="id", curie=UBEM_LINK.curie('id'),
                   model_uri=UBEM_LINK.id, domain=None, range=URIRef,
                   pattern=re.compile(r'^[a-z0-9][a-z0-9_.-]*$'))

slots.title = Slot(uri=DCT.title, name="title", curie=DCT.curie('title'),
                   model_uri=UBEM_LINK.title, domain=None, range=Optional[str])

slots.short_name = Slot(uri=SKOS.altLabel, name="short_name", curie=SKOS.curie('altLabel'),
                   model_uri=UBEM_LINK.short_name, domain=None, range=Optional[str])

slots.publisher = Slot(uri=DCT.publisher, name="publisher", curie=DCT.curie('publisher'),
                   model_uri=UBEM_LINK.publisher, domain=None, range=Optional[str])

slots.landing_page = Slot(uri=DCAT.landingPage, name="landing_page", curie=DCAT.curie('landingPage'),
                   model_uri=UBEM_LINK.landing_page, domain=None, range=Optional[Union[str, URI]])

slots.doi = Slot(uri=UBEM_LINK.doi, name="doi", curie=UBEM_LINK.curie('doi'),
                   model_uri=UBEM_LINK.doi, domain=None, range=Optional[str],
                   pattern=re.compile(r'^10\.\d{4,9}/\S+$'))

slots.citation = Slot(uri=DCT.bibliographicCitation, name="citation", curie=DCT.curie('bibliographicCitation'),
                   model_uri=UBEM_LINK.citation, domain=None, range=Optional[str])

slots.reference_paper_doi = Slot(uri=UBEM_LINK.reference_paper_doi, name="reference_paper_doi", curie=UBEM_LINK.curie('reference_paper_doi'),
                   model_uri=UBEM_LINK.reference_paper_doi, domain=None, range=Optional[str],
                   pattern=re.compile(r'^10\.\d{4,9}/\S+$'))

slots.license = Slot(uri=DCT.license, name="license", curie=DCT.curie('license'),
                   model_uri=UBEM_LINK.license, domain=None, range=Optional[str])

slots.access_level = Slot(uri=UBEM_LINK.access_level, name="access_level", curie=UBEM_LINK.curie('access_level'),
                   model_uri=UBEM_LINK.access_level, domain=None, range=Optional[Union[str, "AccessLevel"]])

slots.distributions = Slot(uri=DCAT.distribution, name="distributions", curie=DCAT.curie('distribution'),
                   model_uri=UBEM_LINK.distributions, domain=None, range=Optional[Union[Union[dict, Distribution], list[Union[dict, Distribution]]]])

slots.format = Slot(uri=DCT.format, name="format", curie=DCT.curie('format'),
                   model_uri=UBEM_LINK.format, domain=None, range=Optional[str])

slots.access_url = Slot(uri=DCAT.accessURL, name="access_url", curie=DCAT.curie('accessURL'),
                   model_uri=UBEM_LINK.access_url, domain=None, range=Optional[str])

slots.api = Slot(uri=UBEM_LINK.api, name="api", curie=UBEM_LINK.curie('api'),
                   model_uri=UBEM_LINK.api, domain=None, range=Optional[Union[bool, Bool]])

slots.registration_required = Slot(uri=UBEM_LINK.registration_required, name="registration_required", curie=UBEM_LINK.curie('registration_required'),
                   model_uri=UBEM_LINK.registration_required, domain=None, range=Optional[Union[bool, Bool]])

slots.conventions = Slot(uri=UBEM_LINK.conventions, name="conventions", curie=UBEM_LINK.curie('conventions'),
                   model_uri=UBEM_LINK.conventions, domain=None, range=Optional[Union[Union[dict, Convention], list[Union[dict, Convention]]]])

slots.applies_to = Slot(uri=UBEM_LINK.applies_to, name="applies_to", curie=UBEM_LINK.curie('applies_to'),
                   model_uri=UBEM_LINK.applies_to, domain=None, range=Optional[str])

slots.rule = Slot(uri=UBEM_LINK.rule, name="rule", curie=UBEM_LINK.curie('rule'),
                   model_uri=UBEM_LINK.rule, domain=None, range=Optional[str])

slots.example = Slot(uri=UBEM_LINK.example, name="example", curie=UBEM_LINK.curie('example'),
                   model_uri=UBEM_LINK.example, domain=None, range=Optional[str])

slots.ubem_roles = Slot(uri=UBEM_LINK.ubem_roles, name="ubem_roles", curie=UBEM_LINK.curie('ubem_roles'),
                   model_uri=UBEM_LINK.ubem_roles, domain=None, range=Optional[Union[Union[str, "UBEMRole"], list[Union[str, "UBEMRole"]]]])

slots.content_types = Slot(uri=DCAT.theme, name="content_types", curie=DCAT.curie('theme'),
                   model_uri=UBEM_LINK.content_types, domain=None, range=Optional[Union[str, list[str]]])

slots.geographic_scope = Slot(uri=UBEM_LINK.geographic_scope, name="geographic_scope", curie=UBEM_LINK.curie('geographic_scope'),
                   model_uri=UBEM_LINK.geographic_scope, domain=None, range=Optional[Union[str, "GeographicScope"]])

slots.spatial_coverage = Slot(uri=DCT.spatial, name="spatial_coverage", curie=DCT.curie('spatial'),
                   model_uri=UBEM_LINK.spatial_coverage, domain=None, range=Optional[Union[dict, SpatialCoverage]])

slots.countries = Slot(uri=UBEM_LINK.countries, name="countries", curie=UBEM_LINK.curie('countries'),
                   model_uri=UBEM_LINK.countries, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^([A-Z]{2}|GLOBAL|EU)$'))

slots.bbox = Slot(uri=DCAT.bbox, name="bbox", curie=DCAT.curie('bbox'),
                   model_uri=UBEM_LINK.bbox, domain=None, range=Optional[str])

slots.unit_of_observation = Slot(uri=UBEM_LINK.unit_of_observation, name="unit_of_observation", curie=UBEM_LINK.curie('unit_of_observation'),
                   model_uri=UBEM_LINK.unit_of_observation, domain=None, range=Optional[str])

slots.spatial_granularity = Slot(uri=UBEM_LINK.spatial_granularity, name="spatial_granularity", curie=UBEM_LINK.curie('spatial_granularity'),
                   model_uri=UBEM_LINK.spatial_granularity, domain=None, range=Optional[Union[str, "SpatialGranularity"]])

slots.temporal_coverage = Slot(uri=DCT.temporal, name="temporal_coverage", curie=DCT.curie('temporal'),
                   model_uri=UBEM_LINK.temporal_coverage, domain=None, range=Optional[Union[dict, TemporalCoverage]])

slots.start = Slot(uri=DCAT.startDate, name="start", curie=DCAT.curie('startDate'),
                   model_uri=UBEM_LINK.start, domain=None, range=Optional[str])

slots.end = Slot(uri=DCAT.endDate, name="end", curie=DCAT.curie('endDate'),
                   model_uri=UBEM_LINK.end, domain=None, range=Optional[str])

slots.temporal_resolution = Slot(uri=DCAT.temporalResolution, name="temporal_resolution", curie=DCAT.curie('temporalResolution'),
                   model_uri=UBEM_LINK.temporal_resolution, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(P(?!$)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(T(?=\d)(\d+H)?(\d+M)?(\d+(\.\d+)?S)?)?|static|irregular)$'))

slots.update_frequency = Slot(uri=DCT.accrualPeriodicity, name="update_frequency", curie=DCT.curie('accrualPeriodicity'),
                   model_uri=UBEM_LINK.update_frequency, domain=None, range=Optional[str])

slots.statistical_nature = Slot(uri=UBEM_LINK.statistical_nature, name="statistical_nature", curie=UBEM_LINK.curie('statistical_nature'),
                   model_uri=UBEM_LINK.statistical_nature, domain=None, range=Optional[Union[str, "StatisticalNature"]])

slots.sampling_weights = Slot(uri=UBEM_LINK.sampling_weights, name="sampling_weights", curie=UBEM_LINK.curie('sampling_weights'),
                   model_uri=UBEM_LINK.sampling_weights, domain=None, range=Optional[str])

slots.record_count = Slot(uri=UBEM_LINK.record_count, name="record_count", curie=UBEM_LINK.curie('record_count'),
                   model_uri=UBEM_LINK.record_count, domain=None, range=Optional[int])

slots.record_count_note = Slot(uri=UBEM_LINK.record_count_note, name="record_count_note", curie=UBEM_LINK.curie('record_count_note'),
                   model_uri=UBEM_LINK.record_count_note, domain=None, range=Optional[str])

slots.join_keys = Slot(uri=UBEM_LINK.join_keys, name="join_keys", curie=UBEM_LINK.curie('join_keys'),
                   model_uri=UBEM_LINK.join_keys, domain=None, range=Optional[Union[Union[str, "JoinKey"], list[Union[str, "JoinKey"]]]])

slots.variables_documented = Slot(uri=UBEM_LINK.variables_documented, name="variables_documented", curie=UBEM_LINK.curie('variables_documented'),
                   model_uri=UBEM_LINK.variables_documented, domain=None, range=Optional[Union[bool, Bool]])

slots.machine_readable = Slot(uri=UBEM_LINK.machine_readable, name="machine_readable", curie=UBEM_LINK.curie('machine_readable'),
                   model_uri=UBEM_LINK.machine_readable, domain=None, range=Optional[Union[bool, Bool]])

slots.versioned = Slot(uri=UBEM_LINK.versioned, name="versioned", curie=UBEM_LINK.curie('versioned'),
                   model_uri=UBEM_LINK.versioned, domain=None, range=Optional[Union[bool, Bool]])

slots.persistent_identifier = Slot(uri=UBEM_LINK.persistent_identifier, name="persistent_identifier", curie=UBEM_LINK.curie('persistent_identifier'),
                   model_uri=UBEM_LINK.persistent_identifier, domain=None, range=Optional[Union[bool, Bool]])

slots.known_limitations = Slot(uri=UBEM_LINK.known_limitations, name="known_limitations", curie=UBEM_LINK.curie('known_limitations'),
                   model_uri=UBEM_LINK.known_limitations, domain=None, range=Optional[str])

slots.notes = Slot(uri=UBEM_LINK.notes, name="notes", curie=UBEM_LINK.curie('notes'),
                   model_uri=UBEM_LINK.notes, domain=None, range=Optional[str])

slots.verified = Slot(uri=PROV.wasGeneratedBy, name="verified", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=UBEM_LINK.verified, domain=None, range=Optional[Union[dict, Verification]])

slots.date = Slot(uri=UBEM_LINK.date, name="date", curie=UBEM_LINK.curie('date'),
                   model_uri=UBEM_LINK.date, domain=None, range=Optional[str])

slots.by = Slot(uri=UBEM_LINK.by, name="by", curie=UBEM_LINK.curie('by'),
                   model_uri=UBEM_LINK.by, domain=None, range=Optional[str])

slots.sources_checked = Slot(uri=UBEM_LINK.sources_checked, name="sources_checked", curie=UBEM_LINK.curie('sources_checked'),
                   model_uri=UBEM_LINK.sources_checked, domain=None, range=Optional[Union[Union[str, URI], list[Union[str, URI]]]])

slots.variables = Slot(uri=UBEM_LINK.variables, name="variables", curie=UBEM_LINK.curie('variables'),
                   model_uri=UBEM_LINK.variables, domain=None, range=Optional[Union[Union[dict, VariableProfile], list[Union[dict, VariableProfile]]]])

slots.weather_profile = Slot(uri=UBEM_LINK.weather_profile, name="weather_profile", curie=UBEM_LINK.curie('weather_profile'),
                   model_uri=UBEM_LINK.weather_profile, domain=None, range=Optional[Union[dict, WeatherProfile]])

slots.geometry_profile = Slot(uri=UBEM_LINK.geometry_profile, name="geometry_profile", curie=UBEM_LINK.curie('geometry_profile'),
                   model_uri=UBEM_LINK.geometry_profile, domain=None, range=Optional[Union[dict, GeometryProfile]])

slots.operation_profile = Slot(uri=UBEM_LINK.operation_profile, name="operation_profile", curie=UBEM_LINK.curie('operation_profile'),
                   model_uri=UBEM_LINK.operation_profile, domain=None, range=Optional[Union[dict, OperationProfile]])

slots.characteristics_profile = Slot(uri=UBEM_LINK.characteristics_profile, name="characteristics_profile", curie=UBEM_LINK.curie('characteristics_profile'),
                   model_uri=UBEM_LINK.characteristics_profile, domain=None, range=Optional[Union[dict, CharacteristicsProfile]])

slots.energy_profile = Slot(uri=UBEM_LINK.energy_profile, name="energy_profile", curie=UBEM_LINK.curie('energy_profile'),
                   model_uri=UBEM_LINK.energy_profile, domain=None, range=Optional[Union[dict, EnergyProfile]])

slots.simulation_profile = Slot(uri=UBEM_LINK.simulation_profile, name="simulation_profile", curie=UBEM_LINK.curie('simulation_profile'),
                   model_uri=UBEM_LINK.simulation_profile, domain=None, range=Optional[Union[dict, SimulationProfile]])

slots.context_profile = Slot(uri=UBEM_LINK.context_profile, name="context_profile", curie=UBEM_LINK.curie('context_profile'),
                   model_uri=UBEM_LINK.context_profile, domain=None, range=Optional[Union[dict, ContextProfile]])

slots.provides_concepts = Slot(uri=UBEM_LINK.provides_concepts, name="provides_concepts", curie=UBEM_LINK.curie('provides_concepts'),
                   model_uri=UBEM_LINK.provides_concepts, domain=None, range=Optional[Union[str, list[str]]])

slots.metadata_standards = Slot(uri=UBEM_LINK.metadata_standards, name="metadata_standards", curie=UBEM_LINK.curie('metadata_standards'),
                   model_uri=UBEM_LINK.metadata_standards, domain=None, range=Optional[Union[str, list[str]]])

slots.weather_year_type = Slot(uri=UBEM_LINK.weather_year_type, name="weather_year_type", curie=UBEM_LINK.curie('weather_year_type'),
                   model_uri=UBEM_LINK.weather_year_type, domain=None, range=Optional[Union[Union[str, "WeatherYearType"], list[Union[str, "WeatherYearType"]]]])

slots.weather_file_format = Slot(uri=UBEM_LINK.weather_file_format, name="weather_file_format", curie=UBEM_LINK.curie('weather_file_format'),
                   model_uri=UBEM_LINK.weather_file_format, domain=None, range=Optional[Union[Union[str, "WeatherFileFormat"], list[Union[str, "WeatherFileFormat"]]]])

slots.timestamp_convention = Slot(uri=UBEM_LINK.timestamp_convention, name="timestamp_convention", curie=UBEM_LINK.curie('timestamp_convention'),
                   model_uri=UBEM_LINK.timestamp_convention, domain=None, range=Optional[Union[str, "TimestampConvention"]])

slots.time_basis = Slot(uri=UBEM_LINK.time_basis, name="time_basis", curie=UBEM_LINK.curie('time_basis'),
                   model_uri=UBEM_LINK.time_basis, domain=None, range=Optional[Union[str, "TimeBasis"]])

slots.gap_filling = Slot(uri=UBEM_LINK.gap_filling, name="gap_filling", curie=UBEM_LINK.curie('gap_filling'),
                   model_uri=UBEM_LINK.gap_filling, domain=None, range=Optional[Union[str, "GapFilling"]])

slots.grid_resolution_km = Slot(uri=UBEM_LINK.grid_resolution_km, name="grid_resolution_km", curie=UBEM_LINK.curie('grid_resolution_km'),
                   model_uri=UBEM_LINK.grid_resolution_km, domain=None, range=Optional[float])

slots.station_id_scheme = Slot(uri=UBEM_LINK.station_id_scheme, name="station_id_scheme", curie=UBEM_LINK.curie('station_id_scheme'),
                   model_uri=UBEM_LINK.station_id_scheme, domain=None, range=Optional[str])

slots.climate_scenarios = Slot(uri=UBEM_LINK.climate_scenarios, name="climate_scenarios", curie=UBEM_LINK.curie('climate_scenarios'),
                   model_uri=UBEM_LINK.climate_scenarios, domain=None, range=Optional[Union[str, list[str]]])

slots.geometry_dimension = Slot(uri=UBEM_LINK.geometry_dimension, name="geometry_dimension", curie=UBEM_LINK.curie('geometry_dimension'),
                   model_uri=UBEM_LINK.geometry_dimension, domain=None, range=Optional[Union[str, "GeometryDimension"]])

slots.levels_of_detail = Slot(uri=UBEM_LINK.levels_of_detail, name="levels_of_detail", curie=UBEM_LINK.curie('levels_of_detail'),
                   model_uri=UBEM_LINK.levels_of_detail, domain=None, range=Optional[Union[Union[str, "LevelOfDetail"], list[Union[str, "LevelOfDetail"]]]])

slots.height_source = Slot(uri=UBEM_LINK.height_source, name="height_source", curie=UBEM_LINK.curie('height_source'),
                   model_uri=UBEM_LINK.height_source, domain=None, range=Optional[Union[Union[str, "HeightSource"], list[Union[str, "HeightSource"]]]])

slots.height_reference = Slot(uri=UBEM_LINK.height_reference, name="height_reference", curie=UBEM_LINK.curie('height_reference'),
                   model_uri=UBEM_LINK.height_reference, domain=None, range=Optional[Union[str, "HeightReference"]])

slots.coordinate_reference_system = Slot(uri=UBEM_LINK.coordinate_reference_system, name="coordinate_reference_system", curie=UBEM_LINK.curie('coordinate_reference_system'),
                   model_uri=UBEM_LINK.coordinate_reference_system, domain=None, range=Optional[str],
                   pattern=re.compile(r'^EPSG:[0-9]+$'))

slots.crs_linear_unit = Slot(uri=UBEM_LINK.crs_linear_unit, name="crs_linear_unit", curie=UBEM_LINK.curie('crs_linear_unit'),
                   model_uri=UBEM_LINK.crs_linear_unit, domain=None, range=Optional[str])

slots.building_id_scheme = Slot(uri=UBEM_LINK.building_id_scheme, name="building_id_scheme", curie=UBEM_LINK.curie('building_id_scheme'),
                   model_uri=UBEM_LINK.building_id_scheme, domain=None, range=Optional[str])

slots.minimum_building_size = Slot(uri=UBEM_LINK.minimum_building_size, name="minimum_building_size", curie=UBEM_LINK.curie('minimum_building_size'),
                   model_uri=UBEM_LINK.minimum_building_size, domain=None, range=Optional[str])

slots.behavior_types = Slot(uri=UBEM_LINK.behavior_types, name="behavior_types", curie=UBEM_LINK.curie('behavior_types'),
                   model_uri=UBEM_LINK.behavior_types, domain=None, range=Optional[Union[Union[str, "BehaviorType"], list[Union[str, "BehaviorType"]]]])

slots.control_actions = Slot(uri=UBEM_LINK.control_actions, name="control_actions", curie=UBEM_LINK.curie('control_actions'),
                   model_uri=UBEM_LINK.control_actions, domain=None, range=Optional[Union[Union[str, "ControlAction"], list[Union[str, "ControlAction"]]]])

slots.collection_method = Slot(uri=UBEM_LINK.collection_method, name="collection_method", curie=UBEM_LINK.curie('collection_method'),
                   model_uri=UBEM_LINK.collection_method, domain=None, range=Optional[Union[Union[str, "CollectionMethod"], list[Union[str, "CollectionMethod"]]]])

slots.building_sectors = Slot(uri=UBEM_LINK.building_sectors, name="building_sectors", curie=UBEM_LINK.curie('building_sectors'),
                   model_uri=UBEM_LINK.building_sectors, domain=None, range=Optional[Union[Union[str, "BuildingSector"], list[Union[str, "BuildingSector"]]]])

slots.data_form = Slot(uri=UBEM_LINK.data_form, name="data_form", curie=UBEM_LINK.curie('data_form'),
                   model_uri=UBEM_LINK.data_form, domain=None, range=Optional[Union[Union[str, "DataForm"], list[Union[str, "DataForm"]]]])

slots.representativeness = Slot(uri=UBEM_LINK.representativeness, name="representativeness", curie=UBEM_LINK.curie('representativeness'),
                   model_uri=UBEM_LINK.representativeness, domain=None, range=Optional[Union[str, "Representativeness"]])

slots.coverage_threshold = Slot(uri=UBEM_LINK.coverage_threshold, name="coverage_threshold", curie=UBEM_LINK.curie('coverage_threshold'),
                   model_uri=UBEM_LINK.coverage_threshold, domain=None, range=Optional[str])

slots.cross_tabulations = Slot(uri=UBEM_LINK.cross_tabulations, name="cross_tabulations", curie=UBEM_LINK.curie('cross_tabulations'),
                   model_uri=UBEM_LINK.cross_tabulations, domain=None, range=Optional[Union[str, list[str]]])

slots.energy_data_scale = Slot(uri=UBEM_LINK.energy_data_scale, name="energy_data_scale", curie=UBEM_LINK.curie('energy_data_scale'),
                   model_uri=UBEM_LINK.energy_data_scale, domain=None, range=Optional[Union[str, "EnergyDataScale"]])

slots.energy_sectors = Slot(uri=UBEM_LINK.energy_sectors, name="energy_sectors", curie=UBEM_LINK.curie('energy_sectors'),
                   model_uri=UBEM_LINK.energy_sectors, domain=None, range=Optional[Union[Union[str, "EnergySector"], list[Union[str, "EnergySector"]]]])

slots.energy_carriers = Slot(uri=UBEM_LINK.energy_carriers, name="energy_carriers", curie=UBEM_LINK.curie('energy_carriers'),
                   model_uri=UBEM_LINK.energy_carriers, domain=None, range=Optional[Union[Union[str, "EnergyCarrier"], list[Union[str, "EnergyCarrier"]]]])

slots.energy_metrics = Slot(uri=UBEM_LINK.energy_metrics, name="energy_metrics", curie=UBEM_LINK.curie('energy_metrics'),
                   model_uri=UBEM_LINK.energy_metrics, domain=None, range=Optional[Union[Union[str, "EnergyMetric"], list[Union[str, "EnergyMetric"]]]])

slots.metering_level = Slot(uri=UBEM_LINK.metering_level, name="metering_level", curie=UBEM_LINK.curie('metering_level'),
                   model_uri=UBEM_LINK.metering_level, domain=None, range=Optional[Union[str, "MeteringLevel"]])

slots.measurement_basis = Slot(uri=UBEM_LINK.measurement_basis, name="measurement_basis", curie=UBEM_LINK.curie('measurement_basis'),
                   model_uri=UBEM_LINK.measurement_basis, domain=None, range=Optional[Union[str, "MeasurementBasis"]])

slots.weather_normalized_available = Slot(uri=UBEM_LINK.weather_normalized_available, name="weather_normalized_available", curie=UBEM_LINK.curie('weather_normalized_available'),
                   model_uri=UBEM_LINK.weather_normalized_available, domain=None, range=Optional[Union[bool, Bool]])

slots.reporting_period = Slot(uri=UBEM_LINK.reporting_period, name="reporting_period", curie=UBEM_LINK.curie('reporting_period'),
                   model_uri=UBEM_LINK.reporting_period, domain=None, range=Optional[str])

slots.simulation_engine = Slot(uri=UBEM_LINK.simulation_engine, name="simulation_engine", curie=UBEM_LINK.curie('simulation_engine'),
                   model_uri=UBEM_LINK.simulation_engine, domain=None, range=Optional[str])

slots.stock_representation = Slot(uri=UBEM_LINK.stock_representation, name="stock_representation", curie=UBEM_LINK.curie('stock_representation'),
                   model_uri=UBEM_LINK.stock_representation, domain=None, range=Optional[Union[str, "StockRepresentation"]])

slots.weather_basis = Slot(uri=UBEM_LINK.weather_basis, name="weather_basis", curie=UBEM_LINK.curie('weather_basis'),
                   model_uri=UBEM_LINK.weather_basis, domain=None, range=Optional[str])

slots.context_kind = Slot(uri=UBEM_LINK.context_kind, name="context_kind", curie=UBEM_LINK.curie('context_kind'),
                   model_uri=UBEM_LINK.context_kind, domain=None, range=Optional[Union[Union[str, "ContextKind"], list[Union[str, "ContextKind"]]]])

slots.convention_type = Slot(uri=UBEM_LINK.convention_type, name="convention_type", curie=UBEM_LINK.curie('convention_type'),
                   model_uri=UBEM_LINK.convention_type, domain=None, range=Optional[Union[str, "ConventionType"]])

slots.applies_to_variables = Slot(uri=UBEM_LINK.applies_to_variables, name="applies_to_variables", curie=UBEM_LINK.curie('applies_to_variables'),
                   model_uri=UBEM_LINK.applies_to_variables, domain=None, range=Optional[Union[str, list[str]]])

slots.applies_to_pattern = Slot(uri=UBEM_LINK.applies_to_pattern, name="applies_to_pattern", curie=UBEM_LINK.curie('applies_to_pattern'),
                   model_uri=UBEM_LINK.applies_to_pattern, domain=None, range=Optional[str])

slots.applies_to_codes = Slot(uri=UBEM_LINK.applies_to_codes, name="applies_to_codes", curie=UBEM_LINK.curie('applies_to_codes'),
                   model_uri=UBEM_LINK.applies_to_codes, domain=None, range=Optional[Union[str, list[str]]])

slots.name = Slot(uri=CSVW.name, name="name", curie=CSVW.curie('name'),
                   model_uri=UBEM_LINK.name, domain=None, range=Optional[str])

slots.label = Slot(uri=SKOS.prefLabel, name="label", curie=SKOS.curie('prefLabel'),
                   model_uri=UBEM_LINK.label, domain=None, range=Optional[str])

slots.description = Slot(uri=DCT.description, name="description", curie=DCT.curie('description'),
                   model_uri=UBEM_LINK.description, domain=None, range=Optional[str])

slots.datatype = Slot(uri=UBEM_LINK.datatype, name="datatype", curie=UBEM_LINK.curie('datatype'),
                   model_uri=UBEM_LINK.datatype, domain=None, range=Optional[Union[str, "VariableDatatype"]])

slots.concept = Slot(uri=SKOS.related, name="concept", curie=SKOS.curie('related'),
                   model_uri=UBEM_LINK.concept, domain=None, range=Optional[str])

slots.mapping_relation = Slot(uri=UBEM_LINK.mapping_relation, name="mapping_relation", curie=UBEM_LINK.curie('mapping_relation'),
                   model_uri=UBEM_LINK.mapping_relation, domain=None, range=Optional[Union[str, "MappingRelation"]])

slots.unit = Slot(uri=QUDT.unit, name="unit", curie=QUDT.curie('unit'),
                   model_uri=UBEM_LINK.unit, domain=None, range=Optional[str])

slots.unit_multiplier = Slot(uri=UBEM_LINK.unit_multiplier, name="unit_multiplier", curie=UBEM_LINK.curie('unit_multiplier'),
                   model_uri=UBEM_LINK.unit_multiplier, domain=None, range=Optional[float])

slots.aggregation = Slot(uri=UBEM_LINK.aggregation, name="aggregation", curie=UBEM_LINK.curie('aggregation'),
                   model_uri=UBEM_LINK.aggregation, domain=None, range=Optional[Union[str, "Aggregation"]])

slots.entity = Slot(uri=UBEM_LINK.entity, name="entity", curie=UBEM_LINK.curie('entity'),
                   model_uri=UBEM_LINK.entity, domain=None, range=Optional[Union[str, "EntityType"]])

slots.code_list = Slot(uri=UBEM_LINK.code_list, name="code_list", curie=UBEM_LINK.curie('code_list'),
                   model_uri=UBEM_LINK.code_list, domain=None, range=Optional[Union[Union[dict, CodeEntry], list[Union[dict, CodeEntry]]]])

slots.code = Slot(uri=UBEM_LINK.code, name="code", curie=UBEM_LINK.curie('code'),
                   model_uri=UBEM_LINK.code, domain=None, range=Optional[str])

slots.concept_value = Slot(uri=UBEM_LINK.concept_value, name="concept_value", curie=UBEM_LINK.curie('concept_value'),
                   model_uri=UBEM_LINK.concept_value, domain=None, range=Optional[str])

slots.missing_codes = Slot(uri=UBEM_LINK.missing_codes, name="missing_codes", curie=UBEM_LINK.curie('missing_codes'),
                   model_uri=UBEM_LINK.missing_codes, domain=None, range=Optional[Union[str, list[str]]])

slots.is_weight = Slot(uri=UBEM_LINK.is_weight, name="is_weight", curie=UBEM_LINK.curie('is_weight'),
                   model_uri=UBEM_LINK.is_weight, domain=None, range=Optional[Union[bool, Bool]])

slots.is_imputation_flag = Slot(uri=UBEM_LINK.is_imputation_flag, name="is_imputation_flag", curie=UBEM_LINK.curie('is_imputation_flag'),
                   model_uri=UBEM_LINK.is_imputation_flag, domain=None, range=Optional[Union[bool, Bool]])

slots.flags_variable = Slot(uri=UBEM_LINK.flags_variable, name="flags_variable", curie=UBEM_LINK.curie('flags_variable'),
                   model_uri=UBEM_LINK.flags_variable, domain=None, range=Optional[str])

slots.is_replicate_weight = Slot(uri=UBEM_LINK.is_replicate_weight, name="is_replicate_weight", curie=UBEM_LINK.curie('is_replicate_weight'),
                   model_uri=UBEM_LINK.is_replicate_weight, domain=None, range=Optional[Union[bool, Bool]])

slots.join_key = Slot(uri=UBEM_LINK.join_key, name="join_key", curie=UBEM_LINK.curie('join_key'),
                   model_uri=UBEM_LINK.join_key, domain=None, range=Optional[Union[str, "JoinKey"]])

slots.do_not_use = Slot(uri=UBEM_LINK.do_not_use, name="do_not_use", curie=UBEM_LINK.curie('do_not_use'),
                   model_uri=UBEM_LINK.do_not_use, domain=None, range=Optional[Union[bool, Bool]])

slots.profiled_by = Slot(uri=UBEM_LINK.profiled_by, name="profiled_by", curie=UBEM_LINK.curie('profiled_by'),
                   model_uri=UBEM_LINK.profiled_by, domain=None, range=Optional[str])

slots.confidence = Slot(uri=UBEM_LINK.confidence, name="confidence", curie=UBEM_LINK.curie('confidence'),
                   model_uri=UBEM_LINK.confidence, domain=None, range=Optional[float])

slots.review_flags = Slot(uri=UBEM_LINK.review_flags, name="review_flags", curie=UBEM_LINK.curie('review_flags'),
                   model_uri=UBEM_LINK.review_flags, domain=None, range=Optional[Union[str, list[str]]])

slots.pref_label = Slot(uri=SKOS.prefLabel, name="pref_label", curie=SKOS.curie('prefLabel'),
                   model_uri=UBEM_LINK.pref_label, domain=None, range=Optional[str])

slots.definition = Slot(uri=SKOS.definition, name="definition", curie=SKOS.curie('definition'),
                   model_uri=UBEM_LINK.definition, domain=None, range=Optional[str])

slots.alt_labels = Slot(uri=SKOS.altLabel, name="alt_labels", curie=SKOS.curie('altLabel'),
                   model_uri=UBEM_LINK.alt_labels, domain=None, range=Optional[Union[str, list[str]]])

slots.broader = Slot(uri=SKOS.broader, name="broader", curie=SKOS.curie('broader'),
                   model_uri=UBEM_LINK.broader, domain=None, range=Optional[Union[str, UBEMConceptId]])

slots.concept_role = Slot(uri=UBEM_LINK.concept_role, name="concept_role", curie=UBEM_LINK.curie('concept_role'),
                   model_uri=UBEM_LINK.concept_role, domain=None, range=Optional[Union[str, "UBEMRole"]])

slots.quantity_kind = Slot(uri=QUDT.hasQuantityKind, name="quantity_kind", curie=QUDT.curie('hasQuantityKind'),
                   model_uri=UBEM_LINK.quantity_kind, domain=None, range=Optional[str])

slots.canonical_unit = Slot(uri=UBEM_LINK.canonical_unit, name="canonical_unit", curie=UBEM_LINK.curie('canonical_unit'),
                   model_uri=UBEM_LINK.canonical_unit, domain=None, range=Optional[str])

slots.exact_match = Slot(uri=SKOS.exactMatch, name="exact_match", curie=SKOS.curie('exactMatch'),
                   model_uri=UBEM_LINK.exact_match, domain=None, range=Optional[Union[str, list[str]]])

slots.close_match = Slot(uri=SKOS.closeMatch, name="close_match", curie=SKOS.curie('closeMatch'),
                   model_uri=UBEM_LINK.close_match, domain=None, range=Optional[Union[str, list[str]]])

slots.related_match = Slot(uri=SKOS.relatedMatch, name="related_match", curie=SKOS.curie('relatedMatch'),
                   model_uri=UBEM_LINK.related_match, domain=None, range=Optional[Union[str, list[str]]])

slots.broad_match = Slot(uri=SKOS.broadMatch, name="broad_match", curie=SKOS.curie('broadMatch'),
                   model_uri=UBEM_LINK.broad_match, domain=None, range=Optional[Union[str, list[str]]])

slots.narrow_match = Slot(uri=SKOS.narrowMatch, name="narrow_match", curie=SKOS.curie('narrowMatch'),
                   model_uri=UBEM_LINK.narrow_match, domain=None, range=Optional[Union[str, list[str]]])

slots.DatasetProfile_id = Slot(uri=UBEM_LINK.id, name="DatasetProfile_id", curie=UBEM_LINK.curie('id'),
                   model_uri=UBEM_LINK.DatasetProfile_id, domain=DatasetProfile, range=Union[str, DatasetProfileId],
                   pattern=re.compile(r'^[a-z0-9][a-z0-9_.-]*$'))

slots.DatasetProfile_title = Slot(uri=DCT.title, name="DatasetProfile_title", curie=DCT.curie('title'),
                   model_uri=UBEM_LINK.DatasetProfile_title, domain=DatasetProfile, range=str)

slots.DatasetProfile_ubem_roles = Slot(uri=UBEM_LINK.ubem_roles, name="DatasetProfile_ubem_roles", curie=UBEM_LINK.curie('ubem_roles'),
                   model_uri=UBEM_LINK.DatasetProfile_ubem_roles, domain=DatasetProfile, range=Union[Union[str, "UBEMRole"], list[Union[str, "UBEMRole"]]])

slots.DatasetProfile_statistical_nature = Slot(uri=UBEM_LINK.statistical_nature, name="DatasetProfile_statistical_nature", curie=UBEM_LINK.curie('statistical_nature'),
                   model_uri=UBEM_LINK.DatasetProfile_statistical_nature, domain=DatasetProfile, range=Union[str, "StatisticalNature"])

slots.DatasetProfile_spatial_granularity = Slot(uri=UBEM_LINK.spatial_granularity, name="DatasetProfile_spatial_granularity", curie=UBEM_LINK.curie('spatial_granularity'),
                   model_uri=UBEM_LINK.DatasetProfile_spatial_granularity, domain=DatasetProfile, range=Union[str, "SpatialGranularity"])

slots.DatasetProfile_access_level = Slot(uri=UBEM_LINK.access_level, name="DatasetProfile_access_level", curie=UBEM_LINK.curie('access_level'),
                   model_uri=UBEM_LINK.DatasetProfile_access_level, domain=DatasetProfile, range=Union[str, "AccessLevel"])

slots.Convention_rule = Slot(uri=UBEM_LINK.rule, name="Convention_rule", curie=UBEM_LINK.curie('rule'),
                   model_uri=UBEM_LINK.Convention_rule, domain=Convention, range=str)

slots.WeatherProfile_weather_year_type = Slot(uri=UBEM_LINK.weather_year_type, name="WeatherProfile_weather_year_type", curie=UBEM_LINK.curie('weather_year_type'),
                   model_uri=UBEM_LINK.WeatherProfile_weather_year_type, domain=WeatherProfile, range=Union[Union[str, "WeatherYearType"], list[Union[str, "WeatherYearType"]]])

slots.GeometryProfile_geometry_dimension = Slot(uri=UBEM_LINK.geometry_dimension, name="GeometryProfile_geometry_dimension", curie=UBEM_LINK.curie('geometry_dimension'),
                   model_uri=UBEM_LINK.GeometryProfile_geometry_dimension, domain=GeometryProfile, range=Union[str, "GeometryDimension"])

slots.OperationProfile_behavior_types = Slot(uri=UBEM_LINK.behavior_types, name="OperationProfile_behavior_types", curie=UBEM_LINK.curie('behavior_types'),
                   model_uri=UBEM_LINK.OperationProfile_behavior_types, domain=OperationProfile, range=Union[Union[str, "BehaviorType"], list[Union[str, "BehaviorType"]]])

slots.CharacteristicsProfile_data_form = Slot(uri=UBEM_LINK.data_form, name="CharacteristicsProfile_data_form", curie=UBEM_LINK.curie('data_form'),
                   model_uri=UBEM_LINK.CharacteristicsProfile_data_form, domain=CharacteristicsProfile, range=Union[Union[str, "DataForm"], list[Union[str, "DataForm"]]])

slots.EnergyProfile_energy_data_scale = Slot(uri=UBEM_LINK.energy_data_scale, name="EnergyProfile_energy_data_scale", curie=UBEM_LINK.curie('energy_data_scale'),
                   model_uri=UBEM_LINK.EnergyProfile_energy_data_scale, domain=EnergyProfile, range=Union[str, "EnergyDataScale"])

slots.VariableProfile_name = Slot(uri=CSVW.name, name="VariableProfile_name", curie=CSVW.curie('name'),
                   model_uri=UBEM_LINK.VariableProfile_name, domain=VariableProfile, range=str)

slots.UBEMConcept_id = Slot(uri=UBEM_LINK.id, name="UBEMConcept_id", curie=UBEM_LINK.curie('id'),
                   model_uri=UBEM_LINK.UBEMConcept_id, domain=UBEMConcept, range=Union[str, UBEMConceptId],
                   pattern=re.compile(r'^[a-z0-9][a-z0-9_.-]*$'))

slots.UBEMConcept_pref_label = Slot(uri=SKOS.prefLabel, name="UBEMConcept_pref_label", curie=SKOS.curie('prefLabel'),
                   model_uri=UBEM_LINK.UBEMConcept_pref_label, domain=UBEMConcept, range=str)

slots.UBEMConcept_definition = Slot(uri=SKOS.definition, name="UBEMConcept_definition", curie=SKOS.curie('definition'),
                   model_uri=UBEM_LINK.UBEMConcept_definition, domain=UBEMConcept, range=str)

