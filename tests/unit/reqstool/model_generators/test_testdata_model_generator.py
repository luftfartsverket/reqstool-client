# Copyright © LFV

import re

import pytest
from reqstool_python_decorators.decorators.decorators import SVCs

from reqstool.model_generators.testdata_model_generator import TestDataModelGenerator

karate_method_names = [
    "[1.4:55] Create a subscripiton with filter and receive messages",
    "[1:38] Create a subscripiton with filter and receive messages",
    "[1.2:53] Create a subscripiton with filter and receive messages",
]

unit_method_names = [
    "testFlightIdAircraftId",
    "testFlightIdAircraftId(String, int)[1]",
]


@SVCs("SVC_006")
@pytest.mark.parametrize("method_name", karate_method_names)
def test_karate_method_identifier_regex(method_name):
    karate_match = re.match(TestDataModelGenerator.KARATE_METHOD_IDENTIFIER_REGEX, method_name)
    assert karate_match is not None
    assert karate_match.group(1) == "Create a subscripiton with filter and receive messages"


@SVCs("SVC_007")
@pytest.mark.parametrize("method_name", unit_method_names)
def test_unit_method_identifier_regex(method_name):
    unit_match = re.match(TestDataModelGenerator.UNIT_METHOD_IDENTIFIER_REGEX, method_name)
    assert unit_match is not None
    assert unit_match.group(1) == "testFlightIdAircraftId"


def test_testdata_model_generator(local_testdata_resources_rootdir_w_path):
    # TODO:
    # * Test the different variants: passed, skipped, failure etc
    # * Test different types of file structure (Java, Python, Frontend Typescript)

    tdmg = (
        TestDataModelGenerator(path=local_testdata_resources_rootdir_w_path("test_basic/baseline/ms-101"), urn="test"),
    )

    assert tdmg is not None
