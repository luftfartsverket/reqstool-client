# Copyright © LFV

from dataclasses import dataclass, field
from typing import Dict, List

from reqstool.common.dataclasses.urn_id import UrnId


@dataclass
class AnnotationData:
    element_kind: str  # FIELD, METHOD, CLASS, ENUM, INTERFACE, RECORD
    fully_qualified_name: str


@dataclass
class AnnotationsData:
    implementations: Dict[str, List[AnnotationData]] = field(default_factory=dict)
    tests: Dict[UrnId, List[AnnotationData]] = field(default_factory=dict)
