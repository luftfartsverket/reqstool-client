# Copyright © LFV

from dataclasses import dataclass, field
from typing import Dict, List

from reqstool.models.annotations import AnnotationsData
from reqstool.models.mvrs import MVRsData
from reqstool.models.requirements import RequirementsData
from reqstool.models.svcs import SVCsData
from reqstool.models.test_data import TestsData


@dataclass
class RawDataset:
    requirements_data: RequirementsData = None

    svcs_data: SVCsData = None

    annotations_data: AnnotationsData = None

    automated_tests: TestsData = None

    mvrs_data: MVRsData = None


@dataclass
class CombinedRawDataset:
    initial_model_urn: str
    urn_parsing_order: List[str] = field(default_factory=list)
    parsing_graph: Dict[str, List[str]] = field(default_factory=dict)
    raw_datasets: Dict[str, RawDataset] = field(default_factory=dict)
