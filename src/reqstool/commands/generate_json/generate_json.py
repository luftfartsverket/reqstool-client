# Copyright © LFV


import re
from enum import Enum

import jsonpickle

from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.common.validator_error_holder import ValidationErrorHolder
from reqstool.common.validators.semantic_validator import SemanticValidator
from reqstool.locations.location import LOCATIONTYPES, LocationInterface
from reqstool.model_generators.combined_indexed_dataset_generator import CombinedIndexedDatasetGenerator
from reqstool.model_generators.combined_raw_datasets_generator import CombinedRawDatasetsGenerator
from reqstool.models.raw_datasets import CombinedRawDataset
from reqstool.models.requirements import SIGNIFANCETYPES, TYPES, VARIANTS
from reqstool.models.svcs import VERIFICATIONTYPES


class UrnIdHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj, data):
        return UrnId.assure_urn_id(obj.urn, obj.id)

    def restore(self, obj):
        urn_id_str = obj
        return UrnId.instance(urn_id_str)


class JsonEnumHandler(jsonpickle.handlers.BaseHandler):
    def restore(self, obj):
        pass

    def flatten(self, obj: Enum, data):
        return obj.value


class GenerateJsonCommand:
    def __init__(self, location: LocationInterface, filter_data: bool):
        self.__initial_location: LocationInterface = location
        self.__filter_data: bool = filter_data
        self.result = self.__run()

    def __run(self) -> str:
        """Generates The imported models as raw JSON

        Returns:
            str: The imported models as raw JSON.
        """
        holder = ValidationErrorHolder()
        semantic_validator = SemanticValidator(validation_error_holder=holder)
        combined_raw_datasets: CombinedRawDataset = CombinedRawDatasetsGenerator(
            initial_location=self.__initial_location, semantic_validator=semantic_validator
        ).combined_raw_datasets

        cids = CombinedIndexedDatasetGenerator(
            _crd=combined_raw_datasets, _filtered=self.__filter_data
        ).combined_indexed_dataset

        # Register the custom handler for enumerations

        jsonpickle.handlers.registry.register(UrnId, UrnIdHandler)
        jsonpickle.handlers.registry.register(SIGNIFANCETYPES, JsonEnumHandler)
        jsonpickle.handlers.registry.register(VERIFICATIONTYPES, JsonEnumHandler)
        jsonpickle.handlers.registry.register(VARIANTS, JsonEnumHandler)
        jsonpickle.handlers.registry.register(LOCATIONTYPES, JsonEnumHandler)
        jsonpickle.handlers.registry.register(TYPES, JsonEnumHandler)

        json_data = jsonpickle.encode(cids, make_refs=False, keys=True, unpicklable=False)

        # Regular expression pattern to match the given format
        pattern = r'json://\\"(.*?)\\"'

        # Replacement using regex
        json_data = re.sub(pattern, r"\1", json_data)

        return json_data
