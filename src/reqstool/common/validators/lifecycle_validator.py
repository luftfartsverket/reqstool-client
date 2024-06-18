# Copyright © LFV

import logging
from typing import Union
from reqstool.common.dataclasses.lifecycle import LIFECYCLESTATE
from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.models.annotations import AnnotationData
from reqstool.models.combined_indexed_dataset import CombinedIndexedDataset
from reqstool.models.requirements import RequirementData
from reqstool.models.svcs import SVCData
from reqstool_python_decorators.decorators.decorators import Requirements


@Requirements("REQ_037", "REQ_038")
class LifecycleValidator:
    """
    Logs warnings if any requirement or SVC is used despite being marked deprecated or obsolete.
    """

    def __init__(self, cid: CombinedIndexedDataset):
        self._cid = cid

        self._validate()

    def _validate(self):
        self._check_defunct_annotations(self._cid.annotations_impls, self._cid.requirements)
        self._check_defunct_annotations(self._cid.annotations_tests, self._cid.svcs)
        self._check_defunct_references(self._cid.mvrs_from_svc, self._cid.svcs)
        self._check_defunct_references(self._cid.svcs_from_req, self._cid.requirements)

    def _check_defunct_annotations(
        self,
        annotations: dict[UrnId, list[AnnotationData]],
        in_collection: dict[UrnId, Union[RequirementData, SVCData]],
    ):
        for urn in annotations:
            if urn not in in_collection:
                continue
            state = in_collection[urn].lifecycle.state
            if state == LIFECYCLESTATE.DEPRECATED or LIFECYCLESTATE.OBSOLETE:
                logging.debug(f"{state.value}: {urn}")

    def _check_defunct_references(
        self, references: dict[UrnId, list[UrnId]], ref_collection: dict[UrnId, Union[SVCData, RequirementData]]
    ):
        for ref_id, related_ids in references.items():
            if ref_id not in ref_collection:
                continue
            state = ref_collection[ref_id].lifecycle.state
            if state == LIFECYCLESTATE.DEPRECATED or LIFECYCLESTATE.OBSOLETE:
                logging.debug(f"{state.value}: {self._format_list(related_ids)}")

    def _format_list(self, items: list[UrnId]):
        return ", ".join(map(str, items))
