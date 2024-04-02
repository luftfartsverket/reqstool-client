# Copyright © LFV

import logging
import os
import sys
from dataclasses import dataclass
from zipfile import ZipFile

from maven_artifact import Artifact, Downloader, RequestException, Utils
from reqstool_python_decorators.decorators.decorators import Requirements

from reqstool.locations.location import LocationInterface


@Requirements("REQ_003", "REQ_017")
@dataclass(kw_only=True)
class MavenLocation(LocationInterface):
    url: str
    group_id: str
    artifact_id: str
    version: str
    classifier: str = "requirements"
    env_token: str

    def _make_available_on_localdisk(self, dst_path: str):
        token = os.getenv(self.env_token)

        # if base65 encoded assume username:password
        if Utils.is_base64(token):
            downloader = Downloader(base=self.url, password=token)
        # assume OAuth Bearer
        else:
            downloader = Downloader(base=self.url, token=token)

        artifact = Artifact(
            group_id=self.group_id,
            artifact_id=self.artifact_id,
            version=self.version,
            classifier=self.classifier,
            extension="zip",
        )

        logging.debug(f"Downloading {artifact} from {self.url} to {dst_path}\n")

        try:
            if not downloader.download(artifact, filename=dst_path):
                raise RequestException(f"Error downloading artifact {artifact} from: {self.url}")
        except RequestException as e:
            logging.fatal(e.msg)
            sys.exit(1)

        logging.debug(f"Unzipping {artifact.get_filename(dst_path)} to {dst_path}\n")

        with ZipFile(artifact.get_filename(dst_path), "r") as zip_ref:
            # Extracting all the members of the zip
            # into a specific location.
            zip_ref.extractall(path=dst_path)

        # os.remove(artifact.get_filename(dst_path))

        logging.debug(f"Unzipped {artifact.get_filename(dst_path)} to {dst_path}\n")
