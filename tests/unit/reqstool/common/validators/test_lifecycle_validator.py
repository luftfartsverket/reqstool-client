# Copyright © LFV

from reqstool.common.validator_error_holder import ValidationErrorHolder
from reqstool.common.validators.lifecycle_validator import LifecycleValidator
from reqstool.common.validators.semantic_validator import SemanticValidator
from reqstool.locations.local_location import LocalLocation
from reqstool.model_generators.combined_indexed_dataset_generator import CombinedIndexedDatasetGenerator
from reqstool.model_generators.combined_raw_datasets_generator import CombinedRawDatasetsGenerator
from reqstool.models.raw_datasets import CombinedRawDataset
from reqstool_python_decorators.decorators.decorators import SVCs


@SVCs("SVC_038")
def test_defunct_states(caplog, local_testdata_resources_rootdir_w_path):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    crd: CombinedRawDataset = CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_basic/lifecycle/ms-101")),
        semantic_validator=semantic_validator,
    ).combined_raw_datasets

    cids = CombinedIndexedDatasetGenerator(_crd=crd)

    LifecycleValidator(cids.combined_indexed_dataset)

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
