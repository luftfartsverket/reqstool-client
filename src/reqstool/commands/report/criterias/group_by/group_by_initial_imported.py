# Copyright © LFV

from dataclasses import dataclass

from reqstool.commands.report.criterias.group_by.group_by import GroupByInterface


@dataclass(kw_only=True)
class GroupByCategory(GroupByInterface):

    # how do we handle requirements without category
    # if a requirement has many categories which one do we use then?

    def _group(self):
        for urn_id, req_data in self.cid.requirements.items():

            group = "Initial URN" if urn_id.urn == self.cid.initial_model_urn else "Imported"

            self._add_req_to_group(group=group, urn_id=urn_id)
