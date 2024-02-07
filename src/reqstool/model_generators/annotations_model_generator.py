# Copyright © LFV

import sys
from typing import Dict

from ruamel.yaml import YAML

from reqstool.commands.exit_codes import EXIT_CODE_SYNTAX_VALIDATION_ERROR
from reqstool.common import utils
from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.common.validators.syntax_validator import JsonSchemaTypes, SyntaxValidator
from reqstool.models.annotations import AnnotationData, AnnotationsData


class AnnotationsModelGenerator:
    def __init__(self, uri: str, urn: str):
        self.uri = uri
        self.urn = urn
        self.model = self.__generate(uri)

    def __generate(self, uri: str) -> AnnotationsData:
        response = utils.open_file_https_file(uri)

        yaml = YAML(typ="safe")

        data: dict = yaml.load(response.text)

        if not SyntaxValidator.is_valid_data(json_schema_type=JsonSchemaTypes.ANNOTATIONS, data=data, urn=self.urn):
            sys.exit(EXIT_CODE_SYNTAX_VALIDATION_ERROR)

        tests = self.__parse_annotations(data, "tests")
        implementations = self.__parse_annotations(data, "implementations")

        return AnnotationsData(tests=tests, implementations=implementations)

    def __parse_annotations(self, data, dictionary_key) -> Dict[UrnId, AnnotationData]:
        dictionary = {}

        if dictionary_key not in data["requirement_annotations"]:
            return dictionary

        for requirement_id in data["requirement_annotations"][dictionary_key].keys():
            urn_id = utils.convert_id_to_urn_id(self.urn, requirement_id)
            if requirement_id not in dictionary:
                dictionary[urn_id] = []

            for value in data["requirement_annotations"][dictionary_key][requirement_id]:
                ad = AnnotationData(element_kind=value["elementKind"], fully_qualified_name=value["fullyQualifiedName"])

                dictionary[urn_id].append(ad)

        return dictionary
