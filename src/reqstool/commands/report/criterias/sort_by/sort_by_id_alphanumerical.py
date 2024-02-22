# Copyright © LFV

from dataclasses import dataclass

from reqstool.commands.report.criterias.group_by.group_by import K
from reqstool.commands.report.criterias.sort_by.sort_by import SortByInterface
from reqstool.common.dataclasses.urn_id import UrnId


@dataclass(kw_only=True)
class SortByIdAlphanumerical(SortByInterface):

    def sort(self, req_data: UrnId) -> K:
        return req_data.id
