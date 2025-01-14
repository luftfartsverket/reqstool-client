# Copyright © LFV

# type: ignore[no-untyped-call]

import logging
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Union

import pygit2
from attrs import field
from pygit2 import CredentialType, RemoteCallbacks, UserPass, clone_repository
from reqstool_python_decorators.decorators.decorators import Requirements

from reqstool.locations.location import LocationInterface

RE_GIT_TAG_VERSION: re.Pattern[str] = re.compile(
    r"^refs\/tags\/(?P<version>(?:v)?\d+\.\d+\.\d+\S*)$", re.VERBOSE | re.IGNORECASE
)

RE_SEMANTIC_VERSION_PLUS_EXTRA: re.Pattern[str] = re.compile(
    r"^(?P<version>(?P<semantic>(?:v)?\d+\.\d+\.\d+)(?P<rest>\S+)?)$", re.VERBOSE | re.IGNORECASE
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
                url=self.url, path=dst_path, checkout_branch=self.branch, callbacks=MyRemoteCallbacks(self.token)
            )
        else:
            repo = clone_repository(url=self.url, path=dst_path, callbacks=MyRemoteCallbacks(self.token))

        logging.debug(f"Cloned repo {self.url} (branch: {self.branch}) to {repo.workdir}\n")

        return str(repo.workdir)

    @staticmethod
    def _get_all_versions(repo_path: str, token: Optional[str] = None) -> List[str]:
        """
        Returns all versions from tags from the repository located at `repo_path` that match the RE_GIT_TAG_VERSION pattern.
        """

        repo = pygit2.Repository(path=repo_path)

        # If the repository needs authentication for remote references:
        # if repo.remotes:
        #     callbacks = MyRemoteCallbacks(token)
        #     remote = repo.remotes["origin"]

        #     # Ensure remote references are updated (no fetch, just accessing the tags)
        #     remote.fetch(callbacks=callbacks)

        all_versions: list[str] = list()

        for ref in repo.references:
            if match := RE_GIT_TAG_VERSION.match(ref):
                all_versions.append(match.group("version"))

        if not all_versions:
            raise ValueError(f"No versions found for repo. {repo_path}")

        return all_versions

    def _resolve_version(self) -> str:
        """Resolve version based on version specifier."""

        if self.version not in ["latest", "latest-stable", "latest-unstable"]:
            return self.version

        all_versions: List[str] = self._get_all_versions(package=self.package, base_url=self.url, token=self.token)

        if self.version == "latest":
            return all_versions[-1]

        is_stable = self.version == "latest-stable"

        filtered_versions: List[str] = self._filter_versions(all_versions=all_versions, stable_versions=is_stable)

        # no matching version found
        if not filtered_versions:
            version_type = "stable" if is_stable else "unstable"
            raise ValueError(f"No {version_type} versions found for {self.package}")

        return filtered_versions[-1]

    @staticmethod
    def _filter_versions(all_versions: List[str], stable_versions: bool) -> List[str]:
        return [
            v
            for v in all_versions
            if (match := RE_SEMANTIC_VERSION_PLUS_EXTRA.search(v)) and (bool(match.group("rest")) != stable_versions)
        ]


class MyRemoteCallbacks(RemoteCallbacks):
    def __init__(self, token: str):
        self.auth_method = ""  # x-oauth-basic, x-access-token
        self.token = token

    def credentials(
        self,
        url: str,
        username_from_url: Union[str, None],
        allowed_types: CredentialType,
    ) -> UserPass:
        return UserPass(username=self.auth_method, password=self.token)
