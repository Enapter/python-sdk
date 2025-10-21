import dataclasses
from typing import Any, Dict

from .command_response import CommandResponse
from .command_state import CommandState
from .message import Message


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
    ) -> CommandResponse:
        return CommandResponse(
            id=self.id,
            state=state,
            payload=payload,
        )
