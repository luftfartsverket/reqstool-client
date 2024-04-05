# Copyright © LFV

from dataclasses import dataclass, field
from pathlib import PurePath
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

    # dynamic
    annotations_yml: RequirementsIndataPathItem = field(
        default_factory=lambda: RequirementsIndataPathItem(path="annotations.yml")
    )
    test_results_dirs: List[RequirementsIndataPathItem] = field(
        default_factory=lambda: [RequirementsIndataPathItem(path="test_results")]
    )

    def prepend_paths(self, prepend_dir):
        for prop in dir(self):
            if (
                not prop.startswith("__")
                and isinstance(getattr(self, prop), RequirementsIndataPathItem)
                and prop not in ["requirements_yml", "svcs_yml", "mvrs_yml"]
            ):
                path_item = getattr(self, prop)
                if path_item.path is not None:
                    path_item.path = str(PurePath(prepend_dir, path_item.path))

    # other has precedence
    def merge(self, other):
        merged_instance = self.__class__()
        for prop in dir(self):
            if not prop.startswith("__"):
                a_value = getattr(self, prop)
                b_value = getattr(other, prop)
                setattr(merged_instance, prop, b_value if b_value is not None else a_value)

        return merged_instance
