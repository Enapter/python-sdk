import dataclasses
import datetime
import enum
from typing import Any, Self


class BlueprintView(enum.Enum):

    ORIGINAL = "ORIGINAL"
    COMPILED = "COMPILED"


@dataclasses.dataclass
class Blueprint:

    id: str
    created_at: datetime.datetime

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            id=dto["id"],
            created_at=datetime.datetime.fromisoformat(dto["created_at"]),
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
        }
