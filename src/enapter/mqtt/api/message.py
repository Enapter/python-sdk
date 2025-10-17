import abc
import json
from typing import Any, Dict, Union


class Message(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def from_dto(cls, dto: Dict[str, Any]):
        pass

    @abc.abstractmethod
    def to_dto(self) -> Dict[str, Any]:
        pass

    @classmethod
    def from_json(cls, data: Union[str, bytes]):
        dto = json.loads(data)
        return cls.from_dto(dto)

    def to_json(self) -> str:
        dto = self.to_dto()
        return json.dumps(dto)
