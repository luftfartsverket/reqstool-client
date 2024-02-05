# Copyright © LFV

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, unique


@unique
class LOCATIONTYPES(Enum):
    GIT = "git"
    LOCAL = "local"
    MAVEN = "maven"


@dataclass(kw_only=True)
class LocationInterface(ABC):
    path: str

    @abstractmethod
    def _make_available_on_localdisk(self, dst_path: str):
        pass
