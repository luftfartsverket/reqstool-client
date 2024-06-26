# Copyright © LFV

from dataclasses import dataclass

URN_ID_SEPARATOR: str = ":"


@dataclass(kw_only=True, frozen=True)
class UrnId:
    urn: str
    id: str

    @staticmethod
    def instance(urn_id_str: str) -> "UrnId":
        urn, id_ = urn_id_str.split(URN_ID_SEPARATOR, 1)

        return UrnId(urn=urn, id=id_)

    @staticmethod
    def assure_urn_id(urn: str, id: str) -> str:
        urn_id = None
        if URN_ID_SEPARATOR in id:
            urn_id = id
        else:
            urn_id = f"{urn}:{id}"

        return urn_id

    def __lt__(self, other: "UrnId"):
        if not isinstance(other, UrnId):
            return NotImplemented
        if self.urn != other.urn:
            return self.urn < other.urn
        return self.id < other.id

    def __str__(self) -> str:
        return f"{self.urn}:{self.id}"
