# Copyright © LFV

from dataclasses import dataclass, field
from typing import List

from reqstool_python_decorators.decorators.decorators import Requirements


@dataclass(kw_only=True)
class RequirementsIndataPathItem:
    path: str
    exists: bool = False


@Requirements("REQ_016")
@dataclass(kw_only=True)
class RequirementsIndataPaths:
    # static
    requirements_yml: RequirementsIndataPathItem = field(
        default_factory=lambda: RequirementsIndataPathItem(path="requirements.yml")
    )

    svcs_yml: RequirementsIndataPathItem = field(
        default_factory=lambda: RequirementsIndataPathItem(path="software_verification_cases.yml")
    )
    mvrs_yml: RequirementsIndataPathItem = field(
        default_factory=lambda: RequirementsIndataPathItem(path="manual_verification_results.yml")
    )

    # generated
    annotations_yml: RequirementsIndataPathItem = field(
        default_factory=lambda: RequirementsIndataPathItem(path="annotations.yml")
    )
    test_results: List[RequirementsIndataPathItem] = field(
        default_factory=lambda: [RequirementsIndataPathItem(path="test_results")]
    )

    # # generated
    # annotations_yml: RequirementsIndataPathItem = field(
    #     default_factory=lambda: RequirementsIndataPathItem(path="annotations.yml")
    # )
    # test_results: List[RequirementsIndataPathItem] = field(
    #     default_factory=lambda: [RequirementsIndataPathItem(path="test_results")]
    # )
