# Copyright © LFV

from pathlib import PurePath

import pytest

from reqstool.requirements_indata.java.java_maven_requirements_indata_paths import JavaMavenRequirementsIndataPaths
from reqstool.requirements_indata.requirements_indata_paths import RequirementsIndataPaths


# Define a fixture to create an instance for testing
@pytest.fixture
def default_instance():
    d = RequirementsIndataPaths()

    return d


# Define a fixture for sample_instance_B
@pytest.fixture
def java_instance():
    j = JavaMavenRequirementsIndataPaths()

    return j


# Test the prepend_paths method with properties that can be None
def test_prepend_paths_with_none_properties(default_instance):
    a: RequirementsIndataPaths = default_instance
    b: RequirementsIndataPaths = default_instance

    prepend_str = "/path/to/prepend"
    a.prepend_paths(prepend_str)

    assert a.requirements_yml.path == b.requirements_yml.path
    assert a.svcs_yml.path == b.svcs_yml.path
    assert a.mvrs_yml.path == b.mvrs_yml.path
    assert a.annotations_yml.path == str(PurePath(prepend_str, b.annotations_yml.path))
    assert len(a.test_results_dirs) == 1


# Test the merge method with properties that can be None
def test_merge_with_none_properties(default_instance, java_instance):
    java_instance.ra_tests_yml = None
    java_merged_instance = default_instance.merge(java_instance)

    assert java_merged_instance.requirements_yml.path == "requirements.yml"
    assert java_merged_instance.svcs_yml.path == "software_verification_cases.yml"
    assert java_merged_instance.mvrs_yml.path == "manual_verification_results.yml"
    assert java_merged_instance.annotations_yml.path == "target/reqstool/annotations.yml"
    assert len(java_merged_instance.test_results_dirs) == 2

    expected_paths = ["target/failsafe-reports", "target/surefire-reports"]
    assert all(item.path in expected_paths for item in java_merged_instance.test_results_dirs)
