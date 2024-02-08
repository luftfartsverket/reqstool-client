# Copyright © LFV

from dataclasses import dataclass, field
import dataclasses
from pathlib import PurePath
from reqstool.locations.local_location import LocalLocation
from reqstool.locations.location import LocationInterface


@dataclass(kw_only=True)
class LocationResolver:
    parent: LocationInterface
    current: LocationInterface = field(init=False)
    _current_unresolved: LocationInterface

    def __post_init__(self):
        self.current = self._LocationResolver__resolve_resolved()

    def __resolve_resolved(self) -> LocationInterface:
        # Parent: None   Current: X     -> Resolved: X
        if self.parent is None:
            resolved = self._current_unresolved
        elif isinstance(self._current_unresolved, LocalLocation):
            # Parent: X  Current: Local -> Resolved: X (resolve path)
            if PurePath(self._current_unresolved.path).is_absolute():
                new_path = self._current_unresolved.path
            else:
                new_path = PurePath(self.parent.path, self._current_unresolved.path)

            resolved = dataclasses.replace(self.parent, path=new_path)

        # Parent: Local  Current: Git   -> Resolved: Git
        # Parent: Local  Current: Maven -> Resolved: Maven
        # Parent: Git    Current: Git   -> Resolved: Git
        # Parent: Git    Current: Maven -> Resolved: Maven
        # Parent: Maven  Current: Git   -> Resolved: Git
        # Parent: Maven  Current: Maven -> Resolved: Maven
        else:
            resolved = self._current_unresolved

        return resolved

    def make_available_on_localdisk(self, dst_path: str):
        return self.current._make_available_on_localdisk(dst_path=dst_path)
