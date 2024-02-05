# Copyright © LFV

from dataclasses import dataclass
from typing import Dict, List, Set

from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.models.annotations import AnnotationData
from reqstool.models.mvrs import MVRData
from reqstool.models.requirements import RequirementData
from reqstool.models.svcs import SVCData
from reqstool.models.test_data import TestData


@dataclass
class CombinedIndexedDataset:
    initial_model_urn: str

    urn_parsing_order: List[str]

    # key: urn
    visited_imports_during_filtering: Set[str]

    # metadata
    accessible_nodes_dict: Dict[str, List[str]]
    filtered: bool

    # datastructures

    requirements: Dict[UrnId, RequirementData]
    svcs: Dict[UrnId, SVCData]
    mvrs: Dict[UrnId, MVRData]

    # annotations have no id
    # key = req id
    annotations_impls: Dict[UrnId, List[AnnotationData]]
    # key = svc id
    annotations_tests: Dict[UrnId, List[AnnotationData]]

    # key = fully qualified method
    automated_test_result: Dict[UrnId, List[TestData]]

    # indexes/lookups

    # requirement indexes
    reqs_from_urn: Dict[str, List[UrnId]]

    # svc indexes
    svcs_from_urn: Dict[str, List[UrnId]]
    svcs_from_req: Dict[UrnId, List[UrnId]]

    # mvr indexes
    mvrs_from_urn: Dict[str, List[UrnId]]
    mvrs_from_svc: Dict[UrnId, List[UrnId]]
