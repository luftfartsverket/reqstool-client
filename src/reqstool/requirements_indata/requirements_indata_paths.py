# Copyright © LFV

from dataclasses import dataclass, field
from pathlib import PurePath


@dataclass(kw_only=True)
class RequirementsIndataStructureItem:
    path: str
    exists: bool = False


@dataclass(kw_only=True)
class RequirementsIndataPaths:
    # static
    requirements_yml: RequirementsIndataStructureItem = field(
        default_factory=lambda: RequirementsIndataStructureItem(path="requirements.yml")
    )

    svcs_yml: RequirementsIndataStructureItem = field(
        default_factory=lambda: RequirementsIndataStructureItem(path="software_verification_cases.yml")
    )
    mvrs_yml: RequirementsIndataStructureItem = field(
        default_factory=lambda: RequirementsIndataStructureItem(path="manual_verification_results.yml")
    )

    # dynamic
    annotations_yml: RequirementsIndataStructureItem = field(
        default_factory=lambda: RequirementsIndataStructureItem(path="annotations.yml")
    )
    test_results_failsafe_dir: RequirementsIndataStructureItem = field(
        default_factory=lambda: RequirementsIndataStructureItem(path="test_results/failsafe")
    )
    test_results_surefire_dir: RequirementsIndataStructureItem = field(
        default_factory=lambda: RequirementsIndataStructureItem(path="test_results/surefire")
    )

    def prepend_paths(self, prepend_dir):
        for prop in dir(self):
            if (
                not prop.startswith("__")
                and isinstance(getattr(self, prop), RequirementsIndataStructureItem)
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
