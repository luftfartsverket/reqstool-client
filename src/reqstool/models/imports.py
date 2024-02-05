# Copyright © LFV

from dataclasses import dataclass

from reqstool.location_resolver.location_resolver import LocationResolver


@dataclass
class ImportDataInterface(LocationResolver):
    pass


@dataclass
class GitImportData(ImportDataInterface):
    pass


@dataclass
class LocalImportData(ImportDataInterface):
    pass


@dataclass
class MavenImportData(ImportDataInterface):
    pass
