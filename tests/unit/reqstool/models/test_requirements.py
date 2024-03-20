# Copyright © LFV

import pytest

from reqstool.models.requirements import VARIANTS, MetaData, ReferenceData, RequirementData, RequirementsData


@pytest.fixture
def reference_data():
    return ReferenceData(requirement_ids={"REQ_001", "REQ_002"})


@pytest.fixture
def requirement_data(reference_data):
    return RequirementData(
        id="REQ_001",
        title="some title",
        significance="shall",
        description="some description",
        rationale="some rationale",
        categories=["maintainability", "functional-suitability"],
        references=[reference_data],
        revision="0.0.1",
    )


@pytest.fixture
def requirements_data(requirement_data, implementations_data, maven_import_data):
    return RequirementsData(
        metadata=MetaData(
            urn="URN_TEST",
            variant=VARIANTS.MICROSERVICE,
            title="Some document title",
            url="https://url.example.com",
        ),
        implementations=[implementations_data],
        imports={"system_urn": maven_import_data},
        requirements={"REQ_001": requirement_data},
    )


def test_reference_data(reference_data):
    assert reference_data.requirement_ids.issubset({"REQ_001", "REQ_002"})


def test_requirement_data(requirement_data, reference_data):
    assert requirement_data.id == "REQ_001"
    assert requirement_data.title == "some title"
    assert requirement_data.significance == "shall"
    assert requirement_data.description == "some description"
    assert requirement_data.rationale == "some rationale"
    assert requirement_data.categories == ["maintainability", "functional-suitability"]
    assert requirement_data.references == [reference_data]
    assert requirement_data.revision == "0.0.1"


def test_requirements_data(
    requirements_data: RequirementsData, requirement_data, implementations_data, maven_import_data
):
    assert requirements_data.metadata.urn == "URN_TEST"
    assert requirements_data.metadata.variant == VARIANTS("microservice")
    assert requirements_data.metadata.title == "Some document title"
    assert requirements_data.metadata.url == "https://url.example.com"
    assert requirements_data.implementations == [implementations_data]
    assert requirements_data.imports == {"system_urn": maven_import_data}
    assert requirements_data.requirements == {"REQ_001": requirement_data}
