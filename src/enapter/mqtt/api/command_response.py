import dataclasses
from typing import Any, Self

from .command_state import CommandState
from .message import Message


@dataclasses.dataclass
class CommandResponse(Message):

    id: str
    state: CommandState
    payload: dict[str, Any]

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            id=dto["id"],
            state=CommandState(dto["state"]),
            payload=dto.get("payload", {}),
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "state": self.state.value,
            "payload": self.payload,
        }
