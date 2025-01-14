# Copyright © LFV

import logging
import os
from dataclasses import dataclass, field
from typing import List, Optional

from lxml import etree
from maven_artifact import Artifact, RequestException, Resolver
from reqstool_python_decorators.decorators.decorators import Requirements

from reqstool.common.dataclasses.maven_version import MavenVersion
from reqstool.locations.location import LocationInterface


@Requirements("REQ_003", "REQ_017")
@dataclass(kw_only=True)
class MavenLocation(LocationInterface):
    url: Optional[str] = "https://repo.maven.apache.org/maven2"
    group_id: str
    artifact_id: str
    version: str  # Can be "latest", "latest-stable", "latest-unstable", or specific version
    classifier: str = field(default="reqstool")
    env_token: Optional[str]
    token: Optional[str] = field(init=False, default=None)

    def __post_init__(self) -> None:
        # Retrieve token from environment variable
        self.token = os.getenv(self.env_token) if self.env_token else None

        if self.token:
            logging.debug("Using OAuth Bearer token for authentication")

    def _get_all_versions(self, resolver: Resolver, artifact: Artifact) -> List[str]:
        """Get all available versions for the artifact."""
        try:
            # Construct Maven metadata path
            group_path: str = artifact.group_id.replace("/", ".")  # Convert slashes to dots first
            group_path: str = group_path.replace(".", "/")  # Then convert dots to slashes
            path = f"/{group_path}/{artifact.artifact_id}/maven-metadata.xml"

            xml = resolver.requestor.request(
                resolver.base + path, resolver._onFail, lambda r: etree.fromstring(r.content)
            )
            all_versions: List[str] = xml.xpath("/metadata/versioning/versions/version/text()")

            if not all_versions:
                raise RequestException(f"No versions found for {artifact}")

            return all_versions
        except Exception as e:
            raise RequestException(f"Failed to get versions for {artifact}: {str(e)}")

    def _resolve_version(self, resolver: Resolver) -> str:
        """Resolve version based on version specifier."""

        if self.version not in ["latest", "latest-stable", "latest-unstable"]:
            return self.version

        base_artifact: Artifact = Artifact(
            group_id=self.group_id, version=self.version, artifact_id=self.artifact_id, classifier=self.classifier
        )

        all_versions: List[str] = self._get_all_versions(resolver, base_artifact)

        if self.version == "latest":
            return all_versions[-1]

        is_stable = self.version == "latest-stable"
        mv: MavenVersion
        filtered_versions: List[MavenVersion] = [
            mv
            for v in all_versions
            if (mv := MavenVersion(version=v)) and ((bool(mv.qualifier) or mv.snapshot) != is_stable)
        ]

        # no matching version found
        if not filtered_versions:
            version_type: str = "stable" if is_stable else "unstable"
            raise RequestException(f"No {version_type} versions found for {self.group_id}:{self.artifact_id}")

        return filtered_versions[-1].version

    def _extract_zip(self, zip_file: str, dst_path: str) -> str:
        """Extract ZIP file and return top level directory."""
        logging.debug(f"Unzipping {zip_file} to {dst_path}")
        with ZipFile(zip_file, "r") as zip_ref:
            top_level_dirs = {name.split("/")[0] for name in zip_ref.namelist() if "/" in name}
            zip_ref.extractall(path=dst_path)

        if len(top_level_dirs) != 1:
            raise RequestException(
                f"Maven zip artifact does not have one and only one top level directory: {top_level_dirs}"
            )

        top_level_dir = os.path.join(dst_path, top_level_dirs.pop())
        logging.debug(f"Unzipped {zip_file} to {top_level_dir}")
        return top_level_dir

    def _make_available_on_localdisk(self, dst_path: str) -> str:
        downloader = Downloader(base=self.url, token=self.token)
        resolver = downloader.resolver

        try:
            resolved_version: str = self._resolve_version(resolver)

            artifact: Artifact = Artifact(
                group_id=self.group_id,
                artifact_id=self.artifact_id,
                version=resolved_version,
                classifier=self.classifier,
                extension="zip",
            )
            resolved_artifact: Artifact = resolver.resolve(artifact)

            if resolved_artifact.version != resolved_version:
                logging.debug(f"Resolved version '{self.version}' to: {resolved_artifact.version}")

            if not downloader.download(resolved_artifact, filename=dst_path):
                raise RequestException(f"Error downloading artifact {resolved_artifact} from: {self.url}")

            return self._extract_zip(resolved_artifact.get_filename(dst_path), dst_path)

        except RequestException as e:
            logging.fatal(str(e))
            sys.exit(1)
        except Exception as e:
            logging.fatal(f"Unexpected error: {str(e)}")
            sys.exit(1)
