from enum import Enum


class Grouping(Enum):
    DEFAULT = "initial/imports"
    CATEGORY = "category"


class Sorting(Enum):
    DEFAULT = "id-alphanumerical"
    SIGNIFICANCE = "significance"
