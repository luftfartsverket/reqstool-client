# Copyright © LFV

from reqstool_python_decorators.decorators.decorators import SVCs

from reqstool.common.dataclasses.urn_id import UrnId
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

    cids = CombinedIndexedDatasetGenerator(_crd=crd)

    assert cids is not None


def test_standard_baseline_ms001_no_filtering(resource_funcname_rootdir, local_testdata_resources_rootdir_w_path):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    crd: CombinedRawDataset = CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/baseline/ms-001")),
        semantic_validator=semantic_validator,
    ).combined_raw_datasets

    cids = CombinedIndexedDatasetGenerator(_crd=crd, _filtered=False).combined_indexed_dataset

    assert len(cids.requirements) == 8


@SVCs("SVC_005")
def test_standard_baseline_ms001(resource_funcname_rootdir, local_testdata_resources_rootdir_w_path):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    crd: CombinedRawDataset = CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/baseline/ms-001")),
        semantic_validator=semantic_validator,
    ).combined_raw_datasets

    cids = CombinedIndexedDatasetGenerator(_crd=crd, _filtered=True).combined_indexed_dataset

    # check reqs
    assert len(cids.requirements) == 6
    assert UrnId.instance("ms-001:REQ_010") in cids.requirements
    assert UrnId.instance("ms-001:REQ_020") in cids.requirements
    assert UrnId.instance("sys-001:REQ_sys001_505") in cids.requirements
    assert UrnId.instance("ext-001:REQ_ext001_100") in cids.requirements
    assert UrnId.instance("ext-002:REQ_ext002_300") in cids.requirements
    assert UrnId.instance("ext-002:REQ_ext002_400") in cids.requirements


def test_standard_baseline_sys001(resource_funcname_rootdir, local_testdata_resources_rootdir_w_path):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    crd: CombinedRawDataset = CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/baseline/sys-001")),
        semantic_validator=semantic_validator,
    ).combined_raw_datasets

    cids = CombinedIndexedDatasetGenerator(_crd=crd, _filtered=True).combined_indexed_dataset

    assert cids.initial_model_urn == "sys-001"
