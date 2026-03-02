import dataclasses
from typing import Any, Self

from .engine_state import EngineState


@dataclasses.dataclass
class Engine:

    id: str
    state: EngineState
    timezone: str

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            id=dto["id"],
            state=EngineState(dto["state"]),
            timezone=dto["timezone"],
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "state": self.state.value,
            "timezone": self.timezone,
        }
