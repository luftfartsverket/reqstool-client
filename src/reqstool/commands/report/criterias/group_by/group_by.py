# Copyright © LFV

from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from operator import attrgetter
from types import MappingProxyType
from typing import Dict, Iterator, List, Tuple, TypeVar

from reqstool.commands.report.criterias.sort_by.sort_by import SORT_BY_OPTIONS
from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.models.combined_indexed_dataset import CombinedIndexedDataset

K = TypeVar("K")


@dataclass(kw_only=True)
class GroupByInterface(ABC):
    cid: CombinedIndexedDataset
    sort_by: List[SORT_BY_OPTIONS]

    grouped_requirements: Dict[K, List[UrnId]] = field(init=False, default_factory=lambda: defaultdict(list))

    def __post_init__(self):
        self._group()
        # make immutable
        self.grouped_requirements = MappingProxyType(dict(self.grouped_requirements))
        self._sort()

    def __iter__(self) -> Iterator[Tuple[K, List[UrnId]]]:
        return iter(self.grouped_requirements.items())

    def _add_req_to_group(self, group: K, urn_id: UrnId):
        self.grouped_requirements[group].append(urn_id)

    def _sort(self):
        if len(self.sort_by) == 0:
            return

        for group, urn_ids in self.grouped_requirements.items():
            urn_ids.sort(
                key=lambda urn_id: attrgetter(*[sort_option.value for sort_option in self.sort_by])(
                    self.cid.requirements[urn_id]
                )
            )

    @abstractmethod
    def _group(self):
        pass
