# Copyright © LFV

from dataclasses import dataclass

from reqstool.requirements_indata.requirements_indata_paths import RequirementsIndataPathItem, RequirementsIndataPaths


@dataclass(kw_only=True)
class PythonRequirementsIndataPaths(RequirementsIndataPaths):
    def __init__(self):
        super().__init__()

        self.annotations_yml = RequirementsIndataPathItem(path="build/reqstool/annotations.yml")

        self.test_results_dirs = [RequirementsIndataPathItem(path="build/junit.xml")]
