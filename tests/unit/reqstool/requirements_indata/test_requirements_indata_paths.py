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
