# Copyright © LFV

from dataclasses import dataclass

from reqstool.location_resolver.location_resolver import LocationResolver


@dataclass
class ImplementationDataInterface(LocationResolver):
    pass


@dataclass
class GitImplData(ImplementationDataInterface):
    pass


@dataclass
class LocalImplData(ImplementationDataInterface):
    pass


@dataclass
class MavenImplData(ImplementationDataInterface):
    pass
