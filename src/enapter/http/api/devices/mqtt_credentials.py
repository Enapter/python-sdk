import dataclasses
from typing import Any, Self


@dataclasses.dataclass
class MQTTCredentials:

    username: str
    password: str

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(username=dto["username"], password=dto["password"])
