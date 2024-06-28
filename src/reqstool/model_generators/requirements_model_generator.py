# Copyright © LFV

import re
import sys
from typing import Dict, List, Set

from packaging.version import InvalidVersion, Version
from reqstool_python_decorators.decorators.decorators import Requirements
from ruamel.yaml import YAML

from reqstool.commands.exit_codes import EXIT_CODE_SYNTAX_VALIDATION_ERROR
from reqstool.common import utils
from reqstool.common.dataclasses.lifecycle import LIFECYCLESTATE, LifecycleData
from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.common.validators.semantic_validator import SemanticValidator
from reqstool.common.validators.syntax_validator import JsonSchemaTypes, SyntaxValidator
from reqstool.filters.requirements_filters import RequirementFilter
from reqstool.locations.git_location import GitLocation
from reqstool.locations.local_location import LocalLocation
from reqstool.locations.location import LOCATIONTYPES, LocationInterface
from reqstool.locations.maven_location import MavenLocation
from reqstool.models.implementations import GitImplData, ImplementationDataInterface, LocalImplData, MavenImplData
from reqstool.models.imports import GitImportData, ImportDataInterface, LocalImportData, MavenImportData
from reqstool.models.requirements import (
    CATEGORIES,
    IMPLEMENTATION,
    SIGNIFANCETYPES,
    VARIANTS,
    MetaData,
    ReferenceData,
    RequirementData,
    RequirementsData,
)


