# Copyright © LFV

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from operator import itemgetter
from typing import Dict, Iterator, List, Tuple, TypeVar

from reqstool.commands.report.criterias.sort_by.sort_by import SORT_BY_OPTIONS
from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.models.combined_indexed_dataset import CombinedIndexedDataset

K = TypeVar("K")


@dataclass(kw_only=True)
class GroupByInterface(ABC):
    cid: CombinedIndexedDataset
    sort_by: List[SORT_BY_OPTIONS]

    grouped_requirements: Dict[K, List[UrnId]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self._group()
        self._sort()

    def __iter__(self) -> Iterator[Tuple[K, List[UrnId]]]:
        return iter(self.grouped_requirements.items())

    def _add_req_to_group(self, group: K, urn_id: UrnId):
        if group not in self.grouped_requirements:
            logging.debug(f"Creating list in dict for group: {group}")
            self.grouped_requirements[group] = []

        self.grouped_requirements[group].append(urn_id)

    # https://docs.python.org/3/howto/sorting.html#operator-module-functions-and-partial-function-evaluation

    # i think we should use attrgetter, that would also allow sort by A then B

    def _sort(self):
        self.sort_by = [SORT_BY_OPTIONS.ID, SORT_BY_OPTIONS.REVISION]

        if len(self.sort_by) == 0:
            return

        # Define a mapping of attribute names to itemgetters
        # attr_mapping = {
        #     SORT_BY_OPTIONS.ID: itemgetter(SORT_BY_OPTIONS.ID.value),
        #     SORT_BY_OPTIONS.REVISION: itemgetter(SORT_BY_OPTIONS.REVISION.value),
        #     SORT_BY_OPTIONS.SIGNIFICANCE: itemgetter(SORT_BY_OPTIONS.SIGNIFICANCE.value),
        # }

        # not sure that this works with tuple
        # we need to return a single itemgetter that can have multiple fields, i.e. itemg
        for group, urn_ids in self.grouped_requirements.items():
            urn_ids.sort(
                key=lambda urn_id: itemgetter(*[sort_option.value for sort_option in self.sort_by])(
                    self.cid.requirements[urn_id]
                ),
                # key=lambda urn_id: tuple(
                #     attr_mapping[sort_option](self.cid.requirements[urn_id]) for sort_option in self.sort_by
                # ),
                # urn_ids.sort(
                #     key=itemgetter(*[sort_option.value for sort_option in self.sort_by])
                # )
            )

    @abstractmethod
    def _group(self):
        pass
