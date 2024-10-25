# Copyright © LFV

import os
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field, fields
from typing import List, Union

from reqstool_python_decorators.decorators.decorators import Requirements
from ruamel.yaml import YAML

from reqstool.commands.exit_codes import EXIT_CODE_SYNTAX_VALIDATION_ERROR
from reqstool.common.utils import open_file_https_file
from reqstool.common.validators.syntax_validator import JsonSchemaTypes, SyntaxValidator
from reqstool.locations.git_location import GitLocation
from reqstool.locations.local_location import LocalLocation
from reqstool.locations.location import LocationInterface
from reqstool.locations.maven_location import MavenLocation
from reqstool.reqstool_config.reqstool_config import ReqstoolConfig
from reqstool.requirements_indata.requirements_indata_paths import RequirementsIndataPathItem, RequirementsIndataPaths


@dataclass(kw_only=True)
class RequirementsIndata:
    dst_path: str  # tmp path
    location: LocationInterface  # current location
    reqstool_config: ReqstoolConfig = field(init=False, default=None)
    requirements_indata_paths: RequirementsIndataPaths = field(default_factory=RequirementsIndataPaths)

    def __post_init__(self):
        self._handle_requirements_config()
        self._ensure_absolute_paths_and_check_existance()

    @Requirements("REQ_011")
    def _handle_requirements_config(self):

        if os.path.exists(os.path.join(self.dst_path, "reqstool_config.yml")):
            response = open_file_https_file(os.path.join(self.dst_path, "reqstool_config.yml"))

            yaml = YAML(typ="safe")

            data: dict = yaml.load(response.text)

            if not SyntaxValidator.is_valid_data(
                json_schema_type=JsonSchemaTypes.REQSTOOL_CONFIG, data=data, urn="unknown"
            ):
                sys.exit(EXIT_CODE_SYNTAX_VALIDATION_ERROR)

            self.reqstool_config = ReqstoolConfig._parse(yaml_data=data)

    def _ensure_absolute_paths_and_check_existance(self):
        # iterate over all fields and ensure absolute paths

        for f in fields(self.requirements_indata_paths):
            field_name = f.name
            original: Union[RequirementsIndataPathItem, List[RequirementsIndataPathItem]] = getattr(
                self.requirements_indata_paths, field_name
            )

            if isinstance(self.location, GitLocation):
                # Include self.location.path when resolving a git repository
                RequirementsIndata._ensure_absolute_path_and_check_existance(
                    paths=[self.dst_path, self.location.path], original=original
                )
            elif isinstance(self.location, MavenLocation):
                # Include self.location.path when resolving a git repository
                RequirementsIndata._ensure_absolute_path_and_check_existance(paths=[self.dst_path], original=original)
            elif isinstance(self.location, LocalLocation):
                # resolve soft link
                abs_dst_path = os.readlink(self.dst_path)
                RequirementsIndata._ensure_absolute_path_and_check_existance(paths=[abs_dst_path], original=original)
            else:
                raise TypeError

    def _ensure_absolute_path_and_check_existance(
        paths: List[str], original: Union[RequirementsIndataPathItem, List[RequirementsIndataPathItem]]
    ):

        if isinstance(original, RequirementsIndataPathItem):
            new_abs_path = os.path.abspath(os.path.join(*paths, original.path))
            original.path = new_abs_path
            original.exists = os.path.exists(original.path)

        elif isinstance(original, Sequence):
            for item in original:
                new_abs_path = os.path.abspath(os.path.join(*paths, item.path))
                item.path = new_abs_path
                item.exists = os.path.exists(item.path)
        else:
            raise TypeError(type(original))
