# Copyright © LFV

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, unique
from typing import TypeVar

from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.models.combined_indexed_dataset import CombinedIndexedDataset

K = TypeVar("K")


# sorting can only be made on relevant req_data data

# relevant is:

# * a scalar: string, int, enumeration etc (not dict, list etc)
# * mandatory field?


# relevant for now are


@unique
class SORT_BY_OPTIONS(Enum):
    ID = "id"
    SIGNIFICANCE = "significance"
    REVISION = "revision"


@dataclass(kw_only=True)
class SortByInterface(ABC):
    cid: CombinedIndexedDataset

    @abstractmethod
    def sort(self, req_data: UrnId) -> K:
        pass
