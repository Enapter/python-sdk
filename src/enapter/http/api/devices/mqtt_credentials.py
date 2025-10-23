import dataclasses
from typing import Any, Dict


@dataclasses.dataclass
class MQTTCredentials:

    username: str
    password: str

    @classmethod
    def from_dto(cls, dto: Dict[str, Any]) -> "MQTTCredentials":
        return cls(username=dto["username"], password=dto["password"])
