# Copyright © LFV

from dataclasses import dataclass

from reqstool.requirements_indata.requirements_indata_paths import (
    RequirementsIndataPaths,
    RequirementsIndataStructureItem,
)


@dataclass(kw_only=True, frozen=True)
class RequirementsIndataPathItem:
    path: str
    exists: bool = False


@dataclass(kw_only=True)
class JavaMavenRequirementsIndataPaths(RequirementsIndataPaths):
    def __init__(self):
        super().__init__()

        self.annotations_yml = RequirementsIndataStructureItem(path="target/reqstool/annotations.yml")

        self.test_results_failsafe_dir = RequirementsIndataStructureItem(path="target/failsafe-reports")
        self.test_results_surefire_dir = RequirementsIndataStructureItem(path="target/surefire-reports")
