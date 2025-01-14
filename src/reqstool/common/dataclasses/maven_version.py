# Copyright © LFV

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MavenVersion:
    version: str
    major: int = field(init=False)
    minor: int = field(init=False)
    patch: int = field(init=False)
    build_number: Optional[int] = field(init=False)
    qualifier: Optional[str] = field(init=False)
    snapshot: bool = field(init=False, default=False)  # New field for SNAPSHOT detection

    PATTERN_SEMANTIC_VERSION: re.Pattern[str] = re.compile(
        "^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:-(?P<buildno>\d+))?(?:[-.]?(?P<qualifier>"
        "(?!SNAPSHOT$)[a-zA-Z][a-zA-Z0-9]*))?(?:-(?P<snapshot>SNAPSHOT))?$"
    )

    def __post_init__(self) -> None:
        match: Optional[re.Match[str]] = self.PATTERN_SEMANTIC_VERSION.match(self.version)

        if not match:
            raise ValueError(f"Not a valid semantic Maven version string: {self.version}")

        # semantic version is mandatory
        self.major = int(match.group("major"))
        self.minor = int(match.group("minor"))
        self.patch = int(match.group("patch"))

        self.build_number = int(match.group("buildno")) if match.group("buildno") else None

        self.qualifier = match.group("qualifier")

        # check if "SNAPSHOT" is in the version string
        self.snapshot = True if match.group("snapshot") else False
