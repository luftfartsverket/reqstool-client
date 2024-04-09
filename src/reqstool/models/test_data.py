# Copyright © LFV

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict

from reqstool.common.dataclasses.urn_id import UrnId


class TEST_RUN_STATUS(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    MISSING = "missing"


@dataclass
class TestData:
    fully_qualified_name: str
    status: TEST_RUN_STATUS


@dataclass
class TestsData:
    # key: urn + fqn
    tests: Dict[UrnId, TestData] = field(default_factory=dict)
