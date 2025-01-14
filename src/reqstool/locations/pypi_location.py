import logging
import os
import re
import sys
import tarfile
from dataclasses import dataclass, field
from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from reqstool.common.utils import Utils
from reqstool.locations.location import LocationInterface

# https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers-regex
VERSION_PATTERN = r"""
    v?
    (?P<version>                                          # Combined version (epoch + release)
        (?:(?P<epoch>[0-9]+)!)?                           # epoch
        (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
    )
    (?P<rest>                                            # rest: everything after version
        (?P<pre>                                          # pre-release
            [-_\.]?
            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
            [-_\.]?
            (?P<pre_n>[0-9]+)?
        )?
        (?P<post>                                         # post release
            (?:-(?P<post_n1>[0-9]+))
            |
            (?:
                [-_\.]?
                (?P<post_l>post|rev|r)
                [-_\.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            [-_\.]?
            (?P<dev_l>dev)
            [-_\.]?
            (?P<dev_n>[0-9]+)?
        )?
        (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?   # local version
    )?
"""
RE_PEP440_VERSION: re.Pattern[str] = re.compile(VERSION_PATTERN, re.VERBOSE | re.IGNORECASE)
RE_PYPI_SIMPLE_API_HREF_VERSION = re.compile(VERSION_PATTERN + r"\.tar\.gz", re.VERBOSE | re.IGNORECASE)


@dataclass(kw_only=True)
class PypiLocation(LocationInterface):
    url: str = field(default="https://pypi.org/simple")
    package: str
    version: str
    env_token: Optional[str] = field(default=None)
    token: Optional[str] = field(init=False, default=None)

    def __post_init__(self) -> None:
        # Retrieve token from environment variable
        self.token = os.getenv(self.env_token) if self.env_token else None

        if self.token:
            logging.debug("Using OAuth Bearer token for authentication")

    @staticmethod
    def normalize_pypi_package_name(package_name: str) -> str:
        return re.sub(r"[-_.]+", "-", package_name).lower()

    def _make_available_on_localdisk(self, dst_path: str) -> str:
        """
        Download the PyPI package and extract it to the local disk.
        """
        resolved_version: str = self._resolve_version()

        package_url = PypiLocation.get_package_url(self.package, resolved_version, self.url, self.token)

        if not package_url:
            token_info = f"(with token in environment variable '{self.env_token}')" if self.env_token else ""
            raise RuntimeError(
                f"Unable to find a sdist pypi package for {self.package} == {self.version} in repo {self.url}{token_info}"
            )

        logging.debug(f"Downloading {self.package} from {self.url} to {dst_path}\n")

        try:
            downloaded_file = Utils.download_file(url=package_url, dst_path=dst_path, token=self.token)

            logging.debug(f"Extracting {downloaded_file} to {dst_path}\n")

            with tarfile.open(downloaded_file, "r:gz") as tar_ref:
                top_level_dirs = {
                    member.name.split("/")[0] for member in tar_ref.getmembers() if member.name.count("/") > 0
                }
                tar_ref.extractall(path=dst_path, filter="data")
        except tarfile.TarError as e:
            logging.fatal(f"Error extracting {downloaded_file}: {e}")
            sys.exit(1)
        except Exception as e:
            logging.fatal(
                f"Error when downloading etc sdist pypi package for {self.package}=={self.version}"
                f" in repo {self.url} {'with token' if self.token else ''}",
                e,
            )
            sys.exit(1)

        if len(top_level_dirs) != 1:
            logging.fatal(
                f"Tarball from {self.url} did not have one and only one" f" top level directory: {top_level_dirs}"
            )
            sys.exit(1)

        top_level_dir = os.path.join(dst_path, top_level_dirs.pop())

        logging.debug(f"Extracted {downloaded_file} to {top_level_dir}\n")

        return top_level_dir

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
            if (match := RE_PEP440_VERSION.search(v)) and (bool(match.group("rest")) != stable_versions)
        ]

    @staticmethod
    def _get_all_versions(package: str, base_url: str, token: Optional[str] = None) -> List[str]:
        """Get all available versions for the package."""
        package = PypiLocation.normalize_pypi_package_name(package_name=package)

        if not base_url.endswith("/"):
            base_url += "/"

        # Construct the request URL by appending the package_name to base_url_path
        url = urljoin(base_url, f"{package}/")

        # Prepare headers
        headers = {"Accept": "text/html"}

        if token:
            # If the token exists, add it as a Bearer token in the Authorization header
            headers["Authorization"] = f"Bearer {token}"

        # Make the request to the package's metadata endpoint
        response = requests.get(url, headers=headers)

        # Raise an error if the request was unsuccessful
        response.raise_for_status()

        # Parse the HTML response
        soup = BeautifulSoup(response.content, "html.parser")

        all_versions: list[str] = list()

        # Get all version with sdist file
        for link in soup.find_all("a"):
            href = link.get("href")

            # Search for the pattern in the text
            match: Optional[re.Match[str]] = RE_PYPI_SIMPLE_API_HREF_VERSION.search(href)

            if not match:
                # $$$ log here
                continue

            # Extract semantic version value if found, otherwise set to "unknown"
            version = match.group("version")

            all_versions.append(version)

        if not all_versions:
            raise Exception(f"No versions found for {package}")

        return all_versions

    @staticmethod
    def get_package_url(package: str, version: str, base_url: str, token: Optional[str]) -> Optional[str]:
        package = PypiLocation.normalize_pypi_package_name(package_name=package)

        if not base_url.endswith("/"):
            base_url += "/"

        # Construct the request URL by appending the package_name to base_url_path
        url = urljoin(base_url, f"{package}/")

        # Prepare headers
        headers = {"Accept": "text/html"}

        if token:
            # If the token exists, add it as a Bearer token in the Authorization header
            headers["Authorization"] = f"Bearer {token}"

        # Make the request to the package's metadata endpoint
        response = requests.get(url, headers=headers)

        # Raise an error if the request was unsuccessful
        response.raise_for_status()

        # Parse the HTML response
        soup = BeautifulSoup(response.content, "html.parser")

        # Search for the specific version's sdist file
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and f"{version}.tar.gz" in href:
                # Normalize the URL by removing the has suffix if present (e.g. md5, sha1, sha224, sha256, sha384, sha512)
                if "#" in href:
                    href = href.split("#")[0]  # Remove the hash suffix

                absolute_url = urljoin(url, href)
                return absolute_url  # Return the absolute URL of the matching file

        # Return None if no matching file is found
        return None
