# Copyright © LFV

import logging
import os
import sys
from dataclasses import dataclass, field
from typing import Any, Optional
from zipfile import ZipFile
from maven_artifact import Artifact, Downloader, RequestException, Resolver
from reqstool_python_decorators.decorators.decorators import Requirements
from reqstool.locations.location import LocationInterface

from lxml import etree


@Requirements("REQ_003", "REQ_017")
@dataclass(kw_only=True)
class MavenLocation(LocationInterface):
    url: Optional[str] = "https://repo.maven.apache.org/maven2"
    group_id: str
    artifact_id: str
    version: str  # Can be "latest", "latest-stable", "latest-unstable", or specific version
    classifier: str = field(default="reqstool")
    env_token: str

    def _get_versions(self, resolver: Resolver, artifact: Artifact) -> Any:
        """Get all available versions for the artifact."""
        try:
            # Construct Maven metadata path
            group_path = artifact.group_id.replace("/", ".")  # Convert slashes to dots first
            group_path = group_path.replace(".", "/")  # Then convert dots to slashes
            path = f"/{group_path}/{artifact.artifact_id}/maven-metadata.xml"

            xml = resolver.requestor.request(
                resolver.base + path, resolver._onFail, lambda r: etree.fromstring(r.content)
            )
            all_versions = xml.xpath("/metadata/versioning/versions/version/text()")

            if not all_versions:
                raise RequestException(f"No versions found for {artifact}")

            return all_versions
        except Exception as e:
            raise RequestException(f"Failed to get versions for {artifact}: {str(e)}")

    def _resolve_version(self, resolver: Resolver, base_artifact: Artifact) -> str:
        """Resolve version based on version specifier."""
        if self.version == "latest":
            versions = self._get_versions(resolver, base_artifact)
            if not versions:
                raise RequestException(f"No versions found for {self.group_id}:{self.artifact_id}")
            return versions[-1]

        if self.version not in ["latest-stable", "latest-unstable"]:
            return self.version

        versions = self._get_versions(resolver, base_artifact)
        is_stable = self.version == "latest-stable"
        filtered_versions = [v for v in versions if v.endswith("-SNAPSHOT") != is_stable]

        if not filtered_versions:
            version_type = "stable" if is_stable else "unstable"
            raise RequestException(f"No {version_type} versions found for {self.group_id}:{self.artifact_id}")

        return filtered_versions[-1]

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
        token = os.getenv(self.env_token)
        downloader = Downloader(base=self.url, token=token)
        resolver = downloader.resolver

        try:
            base_artifact = Artifact(
                group_id=self.group_id, version=self.version, artifact_id=self.artifact_id, classifier=self.classifier
            )
            version = self._resolve_version(resolver, base_artifact)

            artifact = Artifact(
                group_id=self.group_id,
                artifact_id=self.artifact_id,
                version=version,
                classifier=self.classifier,
                extension="zip",
            )
            resolved_artifact = resolver.resolve(artifact)

            if resolved_artifact.version != version:
                logging.debug(f"Resolved version '{version}' to: {resolved_artifact.version}")

            if not downloader.download(resolved_artifact, filename=dst_path):
                raise RequestException(f"Error downloading artifact {resolved_artifact} from: {self.url}")

            return self._extract_zip(resolved_artifact.get_filename(dst_path), dst_path)

        except RequestException as e:
            logging.fatal(str(e))
            sys.exit(1)
        except Exception as e:
            logging.fatal(f"Unexpected error: {str(e)}")
            sys.exit(1)
