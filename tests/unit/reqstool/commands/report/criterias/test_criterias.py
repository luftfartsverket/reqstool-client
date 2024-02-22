# Copyright © LFV

from reqstool.commands.report.criterias.group_by.group_by_category import GroupByCategory
from reqstool.commands.report.criterias.sort_by.sort_by_id_alphanumerical import SortByIdAlphanumerical
from reqstool.common.validator_error_holder import ValidationErrorHolder
from reqstool.common.validators.semantic_validator import SemanticValidator
from reqstool.locations.local_location import LocalLocation
from reqstool.model_generators.combined_indexed_dataset_generator import CombinedIndexedDatasetGenerator
from reqstool.model_generators.combined_raw_datasets_generator import CombinedRawDatasetsGenerator
from reqstool.models.raw_datasets import CombinedRawDataset


def test_basic_baseline(resource_funcname_rootdir, local_testdata_resources_rootdir_w_path):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    crd: CombinedRawDataset = CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_basic/baseline/ms-101")),
        semantic_validator=semantic_validator,
    ).combined_raw_datasets

    cid = CombinedIndexedDatasetGenerator(_crd=crd).combined_indexed_dataset

    gbc = GroupByCategory(cid=cid, sort_by=SortByIdAlphanumerical(cid=cid))

    for key, value in gbc:
        print(f"{key}:{value}")

    assert gbc is not None
