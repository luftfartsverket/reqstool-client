# Copyright © LFV

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Dict, List, Set

from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.filters.requirements_filters import RequirementFilter
from reqstool.models.implementations import ImplementationDataInterface
from reqstool.models.imports import ImportDataInterface


@unique
class VARIANTS(Enum):
    SYSTEM = "system"
    MICROSERVICE = "microservice"
    EXTERNAL = "external"


@unique
class TYPES(Enum):
    REQUIREMENTS = "requirements"
    SOFTWARE_VERIFICATION_CASES = "software_verification_cases"
    EXTERNAL = "manual_verification_results"


@unique
class SIGNIFANCETYPES(Enum):
    SHALL = "shall"
    SHOULD = "should"
    MAY = "may"


@dataclass
class ReferenceData:
    requirement_ids: Set[UrnId] = set[UrnId]
    sources: Set[str] = set[str]


@dataclass
class RequirementData:
    id: UrnId
    title: str
    significance: SIGNIFANCETYPES
    description: str
    rationale: str
    revision: str
    category: List[str] = field(default_factory=list)
    references: List[ReferenceData] = field(default_factory=list)


@dataclass
class MetaData:
    urn: str
    variant: VARIANTS
    title: str
    url: str


@dataclass
class RequirementsData:
    metadata: MetaData
    implementations: List[ImplementationDataInterface] = field(default_factory=list)
    imports: List[ImportDataInterface] = field(default_factory=list)
    # key: urn
    filters: Dict[str, RequirementFilter] = field(default_factory=list)
    requirements: Dict[str, RequirementData] = field(default_factory=dict)
