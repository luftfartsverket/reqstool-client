# Copyright © LFV

import os

import pytest

from reqstool.common.validator_error_holder import ValidationErrorHolder
from reqstool.common.validators.semantic_validator import SemanticValidator
from reqstool.locations.git_location import GitLocation
from reqstool.locations.maven_location import MavenLocation
from reqstool.model_generators import combined_raw_datasets_generator


def choose_token() -> str:
    if os.getenv("GITHUB_TOKEN"):
        return "GITHUB_TOKEN"
    else:
        return "GITLAB_TOKEN"


@pytest.mark.skipif(
    not (os.getenv("GITHUB_TOKEN") or os.getenv("GITLAB_TOKEN")),
    reason="Test needs GITLAB_TOKEN or GITLAB environment variable to be set",
)
def test_basic_git():
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())

    combined_raw_datasets_generator.CombinedRawDatasetsGenerator(
        initial_location=GitLocation(
            env_token=choose_token(),
            url="https://github.com/Luftfartsverket/reqstool-client.git",
            path="tests/resources/test_data/data/remote/test_standard/test_standard_maven_git/ms-001",
            branch="main",
        ),
        semantic_validator=semantic_validator,
    )


@pytest.mark.skipif(
    not (os.getenv("GITHUB_TOKEN") or os.getenv("GITLAB_TOKEN")),
    reason="Test needs GITLAB_TOKEN or GITHUB_TOKEN environment variable to be set",
)
def test_basic_maven():
    semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())

    artifact_id: str = "reqstool-testdata-test-basic-ms101"
    version: str = "0.0.2"

    combined_raw_datasets_generator.CombinedRawDatasetsGenerator(
        # Setup
        initial_location=MavenLocation(
            env_token=choose_token(),
            url="https://",
            path="https://maven.pkg.github.com/Luftfartsverket/reqstool-client",
            group_id="se.lfv.reqstool.testdata",
            artifact_id=artifact_id,
            version=version,
            classifier="reqstool",
        ),
        semantic_validator=semantic_validator,
    )