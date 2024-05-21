# Copyright © LFV

from dataclasses import dataclass, field
from pathlib import PurePath
from typing import List, Union

from reqstool_python_decorators.decorators.decorators import Requirements


@dataclass(kw_only=True)
class RequirementsIndataPathItem:
    path: str
    exists: bool = False


@Requirements("REQ_016")
@dataclass(kw_only=True)
class RequirementsIndataPaths:
    # static
    requirements_yml: RequirementsIndataPathItem = field(
        default_factory=lambda: RequirementsIndataPathItem(path="requirements.yml")
    )

    svcs_yml: RequirementsIndataPathItem = field(
        default_factory=lambda: RequirementsIndataPathItem(path="software_verification_cases.yml")
    )
    mvrs_yml: RequirementsIndataPathItem = field(
        default_factory=lambda: RequirementsIndataPathItem(path="manual_verification_results.yml")
    )

    # dynamic
    annotations_yml: RequirementsIndataPathItem = field(
        default_factory=lambda: RequirementsIndataPathItem(path="annotations.yml")
    )
    test_results_dirs: List[RequirementsIndataPathItem] = field(
        default_factory=lambda: [RequirementsIndataPathItem(path="test_results")]
    )

    def prepend_paths(self, prepend_dir):
        for prop in dir(self):
            if (
                not prop.startswith("__")
                and self.attribute_is_instance_or_list_of_class(prop_name=prop, the_class=RequirementsIndataPathItem)
                and prop not in ["requirements_yml", "svcs_yml", "mvrs_yml"]
            ):
                path_item = getattr(self, prop)
                self.check_type_and_prepend_path(path_item=path_item, prepend_dir=prepend_dir)

    def check_type_and_prepend_path(
        self, path_item: Union[RequirementsIndataPathItem, List[RequirementsIndataPathItem]], prepend_dir: str
    ):
        """Prepend path for each entry in a list of RequirementsIndataPathItem(s)
           or just on a single entity of the class

        Args:
            path_item (RequirementsIndataPathItem, [RequirementsIndataPathItem]): Either a RequirementsIndataPathItem
            or a list of RequirementsIndataPathItem
            prepend_dir (str): the root dir of the project specified in the reqstool_config.yml.

        Raises:
            TypeError: if there is a mismatch with path_item type or a path of a RequirementsIndataPathItem is missing.
        """
        if type(path_item) is list:
            for entry in path_item:
                if entry.path is not None:
                    entry.path = str(PurePath(prepend_dir, entry.path))
        else:
            if path_item.path is not None:
                path_item.path = str(PurePath(prepend_dir, path_item.path))

    def merge(self, other):
        merged_instance = self.__class__()
        for prop in dir(self):
            if not prop.startswith("__"):
                a_value = getattr(self, prop)
                b_value = getattr(other, prop)
                setattr(merged_instance, prop, b_value if b_value is not None else a_value)

        return merged_instance

    def attribute_is_instance_or_list_of_class(self, prop_name, the_class):
        prop = getattr(self, prop_name)
        if isinstance(prop, the_class):
            return True
        elif isinstance(prop, list):
            return all(isinstance(item, the_class) for item in prop)
        else:
            return False
