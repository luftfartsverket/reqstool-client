# Copyright © LFV

import pytest
from reqstool_python_decorators.decorators.decorators import SVCs

from reqstool.common.validators.semantic_validator import SemanticValidator, ValidationErrorHolder
from reqstool.locations.local_location import LocalLocation
from reqstool.model_generators import combined_raw_datasets_generator


@pytest.fixture
def get_validation(resource_funcname_rootdir, local_testdata_resources_rootdir_w_path):
    holder = ValidationErrorHolder()
    semantic_validator = SemanticValidator(validation_error_holder=holder)
    img = combined_raw_datasets_generator.CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_errors/ms-101")),
        semantic_validator=semantic_validator,
    )

    return img.combined_raw_datasets


@pytest.fixture
def get_svcs_data_raw():
    # Data is raw since it's parsed directly from yaml data at runtime
    data = {
        "filters": {
            "sys-001": {"svc_ids": {"includes": ["SVC_sys001_101", "SVC_sys001_109"], "excludes": ["SVC_sys001_101"]}}
        },
        "cases": {},
    }
    return data


@pytest.fixture
def get_systems_data_raw():
    # Data is raw since it's parsed directly from yaml data at runtime
    data = {
        "path": "../sys-001",
        "filters": {"sys-001": {"requirement_ids": {"includes": ["REQ_sys001_101"], "excludes": ["REQ_sys001_102"]}}},
    }

    return data


@pytest.fixture
def get_requirements_data_raw():
    # Data is raw since it's parsed directly from yaml data at runtime
    data = {
        "metadata": {
            "urn": "ms-001",
            "variant": "microservice",
            "title": "Some Microservice Requirement Title",
            "url": "https://url.example.com",
        },
        "systems": {
            "local": [
                {
                    "path": "../sys-001",
                    "filters": {
                        "sys-001": {"requirement_ids": {"includes": ["REQ_sys001_103", "ext001:REQ_ext003_101"]}}
                    },
                }
            ]
        },
        "requirements": [
            {
                "id": "REQ_ms001_101",
                "title": "Title REQ_ms001_101",
                "significance": "may",
                "description": "Description REQ_ms001_101",
                "rationale": "Rationale REQ_ms001_101",
                "categories": ["maintainability", "functional-suitability"],
                "revision": "0.0.1",
            },
            {
                "id": "REQ_ms001_101",
                "title": "Title REQ_ms001_102",
                "significance": "may",
                "description": "Some description REQ_ms001_102",
                "rationale": "Rationale REQ_ms001_102",
                "categories": ["maintainability", "functional-suitability"],
                "references": {"requirement_ids": ["sys-001:REQ_sys001_101"]},
                "revision": "0.0.1",
            },
        ],
    }

    return data


@pytest.fixture
def get_svc_data():
    # Data is raw since it's parsed directly from yaml data at runtime
    data = {
        "filters": {"sys-001": {"svc_ids": {"includes": ["SVC_sys001_101", "SVC_sys001_109"]}}},
        "cases": [
            {
                "id": "SVC_ms001_101",
                "requirement_ids": ["REQ_ms001_101"],
                "title": "Some Title SVC_ms001_101",
                "verification": "automated-test",
                "revision": "0.0.1",
            },
            {
                "id": "SVC_ms001_101",
                "requirement_ids": ["REQ_ms001_102"],
                "title": "Some Title SVC_ms001_102",
                "verification": "manual-test",
                "revision": "0.0.1",
            },
            {
                "id": "SVC_ms001_103",
                "requirement_ids": ["sys-001:REQ_sys001_103"],
                "title": "Some Title SVC_ms001_103",
                "description": "Some Description SVC_ms001_103",
                "verification": "automated-test",
                "instructions": "Some instructions",
                "revision": "0.0.2",
            },
        ],
    }

    return data


def test_basic_validation(resource_funcname_rootdir, local_testdata_resources_rootdir_w_path):
    holder = ValidationErrorHolder()
    semantic_validator = SemanticValidator(validation_error_holder=holder)

    img = combined_raw_datasets_generator.CombinedRawDatasetsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_errors/ms-101")),
        semantic_validator=semantic_validator,
    )

    assert img.combined_raw_datasets.raw_datasets

    errors = semantic_validator._validation_error_holder.get_errors()

    assert len(errors) == 7


@SVCs("SVC_016")
def test_validate_no_duplicate_reqs(get_requirements_data_raw):
    holder = ValidationErrorHolder()
    semantic_validator = SemanticValidator(validation_error_holder=holder)
    has_errors = semantic_validator._validate_no_duplicate_requirement_ids(get_requirements_data_raw)
    assert has_errors is True


@SVCs("SVC_017")
def test_validate_no_duplicate_svcs(get_svc_data):
    holder = ValidationErrorHolder()
    semantic_validator = SemanticValidator(validation_error_holder=holder)
    has_errors = semantic_validator._validate_no_duplicate_svc_ids(get_svc_data)
    assert has_errors is True


@SVCs("SVC_018")
def test_validate_svc_to_existing_reqs(get_validation):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    errors = semantic_validator._validate_svc_refers_to_existing_requirement_ids(get_validation)
    expected_error = """SVC '<ms-101:SVC_201>' refers to
                                    non-existing requirement id: <ms-101:REQ_20101>"""
    assert expected_error in errors[0].msg


@SVCs("SVC_018")
def test_validate_impls_to_existing_reqs(get_validation):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    errors = semantic_validator._validate_annotation_impls_refers_to_existing_requirement_ids(get_validation)
    expected_error = """Annotation refers to
                            non-existing requirement id: <ms-101:REQ_10101>"""
    assert expected_error in errors[0].msg


@SVCs("SVC_019")
def test_validate_tests_to_existing_svcs(get_validation):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    errors = semantic_validator._validate_annotation_tests_refers_to_existing_svc_ids(get_validation)
    expected_error_1 = "Annotation refers to non-existing svc id: <ms-101:SVC_101121>"
    expected_error_2 = "Annotation refers to non-existing svc id: <ms-101:SVC_102>"
    assert expected_error_1 in errors[0].msg
    assert expected_error_2 in errors[1].msg


@SVCs("SVC_019")
def test_validate_mvrs_to_existing_svcs(get_validation):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    errors = semantic_validator._validate_mvr_refers_to_existing_svc_ids(get_validation)
    expected_error = "MVR refers to non-existing svc id: <ms-101:SVC_20111>"
    assert expected_error in errors[0].msg


def test_validate_svc_filter_exlude_xor_import(get_svcs_data_raw):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    has_errors = semantic_validator._validate_svc_imports_filter_has_excludes_xor_includes(get_svcs_data_raw)
    expected_error = "Both imports and exclude filters applied to svc! (urn: sys-001)"
    errors = semantic_validator._validation_error_holder.get_errors()
    assert has_errors > 0
    assert expected_error in errors[0].msg


def test_validate_req_filter_exlude_xor_import(get_systems_data_raw):
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
    has_errors = semantic_validator._validate_req_imports_filter_has_excludes_xor_includes(get_systems_data_raw)
    expected_error = "Both imports and exclude filters applied to req! (urn: sys-001)"
    errors = semantic_validator._validation_error_holder.get_errors()
    assert has_errors > 0
    assert expected_error in errors[0].msg