class RequirementsModelGenerator:
    def __init__(
        self,
        parent: LocationInterface,
        semantic_validator: SemanticValidator,
        filename: str,
        prefix_with_urn: bool = False,
    ):
        self.parent = parent
        self.filename = filename
        self.prefix_with_urn = prefix_with_urn
        self.semantic_validator = semantic_validator
        self.requirements_data = self.__generate(filename)

    @staticmethod
    def get_urn_if_available(data: str) -> str:
        # Regular expression pattern to match the URN value
        pattern = r"urn:\s*([^\n]+)"

        # Search for the pattern in the text
        match = re.search(pattern, data)

        # Extract URN value if found, otherwise set to "unknown"
        urn = match.group(1) if match else "unknown"

        return urn

    def __generate(
        self,
        uri: str,
    ) -> RequirementsData:
        response = utils.open_file_https_file(uri)

        yaml = YAML(typ="safe")

        data = yaml.load(response.text)

        urn = self.get_urn_if_available(response.text)

        if not SyntaxValidator.is_valid_data(json_schema_type=JsonSchemaTypes.REQUIREMENTS, data=data, urn=urn):
            sys.exit(EXIT_CODE_SYNTAX_VALIDATION_ERROR)

        r_metadata: MetaData = self.__parse_metadata(data["metadata"])

        r_implementations: List[ImplementationDataInterface] = []
        r_systems: List[ImportDataInterface] = []
        r_requirements: Dict[str, RequirementData] = {}
        r_filters: Dict[str, RequirementFilter] = {}

        match r_metadata.variant:
            case VARIANTS.SYSTEM:
                self.prefix_with_urn = False
                r_systems = self.__parse_systems(data=data)
                r_filters = self.__parse_requirement_filters(data=data)
                r_implementations = self.__parse_implementations(data=data)
                r_requirements = self.__parse_requirements(data=data)
            case VARIANTS.MICROSERVICE:
                self.prefix_with_urn = False
                r_systems = self.__parse_systems(data=data)
                r_filters = self.__parse_requirement_filters(data=data)
                r_requirements = self.__parse_requirements(data=data)
            case VARIANTS.EXTERNAL:
                self.prefix_with_urn = False
                r_requirements = self.__parse_requirements(data=data)
            case _:
                raise RuntimeError("Unsupported system type")

        return RequirementsData(
            metadata=r_metadata,
            implementations=r_implementations,
            imports=r_systems,
            requirements=r_requirements,
            filters=r_filters,
        )

    def __parse_metadata(self, data):
        r_urn: str = data["urn"]
        r_variant: VARIANTS = VARIANTS(data["variant"])
        r_title: str = data["title"]
        r_url: str = None if "url" not in data else data["url"]

        return MetaData(urn=r_urn, variant=r_variant, title=r_title, url=r_url)

    def __parse_implementations(self, data):
        r_implementations = []

        if "implementations" in data:
            # git
            self.__parse_implementations_git(data=data, r_implementations=r_implementations)

            # local
            self.__parse_implementations__local(data=data, r_implementations=r_implementations)

            # maven
            self.__parse_implementations__maven(data=data, r_implementations=r_implementations)

        return r_implementations

    def __parse_implementations__maven(self, data, r_implementations):
        if "maven" in data["implementations"]:
            for maven in data["implementations"]["maven"]:
                maven_impl = MavenImplData(
                    parent=self.parent,
                    _current_unresolved=MavenLocation(
                        env_token=maven["env_token"],
                        url=maven["url"],
                        group_id=maven["group_id"],
                        artifact_id=maven["artifact_id"],
                        version=maven["version"],
                        classifier=maven["classifier"],
                        path=maven["path"],
                    ),
                )

                r_implementations.append(maven_impl)

    def __parse_implementations__local(self, data, r_implementations):
        if "local" in data["implementations"]:
            for local in data["implementations"]["local"]:
                local_impl = LocalImplData(parent=self.parent, _current_unresolved=LocalLocation(path=local["path"]))

                r_implementations.append(local_impl)

    def __parse_implementations_git(self, data, r_implementations):
        if "git" in data["implementations"]:
            for git in data["implementations"]["git"]:
                git_impl = GitImplData(
                    parent=self.parent,
                    _current_unresolved=GitLocation(
                        env_token=git["env_token"],
                        url=git["url"],
                        branch=git["branch"],
                        path=git["path"],
                    ),
                )

                r_implementations.append(git_impl)

    def __parse_systems(self, data):
        r_systems = []

        if "imports" in data:
            # git
            self.__parse_systems_git(data=data, r_systems=r_systems)

            # local
            self.__parse_systems_local(data=data, r_systems=r_systems)

            # maven
            self.__parse_systems_maven(data=data, r_systems=r_systems)

        return r_systems

    def __parse_systems_maven(self, data, r_systems):
        if LOCATIONTYPES.MAVEN.value in data["imports"]:
            for maven in data["imports"][LOCATIONTYPES.MAVEN.value]:
                maven_system = MavenImportData(
                    parent=self.parent,
                    _current_unresolved=MavenLocation(
                        env_token=maven["env_token"],
                        url=maven["url"],
                        group_id=maven["group_id"],
                        artifact_id=maven["artifact_id"],
                        version=maven["version"],
                        classifier=maven["classifier"],
                        path=maven["path"],
                    ),
                )

                r_systems.append(maven_system)

    def __parse_systems_local(self, data, r_systems):
        if LOCATIONTYPES.LOCAL.value in data["imports"]:
            for local in data["imports"][LOCATIONTYPES.LOCAL.value]:
                local_impl = LocalImportData(parent=self.parent, _current_unresolved=LocalLocation(path=local["path"]))

                r_systems.append(local_impl)

    def __parse_systems_git(self, data, r_systems):
        if LOCATIONTYPES.GIT.value in data["imports"]:
            for git in data["imports"][LOCATIONTYPES.GIT.value]:
                git_system = GitImportData(
                    parent=self.parent,
                    _current_unresolved=GitLocation(
                        env_token=git["env_token"],
                        url=git["url"],
                        branch=git["branch"],
                        path=git["path"],
                    ),
                )

                r_systems.append(git_system)

    def __parse_requirement_filters(self, data) -> Dict[str, RequirementFilter]:  # NOSONAR
        r_filters = {}

        self.semantic_validator._validate_req_imports_filter_has_excludes_xor_includes(data)

        if "filters" in data:
            for urn in data["filters"].keys():
                urn_filter = data["filters"][urn]

                req_urn_ids_imports: Set[str] = None  # NOSONAR
                req_urn_ids_excludes: Set[str] = None  # NOSONAR
                custom_includes = None
                custom_exclude = None

                if "requirement_ids" in urn_filter:
                    if "includes" in urn_filter["requirement_ids"]:
                        filtered_ids = utils.check_ids_to_filter(
                            current_urn=urn, ids=urn_filter["requirement_ids"]["includes"]
                        )
                        req_ids_includes = set(filtered_ids)
                        req_urn_ids_imports: Set[UrnId] = set(
                            utils.convert_ids_to_urn_id(urn=urn, ids=req_ids_includes)
                        )

                    if "excludes" in urn_filter["requirement_ids"]:
                        filtered_ids = utils.check_ids_to_filter(
                            current_urn=urn, ids=urn_filter["requirement_ids"]["excludes"]
                        )
                        req_ids_excludes = set(filtered_ids)
                        req_urn_ids_excludes: Set[UrnId] = set(
                            utils.convert_ids_to_urn_id(urn=urn, ids=req_ids_excludes)
                        )

                if "custom" in urn_filter:
                    if "includes" in urn_filter["custom"]:
                        custom_includes = urn_filter["custom"]["includes"]

                    if "excludes" in urn_filter["custom"]:
                        custom_exclude = urn_filter["custom"]["excludes"]

                req_filter = RequirementFilter(
                    urn_ids_imports=req_urn_ids_imports,
                    urn_ids_excludes=req_urn_ids_excludes,
                    custom_imports=custom_includes,
                    custom_exclude=custom_exclude,
                )

                r_filters[urn] = req_filter

        return r_filters

    @Requirements("REQ_004", "REQ_036")
    def __parse_requirements(self, data):  # NOSONAR
        r_reqs = {}

        self.semantic_validator._validate_no_duplicate_requirement_ids(data=data)

        if "requirements" in data:
            for req in data["requirements"]:
                refs_data = []
                urn = data["metadata"]["urn"]

                if "references" in req:
                    refs_data.extend(
                        [
                            ReferenceData(
                                requirement_ids=utils.convert_ids_to_urn_id(
                                    ids=req["references"]["requirement_ids"], urn=urn
                                )
                            )
                        ]
                    )

                # Check if rationale is defined, or set it to None
                rationale = req["rationale"] if "rationale" in req else None
                # Check if implementation is defined, or set it to True
                implementation = req["implementation"] if "implementation" in req else IMPLEMENTATION.IN_CODE.value
                # Get lifecycle variables or use defaults
                if "lifecycle" in req:
                    lifecycle_state = LIFECYCLESTATE(req["lifecycle"]["state"])
                    lifecycle_reason = req["lifecycle"]["reason"] if "reason" in req["lifecycle"] else None
                else:
                    lifecycle_state = LIFECYCLESTATE.EFFECTIVE
                    lifecycle_reason = None

                urn_id = UrnId(urn=urn, id=req["id"])
                req_data = RequirementData(
                    id=urn_id,
                    title=req["title"],
                    significance=SIGNIFANCETYPES(req["significance"]),
                    description=req["description"],
                    rationale=rationale,
                    implementation=IMPLEMENTATION(implementation),
                    categories=[CATEGORIES(c) for c in req["categories"]],
                    references=refs_data,
                    revision=self.__parse_req_version(version=req["revision"], urn_id=urn_id),
                    lifecycle=LifecycleData(state=lifecycle_state, reason=lifecycle_reason),
                )

                if req_data.id not in r_reqs:
                    r_reqs[req_data.id] = req_data

        return r_reqs

    def __parse_req_version(self, version: str, urn_id: UrnId) -> Version:
        try:
            return Version(version)
        except InvalidVersion as e:
            raise TypeError(f"Invalid version: {e} for: {urn_id}")
