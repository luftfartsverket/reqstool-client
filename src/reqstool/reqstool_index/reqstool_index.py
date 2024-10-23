# Copyright © LFV

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import List, Optional


@unique
class LANGUAGE_TYPES(Enum):
    JAVA: str = "java"
    JAVASCRIPT: str = "javascript"
    PYTHON: str = "python"
    TYPESCRIPT: str = "typescript"


@unique
class BUILD_TOOL_TYPES(Enum):
    GRADLE: str = "gradle"
    HATCH: str = "hatch"
    MAVEN: str = "maven"
    NPM: str = "npm"
    POETRY: str = "poetry"
    YARN: str = "yarn"


@dataclass
class Resources:
    requirements: str
    software_verification_cases: Optional[str] = field(default=None)
    manual_verification_results: Optional[str] = field(default=None)
    annotations: Optional[str] = field(default=None)
    test_results: List[str] = field(default_factory=list)


@dataclass
class ReqstoolIndex:
    language: LANGUAGE_TYPES
    build: BUILD_TOOL_TYPES
    version: str
    resources: Resources

    @staticmethod
    def _parse(yaml_data: dict) -> "ReqstoolIndex":
        r_language = LANGUAGE_TYPES(yaml_data["language"])
        r_build = BUILD_TOOL_TYPES(yaml_data["build"])
        r_version = yaml_data["version"]

        # Parse resources
        resources_data = yaml_data["resources"]
        r_resources = Resources(
            requirements=resources_data["requirements"],
            software_verification_cases=(
                resources_data["software_verification_cases"]
                if "software_verification_cases" in resources_data
                else None
            ),
            manual_verification_results=(
                resources_data["manual_verification_results"]
                if "manual_verification_results" in resources_data
                else None
            ),
            annotations=resources_data["annotations"] if "annotations" in resources_data else None,
            test_results=resources_data["test_results"] if "test_results" in resources_data else None,
        )

        return ReqstoolIndex(
            language=r_language,
            build=r_build,
            version=r_version,
            resources=r_resources,
        )
