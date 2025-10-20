import dataclasses
import enum
from typing import Any, Dict

from .message import Message


class CommandState(enum.Enum):

    COMPLETED = "completed"
    ERROR = "error"
    LOG = "log"


@dataclasses.dataclass
class CommandRequest(Message):

    id: str
    name: str
    arguments: Dict[str, Any]

    @classmethod
    def from_dto(cls, dto: Dict[str, Any]) -> "CommandRequest":
        return cls(
            id=dto["id"],
            name=dto["name"],
            arguments=dto.get("arguments", {}),
        )

    def to_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "arguments": self.arguments,
        }

    def new_response(
        self, state: CommandState, payload: Dict[str, Any]
    ) -> "CommandResponse":
        return CommandResponse(
            id=self.id,
            state=state,
            payload=payload,
        )


@dataclasses.dataclass
class CommandResponse(Message):

    id: str
    state: CommandState
    payload: Dict[str, Any]

    @classmethod
    def from_dto(cls, dto: Dict[str, Any]) -> "CommandResponse":
        return cls(
            id=dto["id"],
            state=CommandState(dto["state"]),
            payload=dto.get("payload", {}),
        )

    def to_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "state": self.state.value,
            "payload": self.payload,
        }
