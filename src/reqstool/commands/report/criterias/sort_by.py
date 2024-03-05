# Copyright © LFV

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, unique
from typing import TypeVar

from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.models.combined_indexed_dataset import CombinedIndexedDataset

K = TypeVar("K")


@unique
class SortByOptions(Enum):
    ID = "id"
    SIGNIFICANCE = "significance"
    REVISION = "revision"


@dataclass(kw_only=True)
class SortByInterface(ABC):
    cid: CombinedIndexedDataset

    @abstractmethod
    def sort(self, req_data: UrnId) -> K:
        pass
