import abc
import json
from typing import Any, Self


class Message(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        pass

    @abc.abstractmethod
    def to_dto(self) -> dict[str, Any]:
        pass

    @classmethod
    def from_json(cls, data: str | bytes) -> Self:
        dto = json.loads(data)
        return cls.from_dto(dto)

    def to_json(self) -> str:
        dto = self.to_dto()
        return json.dumps(dto)
