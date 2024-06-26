# Copyright © LFV

from dataclasses import dataclass, field
from enum import Enum, unique


@unique
class LIFECYCLESTATE(Enum):
    DRAFT = "draft"
    EFFECTIVE = "effective"
    DEPRECATED = "deprecated"
    OBSOLETE = "obsolete"


lifecycle_state_sort_order = {
    LIFECYCLESTATE.OBSOLETE: 0,
    LIFECYCLESTATE.DEPRECATED: 1,
    LIFECYCLESTATE.EFFECTIVE: 2,
    LIFECYCLESTATE.DRAFT: 3,
}


@dataclass
class LifecycleData:
    reason: str = field(default=str)
    state: LIFECYCLESTATE = field(default=LIFECYCLESTATE.EFFECTIVE)
