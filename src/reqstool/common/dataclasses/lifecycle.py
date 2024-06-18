# Copyright © LFV

from dataclasses import dataclass, field
from enum import Enum, unique


@unique
class LIFECYCLESTATE(Enum):
    DRAFT = "draft"
    EFFECTIVE = "effective"
    DEPRECATED = "deprecated"
    OBSOLETE = "obsolete"


@dataclass
class LifecycleData:
    reason: str = field(default=str)
    state: LIFECYCLESTATE = field(default=LIFECYCLESTATE.EFFECTIVE)
