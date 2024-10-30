# Copyright © LFV

from pytest import fixture
from ruamel.yaml import YAML

from reqstool.reqstool_config.reqstool_config import ReqstoolConfig


@fixture
def rc_yaml_index_all() -> dict:
    YAML_STR = """
    language: python
    build: hatch
    resources:
        requirements: reqstool/requirements.yml
        software_verification_cases: reqstool/software_verification_cases.yml
        manual_verification_results: reqstool/manual_verification_results.yml
        annotations: build/reqstool/annotations.yml
        test_results:
            - build/junit.xml
    """
    yaml = YAML(typ="safe")
    data = yaml.load(YAML_STR)
    return data


@fixture
def rc_yaml_index_minimal() -> dict:
    YAML_STR = """
    resources:
        annotations: build/reqstool/annotations.yml
        test_results:
            - build/junit.xml
    """
    yaml = YAML(typ="safe")
    data = yaml.load(YAML_STR)
    return data


def test_all(rc_yaml_index_all):
    rc = ReqstoolConfig._parse(yaml_data=rc_yaml_index_all)

    # Access attributes directly instead of subscripting
    assert rc.language == "python"
    assert rc.build == "hatch"
    assert rc.resources.requirements == "reqstool/requirements.yml"
    assert rc.resources.software_verification_cases == "reqstool/software_verification_cases.yml"
    assert rc.resources.manual_verification_results == "reqstool/manual_verification_results.yml"
    assert rc.resources.annotations == "build/reqstool/annotations.yml"
    assert len(rc.resources.test_results) == 1
    assert "build/junit.xml" in rc.resources.test_results


def test_minimal(rc_yaml_index_minimal):
    rc = ReqstoolConfig._parse(yaml_data=rc_yaml_index_minimal)

    # Access attributes directly
    assert rc.language is None
    assert rc.build is None
    assert rc.resources.requirements is None
    assert rc.resources.software_verification_cases is None
    assert rc.resources.manual_verification_results is None
    assert rc.resources.annotations == "build/reqstool/annotations.yml"
    assert len(rc.resources.test_results) == 1
    assert "build/junit.xml" in rc.resources.test_results
