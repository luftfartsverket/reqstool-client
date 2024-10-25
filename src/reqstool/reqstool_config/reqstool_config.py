# Copyright © LFV

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Resources:
    requirements: Optional[str] = field(default=None)
    software_verification_cases: Optional[str] = field(default=None)
    manual_verification_results: Optional[str] = field(default=None)
    annotations: Optional[str] = field(default=None)
    test_results: List[str] = field(default_factory=lambda: [])


@dataclass
class ReqstoolConfig:
    language: str
    build: str
    resources: Resources

    @staticmethod
    def _parse(yaml_data: dict) -> "ReqstoolConfig":
        r_language = yaml_data.get("language", None)
        r_build = yaml_data.get("build", None)

        # Parse resources
        resources_data = yaml_data["resources"]
        r_resources = Resources(
            requirements=(resources_data["requirements"] if "requirements" in resources_data else None),
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

        return ReqstoolConfig(
            language=r_language,
            build=r_build,
            resources=r_resources,
        )
