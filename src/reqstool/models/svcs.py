# Copyright © LFV

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Dict, List
from packaging.version import Version

from reqstool.common.dataclasses.lifecycle import LIFECYCLESTATE, LifecycleData
from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.filters.svcs_filters import SVCFilter


@unique
class VERIFICATIONTYPES(Enum):
    AUTOMATED_TEST = "automated-test"
    MANUAL_TEST = "manual-test"
    REVIEW = "review"
    PLATFORM = "platform"
    OTHER = "other"


@dataclass(kw_only=True, frozen=True)
class SVCData:
    id: UrnId
    title: str
    description: str
    verification: VERIFICATIONTYPES
    instructions: str
    revision: Version
    lifecycle: LifecycleData = field(default_factory=lambda: LifecycleData(state=LIFECYCLESTATE.EFFECTIVE, reason=None))
    requirement_ids: List[UrnId] = field(default_factory=list)


@dataclass
class SVCsData:
    # key: svc_id
    cases: Dict[str, SVCData] = field(default_factory=dict)
    # key: urn
    filters: Dict[str, SVCFilter] = field(default_factory=dict)
