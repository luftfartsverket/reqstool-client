# Copyright © LFV

import logging
import os
import re
from dataclasses import dataclass
from typing import List, Optional

import pygit2
from attrs import field
from pygit2 import RemoteCallbacks, UserPass, clone_repository
from reqstool_python_decorators.decorators.decorators import Requirements

from reqstool.locations.location import LocationInterface

RE_GIT_TAG_VERSION: re.Pattern[str] = re.compile(
    r"(?:^v)?(?P<version>\d+\.\d+\.\d+)(?P<suffix>\S+)?", re.VERBOSE | re.IGNORECASE
)


@Requirements("REQ_002")
@dataclass(kw_only=True)
class GitLocation(LocationInterface):
    url: str
    branch: str
    env_token: str
    path: str

    token: Optional[str] = field(init=False, default=None)

    def __post_init__(self) -> None:
        # Retrieve token from environment variable
        self.token = os.getenv(self.env_token) if self.env_token else None

        if self.token:
            logging.debug("Using token for authentication")

    def _make_available_on_localdisk(self, dst_path: str) -> str:
        if self.branch:
            repo = clone_repository(
                url=self.url, path=dst_path, checkout_branch=self.branch, callbacks=self.MyRemoteCallbacks(self.token)
            )
        else:
            repo = clone_repository(url=self.url, path=dst_path, callbacks=self.MyRemoteCallbacks(self.token))

        logging.debug(f"Cloned repo {self.url} (branch: {self.branch}) to {repo.workdir}\n")

        return repo.workdir

    @staticmethod
    def _get_all_versions(repo_path: str, token: Optional[str] = None) -> List[str]:
        """
        Returns all versions from tags from the repository located at `repo_path` that match the RE_GIT_TAG_VERSION pattern.
        """

        repo = pygit2.Repository(path=repo_path)

        # If the repository needs authentication for remote references:
        if repo.remotes:
            callbacks = self.MyRemoteCallbacks(token)
            remote = repo.remotes["origin"]

            # Ensure remote references are updated (no fetch, just accessing the tags)
            remote.fetch(callbacks=callbacks)

        all_versions: list[str] = list()

        for tag in repo.references:
            if tag.startswith("refs/tags/"):
                tag_name = tag.split("refs/tags/", 1)[1]
                if RE_GIT_TAG_VERSION.match(tag_name):
                    all_versions.append(tag_name)

        if not all_versions:
            raise Exception(f"No versions found for repo. {repo_path}")

        return all_versions

    def _resolve_version(self) -> str:
        """Resolve version based on version specifier."""

        if self.version not in ["latest", "latest-stable", "latest-unstable"]:
            return self.version

        all_versions: List[str] = self._get_all_versions()

        if self.version == "latest":
            return all_versions[-1]

        is_stable = self.version == "latest-stable"

        resolved_version: Optional[str] = None
        for v in reversed(all_versions):
            match: Optional[re.Match[str]] = RE_PEP440_VERSION.search(v)

            if not match:
                continue

            version: str = match.group("version")
            extra: str = match.group("extra")

            if is_stable and not extra:
                resolved_version = version
            elif not is_stable and extra:
                resolved_version = f"{version}{extra}"

            if resolved_version:
                break

    class MyRemoteCallbacks(RemoteCallbacks):
        def __init__(self, token):
            self.auth_method = ""  # x-oauth-basic, x-access-token
            self.token = token

        def credentials(self, url, username_from_url, allowed_types):
            return UserPass(username=self.auth_method, password=self.token)
