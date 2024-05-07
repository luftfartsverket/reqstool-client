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
from reqstool.reqstool_config.reqstool_config import TYPES, ReqstoolConfig
from reqstool.requirements_indata.java.java_maven_requirements_indata_paths import JavaMavenRequirementsIndataPaths
from reqstool.requirements_indata.python.python_requirements_indata_paths import PythonRequirementsIndataPaths
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

            match self.reqstool_config.type:
                case TYPES.JAVA_MAVEN:
                    self.requirements_indata_paths = JavaMavenRequirementsIndataPaths()
                case TYPES.PYTHON:
                    self.requirements_indata_paths = PythonRequirementsIndataPaths()

            self._handle_custom()

            if self.reqstool_config.project_root_dir is not None:
                self.requirements_indata_paths.prepend_paths(self.reqstool_config.project_root_dir)

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
                RequirementsIndata._ensure_absolute_path_and_check_existance(
                    paths=[self.dst_path, self.location.path], original=original
                )
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

    def _handle_custom(self):
        # replace default values with custom if specified

        if self.reqstool_config.locations.test_results:
            test_results = self.reqstool_config.locations.test_results

            if isinstance(test_results, Sequence):
                r_test_results = []

                for test_result_dir in test_results:
                    r_test_results.append(RequirementsIndataPathItem(path=test_result_dir))

                self.requirements_indata_paths.test_results_dirs = r_test_results

        if self.reqstool_config.locations.annotations:
            self.requirements_indata_paths.annotations_yml = RequirementsIndataPathItem(
                path=self.reqstool_config.locations.annotations
            )
