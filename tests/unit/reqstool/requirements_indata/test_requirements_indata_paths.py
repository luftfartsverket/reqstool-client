# Copyright © LFV


import pytest

from reqstool.requirements_indata.requirements_indata_paths import RequirementsIndataPaths


# Define a fixture to create an instance for testing
@pytest.fixture
def default_instance():
    d = RequirementsIndataPaths()

    return d


# Test the prepend_paths method with properties that can be None
def test_prepend_paths_with_none_properties(default_instance):
    rip: RequirementsIndataPaths = default_instance

    assert rip.requirements_yml.path == "requirements.yml"
    assert rip.svcs_yml.path == "software_verification_cases.yml"
    assert rip.mvrs_yml.path == "manual_verification_results.yml"
    assert rip.annotations_yml.path == "annotations.yml"
    assert len(rip.test_results) == 1
    assert rip.test_results[0].path == "test_results"


# # Test the merge method with properties that can be None
# def test_merge_with_none_properties(default_instance, java_instance):
#     java_instance.ra_tests_yml = None
#     java_merged_instance = default_instance.merge(java_instance)

#     assert java_merged_instance.requirements_yml.path == "requirements.yml"
#     assert java_merged_instance.svcs_yml.path == "software_verification_cases.yml"
#     assert java_merged_instance.mvrs_yml.path == "manual_verification_results.yml"
#     assert java_merged_instance.annotations_yml.path == "target/reqstool/annotations.yml"
#     assert len(java_merged_instance.test_results_dirs) == 2

#     expected_paths = ["target/failsafe-reports", "target/surefire-reports"]
#     assert all(item.path in expected_paths for item in java_merged_instance.test_results_dirs)
