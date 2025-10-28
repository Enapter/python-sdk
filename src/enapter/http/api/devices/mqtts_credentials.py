import dataclasses
from typing import Any, Self


@dataclasses.dataclass
class MQTTSCredentials:

    private_key: str
    certificate: str
    ca_chain: str

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            private_key=dto["private_key"],
            certificate=dto["certificate"],
            ca_chain=dto["ca_chain"],
        )
