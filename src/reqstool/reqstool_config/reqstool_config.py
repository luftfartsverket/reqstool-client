# Copyright © LFV

from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional


@unique
class TYPES(Enum):
    DEFAULT = "default"
    JAVA_MAVEN = "java-maven"


@dataclass
class TestResults:
    failsafe: Optional[str] = None
    surefire: Optional[str] = None


@dataclass
class Locations:
    test_results: TestResults
    annotations: Optional[str] = None


@dataclass
class ReqstoolConfig:
    project_root_dir: str
    type: TYPES
    locations: Optional[Locations] = None

    @staticmethod
    def _parse(yaml_data: dict) -> "ReqstoolConfig":
        r_type = TYPES(yaml_data["type"])

        r_project_root_dir = "." if "project_root_dir" not in yaml_data else yaml_data["project_root_dir"]

        r_locations = Locations(annotations=None, test_results=TestResults())

        if "locations" not in yaml_data:
            return ReqstoolConfig(type=r_type, project_root_dir=r_project_root_dir, locations=r_locations)

        locations = yaml_data["locations"]

        if "annotations" in locations:
            annotations = locations["annotations"]

            r_locations.annotations = annotations

        if "test_results" in locations:
            test_results = locations["test_results"]

            if "failsafe" in test_results:
                r_locations.test_results.failsafe = test_results["failsafe"]

            if "surefire" in test_results:
                r_locations.test_results.surefire = test_results["surefire"]

        return ReqstoolConfig(type=r_type, project_root_dir=r_project_root_dir, locations=r_locations)
