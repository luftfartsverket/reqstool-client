from typing import List

from reqstool.locations.pypi_location import PypiLocation


def test_get_all_versions() -> None:
    all_versions: List[str] = PypiLocation._get_all_versions(package="reqstool", base_url="https://pypi.org/simple")

    assert len(all_versions) > 5


def test_resolve_version() -> None:
    pypi_location = PypiLocation(package="reqstool", version="latest")

    version_latest = pypi_location._resolve_version()

    assert version_latest == "0.5.9"

    pypi_location.version = "latest-stable"

    version_latest_stable = pypi_location._resolve_version()

    assert version_latest == version_latest_stable
