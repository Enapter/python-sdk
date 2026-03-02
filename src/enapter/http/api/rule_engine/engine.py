"""Rule Engine state representation."""

import dataclasses
from typing import Any, Self

from .engine_state import EngineState


@dataclasses.dataclass
class Engine:
    """Rule engine status information."""

    id: str
    state: EngineState
    timezone: str

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        """Create an Engine from a Data Transfer Object."""
        return cls(
            id=dto["id"],
            state=EngineState(dto["state"]),
            timezone=dto["timezone"],
        )

    def to_dto(self) -> dict[str, Any]:
        """Convert the Engine to a Data Transfer Object."""
        return {
            "id": self.id,
            "state": self.state.value,
            "timezone": self.timezone,
        }
