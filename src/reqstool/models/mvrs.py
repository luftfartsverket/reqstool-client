# Copyright © LFV

from dataclasses import dataclass, field
from typing import Dict, List

from reqstool.common.dataclasses.urn_id import UrnId


@dataclass
class MVRData:
    id: UrnId
    comment: str
    passed: bool
    svc_ids: List[UrnId] = field(default_factory=list)


@dataclass
class MVRsData:
    results: Dict[UrnId, MVRData] = field(default_factory=dict)
