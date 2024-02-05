# Copyright © LFV

from dataclasses import dataclass
from typing import Optional

from reqstool.common.dataclasses.urn_id import UrnId


@dataclass
class IDFilters:
    urn_ids_imports: Optional[set[UrnId]] = None
    urn_ids_excludes: Optional[set[UrnId]] = None
    custom_imports: Optional[str] = None
    custom_exclude: Optional[str] = None

    def is_all_none(self) -> bool:
        return (
            self.urn_ids_imports is None
            and self.urn_ids_excludes is None
            and self.custom_imports is None
            and self.custom_exclude is None
        )
