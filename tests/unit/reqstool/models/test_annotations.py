# Copyright © LFV

import pytest

from reqstool.models import annotations as ra


@pytest.fixture
def requirement_annotation_data():
    return ra.AnnotationData(element_kind="CLASS", fully_qualified_name="com.example.class")


@pytest.fixture
def requirements_annotations_data(requirement_annotation_data):
    implementations = {"REQ_001": [requirement_annotation_data], "REQ_002": [requirement_annotation_data]}
    tests = {"REQ_001": [requirement_annotation_data]}

    return ra.AnnotationsData(implementations=implementations, tests=tests)


def test_requirement_annotation_data(requirement_annotation_data):
    assert requirement_annotation_data.element_kind == "CLASS"
    assert requirement_annotation_data.fully_qualified_name == "com.example.class"


def test_requirements_annotations_data(requirements_annotations_data):
    assert len(requirements_annotations_data.implementations) == 2
    assert len(requirements_annotations_data.tests) == 1
