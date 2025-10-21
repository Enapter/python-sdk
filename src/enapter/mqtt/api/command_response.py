import dataclasses
from typing import Any, Dict

from .command_state import CommandState
from .message import Message


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
