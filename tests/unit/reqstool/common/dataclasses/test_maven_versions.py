# Copyright © LFV

from typing import Optional

import pytest

from reqstool.common.dataclasses.maven_version import MavenVersion


@pytest.mark.parametrize(
    "version_string, expected_major, expected_minor, expected_patch, expected_build_number, expected_qualifier, expected_snapshot",
    [
        ("1.2.3-alpha", 1, 2, 3, None, "alpha", False),
        ("1.2.3-SNAPSHOT", 1, 2, 3, None, None, True),
        ("1.2.3a1-SNAPSHOT", 1, 2, 3, None, "a1", True),
        ("1.2.3-beta1-SNAPSHOT", 1, 2, 3, None, "beta1", True),
        ("1.2.3-b2", 1, 2, 3, None, "b2", False),
        ("1.2.3-beta3", 1, 2, 3, None, "beta3", False),
        ("1.2.3-milestone1-SNAPSHOT", 1, 2, 3, None, "milestone1", True),
        ("1.2.3-rc1-SNAPSHOT", 1, 2, 3, None, "rc1", True),
        ("1.2.3-whatever", 1, 2, 3, None, "whatever", False),
        ("1.2.3", 1, 2, 3, None, None, False),
        ("1.2.3-42", 1, 2, 3, 42, None, False),
        ("1.2.3-42-SNAPSHOT", 1, 2, 3, 42, None, True),
    ],
)
def test_version_parsing(
    version_string: str,
    expected_major: int,
    expected_minor: int,
    expected_patch: int,
    expected_build_number: Optional[int],
    expected_qualifier: Optional[str],
    expected_snapshot: bool,
) -> None:
    # Instantiate MavenVersionInformation
    version_info = MavenVersion(version_string)

    # Check that the parsed version matches the expected values
    assert version_info.major == expected_major
    assert version_info.minor == expected_minor
    assert version_info.patch == expected_patch
    assert version_info.build_number == expected_build_number
    assert version_info.qualifier == expected_qualifier
    assert version_info.snapshot == expected_snapshot


def test_invalid_version() -> None:
    # Test invalid version format handling (missing minor/patch)
    with pytest.raises(ValueError):
        MavenVersion("1.2")
    with pytest.raises(ValueError):
        MavenVersion("1.2.3.4")
