# Copyright © LFV

from maven_artifact import Downloader, Resolver

from reqstool.locations.maven_location import MavenLocation


def test_maven_location() -> None:
    maven_location = MavenLocation(
        group_id="se/lfv/reqstool",
        artifact_id="reqstool-maven-plugin",
        version="0.1.0",
        env_token="TOKEN",
    )
    token = "TOKEN"
    downloader = Downloader(base="https://repo.maven.apache.org/maven2", token=token)
    resolver = Resolver(base="https://repo.maven.apache.org/maven2", requestor=downloader.requestor)

    version = maven_location._resolve_version(resolver=resolver)

    assert version == "0.1.0"

    maven_location.version = "latest"

    latest_version = maven_location._resolve_version(
        resolver=resolver,
    )

    # Need to get the latest version instead of hardcoding "1.0.0" here as this test will break as soon as there is a new
    # version of the maven plugin
    assert latest_version == "1.0.0"


# Test to simply run the function, seems to be working but there is no reqstool.zip
# in the artifact so it fails when trying to access it.

# def test_make_available_on_localdisc() -> None:
#     maven_location = MavenLocation(
#         group_id="se/lfv/reqstool",
#         artifact_id="reqstool-maven-plugin",
#         version="latest-stable",
#         env_token="TOKEN",
#     )

#     versions = maven_location._make_available_on_localdisk(dst_path=".")
#     # Filter stable versions and get latest
#     stable_versions = [v for v in versions if not v.endswith("-SNAPSHOT")]
#     if stable_versions:
#         maven_location.version = stable_versions[-1]  # Update the version

#     assert maven_location.version == "1.0.0"
