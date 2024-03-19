# Copyright © LFV

from reqstool_python_decorators.decorators.decorators import SVCs

from reqstool.common.validator_error_holder import ValidationErrorHolder
from reqstool.common.validators.semantic_validator import SemanticValidator
from reqstool.locations.local_location import LocalLocation
from reqstool.model_generators import combined_raw_datasets_generator


@SVCs("SVC_001")
def test_basic_local(resource_funcname_rootdir, local_testdata_resources_rootdir_w_path):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    combined_raw_datasets_generator.CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_basic/baseline/ms-101")),
        semantic_validator=semantic_validator,
    )


@SVCs("SVC_001")
def test_basic_requirements_config(resource_funcname_rootdir, local_testdata_resources_rootdir_w_path):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    combined_raw_datasets_generator.CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(
            path=local_testdata_resources_rootdir_w_path("test_basic/with_requirements_config/ms-101")
        ),
        semantic_validator=semantic_validator,
    )


@SVCs("SVC_001")
def test_standard_ms001_initial(local_testdata_resources_rootdir_w_path):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())

    combined_raw_datasets_generator.CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/baseline/ms-001")),
        semantic_validator=semantic_validator,
    ).combined_raw_datasets


@SVCs("SVC_001")
def test_standard_sys001_initial(local_testdata_resources_rootdir_w_path):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    combined_raw_datasets_generator.CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/baseline/sys-001")),
        semantic_validator=semantic_validator,
    )
