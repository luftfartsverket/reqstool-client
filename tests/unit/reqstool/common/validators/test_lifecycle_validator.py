# Copyright © LFV

import pytest
from reqstool.common.validator_error_holder import ValidationErrorHolder
from reqstool.common.validators.lifecycle_validator import LifecycleValidator
from reqstool.common.validators.semantic_validator import SemanticValidator
from reqstool.locations.local_location import LocalLocation
from reqstool.model_generators.combined_indexed_dataset_generator import CombinedIndexedDatasetGenerator
from reqstool.model_generators.combined_raw_datasets_generator import CombinedRawDatasetsGenerator
from reqstool.models.raw_datasets import CombinedRawDataset
from reqstool_python_decorators.decorators.decorators import SVCs


@pytest.fixture
def combined_indexed_dataset(local_testdata_resources_rootdir_w_path):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    crd: CombinedRawDataset = CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_basic/lifecycle/ms-101")),
        semantic_validator=semantic_validator,
    ).combined_raw_datasets

    return CombinedIndexedDatasetGenerator(_crd=crd).combined_indexed_dataset


@SVCs("SVC_038")
def test_defunct_states(combined_indexed_dataset, caplog):

    LifecycleValidator(combined_indexed_dataset)

    assert "deprecated: UrnId(urn='ms-101', id='REQ_101')" in caplog.text
    assert "deprecated: UrnId(urn='ms-101', id='SVC_101')" in caplog.text
    assert "obsolete: UrnId(urn='ms-101', id='SVC_102')" in caplog.text
    assert "deprecated: UrnId(urn='ms-101', id='SVC_101')" in caplog.text
    assert "obsolete: UrnId(urn='ms-101', id='SVC_102')" in caplog.text
    assert "deprecated: UrnId(urn='ms-101', id='REQ_101')" in caplog.text
    assert "deprecated: UrnId(urn='ms-101', id='SVC_101')" in caplog.text
    assert "obsolete: UrnId(urn='ms-101', id='SVC_102')" in caplog.text
    assert "deprecated: UrnId(urn='ms-101', id='SVC_101')" in caplog.text
    assert "obsolete: UrnId(urn='ms-101', id='SVC_102')" in caplog.text


@SVCs("SVC_038")
def test_active_states(combined_indexed_dataset, caplog):

    LifecycleValidator(combined_indexed_dataset)

    assert "draft: UrnId(urn='ms-101', id='REQ_201')" not in caplog.text
    assert "draft: UrnId(urn='ms-101', id='MVR_201')" not in caplog.text
    assert "effective: UrnId(urn='ms-101', id='MVR_202')" not in caplog.text
    assert "draft: UrnId(urn='ms-101', id='SVC_201')" not in caplog.text
    assert "effective: UrnId(urn='ms-101', id='SVC_202')" not in caplog.text
    assert "draft: UrnId(urn='ms-101', id='REQ_201')" not in caplog.text
    assert "draft: UrnId(urn='ms-101', id='MVR_201')" not in caplog.text
    assert "effective: UrnId(urn='ms-101', id='MVR_202')" not in caplog.text
    assert "draft: UrnId(urn='ms-101', id='SVC_201')" not in caplog.text
    assert "effective: UrnId(urn='ms-101', id='SVC_202')" not in caplog.text


@SVCs("SVC_038")
def test_invalid_schema(local_testdata_resources_rootdir_w_path, caplog):
    with pytest.raises(SystemExit) as excinfo:
        semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
        CombinedRawDatasetsGenerator(
            initial_location=LocalLocation(
                path=local_testdata_resources_rootdir_w_path("test_basic/lifecycle/validation_error")
            ),
            semantic_validator=semantic_validator,
        ).combined_raw_datasets

    assert excinfo.type == SystemExit
    # 128 schema validation error
    assert str(excinfo.value) == "128"
    assert "'reason' is a required property" in caplog.text
