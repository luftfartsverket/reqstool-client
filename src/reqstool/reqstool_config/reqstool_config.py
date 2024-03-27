# Copyright © LFV

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import List, Optional


@unique
class TYPES(Enum):
    DEFAULT = "default"
    JAVA_MAVEN = "java-maven"
    PYTHON = "python"


@dataclass
class Locations:
    test_results: List[str] = field(default_factory=lambda: [])
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

        r_locations = Locations(annotations=None, test_results=[])

        if "locations" in yaml_data:

            locations = yaml_data["locations"]

            if "annotations" in locations:
                annotations = locations["annotations"]

                r_locations.annotations = annotations

            if "test_results_dirs" in locations:
                r_locations.test_results = locations["test_results_dirs"]

        return ReqstoolConfig(type=r_type, project_root_dir=r_project_root_dir, locations=r_locations)
