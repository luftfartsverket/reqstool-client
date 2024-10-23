# Copyright © LFV

import pytest
from pytest import fixture
from ruamel.yaml import YAML

from reqstool.reqstool_index.reqstool_index import BUILD_TOOL_TYPES, LANGUAGE_TYPES, ReqstoolIndex

# XXXyaml-language-server: $schema=file:///home/u30576/dev/clones/github/Luftfartsverket/reqstool-client/src/reqstool/resources/schemas/v1/reqstool_index.schema.json


@fixture
def ri_yaml_index_all() -> dict:
    YAML_STR = """
    language: python
    build: hatch
    version: 0.4.2.dev16
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
def ri_yaml_index_minimal() -> dict:
    YAML_STR = """
    language: python
    build: hatch
    version: 0.4.2.dev16
    resources:
        requirements: reqstool/requirements.yml
    """
    yaml = YAML(typ="safe")
    data = yaml.load(YAML_STR)
    return data


@fixture
def ri_yaml_index_incorrect_type() -> dict:
    YAML_STR = """
    language: none
    build: hatch
    version: 0.4.2.dev16
    resources:
        requirements: reqstool/requirements.yml
    """
    yaml = YAML(typ="safe")
    data = yaml.load(YAML_STR)
    return data


@fixture
def ri_yaml_index_invalid_combination() -> dict:
    YAML_STR = """
    language: javascript
    build: hatch
    version: 0.4.2.dev16
    resources:
        requirements: reqstool/requirements.yml
    """
    yaml = YAML(typ="safe")
    data = yaml.load(YAML_STR)
    return data


def test_all(ri_yaml_index_all):
    ri = ReqstoolIndex._parse(yaml_data=ri_yaml_index_all)

    # Access attributes directly instead of subscripting
    assert ri.language == LANGUAGE_TYPES.PYTHON
    assert ri.build == BUILD_TOOL_TYPES.HATCH
    assert ri.version == "0.4.2.dev16"
    assert ri.resources.requirements == "reqstool/requirements.yml"
    assert ri.resources.software_verification_cases == "reqstool/software_verification_cases.yml"


def test_minimal(ri_yaml_index_minimal):
    ri = ReqstoolIndex._parse(yaml_data=ri_yaml_index_minimal)

    # Access attributes directly
    assert ri.language == LANGUAGE_TYPES.PYTHON
    assert ri.build == BUILD_TOOL_TYPES.HATCH
    assert ri.version == "0.4.2.dev16"
    assert ri.resources.requirements == "reqstool/requirements.yml"
    assert ri.resources.software_verification_cases is None
    assert ri.resources.manual_verification_results is None
    assert ri.resources.annotations is None


def test_incorrect_type(ri_yaml_index_incorrect_type):
    with pytest.raises(ValueError, match="'none' is not a valid LANGUAGE_TYPES"):
        ReqstoolIndex._parse(yaml_data=ri_yaml_index_incorrect_type)


@pytest.mark.skip(reason="Combinations of language and build tool are not checked yet")
def test_invalid_combination(ri_yaml_index_invalid_combination):
    pass
