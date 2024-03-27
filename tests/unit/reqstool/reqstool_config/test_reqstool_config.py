# Copyright © LFV


import pytest
from pytest import fixture
from ruamel.yaml import YAML

from reqstool.reqstool_config.reqstool_config import TYPES, ReqstoolConfig


@fixture
def rc_yaml_config_all() -> dict:
    YAML_STR = """
    type: java-maven

    project_root_dir: /some_root_dir

    locations:
      annotations: custom_annotations.yml
      test_results_dirs:
        - target/failsafe
        - target/surefire
    """
    yaml = YAML(typ="safe")
    data = yaml.load(YAML_STR)

    return data


@fixture
def rc_yaml_config_minimal() -> dict:
    YAML_STR = """
    type: java-maven
    """
    yaml = YAML(typ="safe")
    data = yaml.load(YAML_STR)

    return data


@fixture
def rc_yaml_config_incorrect_type() -> dict:
    YAML_STR = """
    type: java-maven-docs
    """
    yaml = YAML(typ="safe")
    data = yaml.load(YAML_STR)

    return data


def test_all(rc_yaml_config_all):
    rc = ReqstoolConfig._parse(yaml_data=rc_yaml_config_all)

    assert rc.type == TYPES.JAVA_MAVEN
    assert rc.project_root_dir == "/some_root_dir"
    assert rc.locations.annotations == "custom_annotations.yml"
    assert rc.locations.test_results[0] == "target/failsafe"
    assert rc.locations.test_results[1] == "target/surefire"


def test_minimal(rc_yaml_config_minimal):
    rc = ReqstoolConfig._parse(yaml_data=rc_yaml_config_minimal)

    assert rc.type == TYPES.JAVA_MAVEN


def test_incorrect_type(rc_yaml_config_incorrect_type):
    with pytest.raises(ValueError, match="'java-maven-docs' is not a valid TYPES"):
        ReqstoolConfig._parse(yaml_data=rc_yaml_config_incorrect_type)
