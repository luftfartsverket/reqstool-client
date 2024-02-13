# Copyright © LFV

import os
import sys
from dataclasses import dataclass, field, fields

from ruamel.yaml import YAML

from reqstool.commands.exit_codes import EXIT_CODE_SYNTAX_VALIDATION_ERROR
from reqstool.common.utils import open_file_https_file
from reqstool.common.validators.syntax_validator import JsonSchemaTypes, SyntaxValidator
from reqstool.locations.git_location import GitLocation
from reqstool.locations.local_location import LocalLocation
from reqstool.locations.location import LocationInterface
from reqstool.locations.maven_location import MavenLocation
from reqstool.reqstool_config.reqstool_config import TYPES, ReqstoolConfig
from reqstool.requirements_indata.java.java_maven_requirements_indata_paths import (
    JavaMavenRequirementsIndataPaths,
    RequirementsIndataPathItem,
)
from reqstool.requirements_indata.requirements_indata_paths import (
    RequirementsIndataPaths,
    RequirementsIndataStructureItem,
)


@dataclass(kw_only=True)
class RequirementsIndata:
    dst_path: str  # tmp path
    location: LocationInterface  # current location
    reqstool_config: ReqstoolConfig = field(default=None)
    requirements_indata_paths: RequirementsIndataPaths = field(default_factory=RequirementsIndataPaths)

    def __post_init__(self):
        self._handle_requirements_config()
        self._ensure_absolute_paths()
        self._check_what_indata_that_exists()

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

            self._handle_custom()

            if self.reqstool_config.project_root_dir is not None:
                self.requirements_indata_paths.prepend_paths(self.reqstool_config.project_root_dir)

    def _ensure_absolute_paths(self):
        # iterate over all fields and ensure absolute paths

        for f in fields(self.requirements_indata_paths):
            field_name = f.name
            original_item: RequirementsIndataPathItem = getattr(self.requirements_indata_paths, field_name)
            transformed_value = None

            if isinstance(self.location, GitLocation):
                # Include self.location.path when resolving a git repository
                transformed_value = os.path.abspath(os.path.join(self.dst_path, self.location.path, original_item.path))
            elif isinstance(self.location, MavenLocation):
                # Include self.location.path when resolving a git repository
                transformed_value = os.path.abspath(os.path.join(self.dst_path, self.location.path, original_item.path))
            elif isinstance(self.location, LocalLocation):
                # resolve soft link
                abs_dst_path = os.readlink(self.dst_path)
                transformed_value = os.path.abspath(os.path.join(abs_dst_path, original_item.path))
            else:
                raise TypeError

            original_item.path = transformed_value

    def _check_what_indata_that_exists(self):
        # iterate over all fields and check for existance

        for f in fields(self.requirements_indata_paths):
            field_name = f.name
            original_item: RequirementsIndataPathItem = getattr(self.requirements_indata_paths, field_name)
            original_item.exists = os.path.exists(original_item.path)

    def _handle_custom(self):
        # replace default values with custom if specified

        if self.reqstool_config.locations:
            test_results = self.reqstool_config.locations.test_results

            if test_results:
                if test_results.failsafe:
                    self.requirements_indata_paths.test_results_failsafe_dir = RequirementsIndataStructureItem(
                        path=test_results.failsafe
                    )

                if test_results.surefire:
                    self.requirements_indata_paths.test_results_surefire_dir = RequirementsIndataStructureItem(
                        path=test_results.surefire
                    )

            if self.reqstool_config.locations.annotations:
                self.requirements_indata_paths.annotations_yml = RequirementsIndataStructureItem(
                    path=self.reqstool_config.locations.annotations
                )
