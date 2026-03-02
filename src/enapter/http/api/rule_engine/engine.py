import dataclasses
from typing import Any, Self


@dataclasses.dataclass
class Engine:

    id: str
    state: str
    timezone: str

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            id=dto["id"],
            state=dto["state"],
            timezone=dto["timezone"],
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "state": self.state,
            "timezone": self.timezone,
        }
