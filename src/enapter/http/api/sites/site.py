import dataclasses
import datetime
from typing import Any, Self


@dataclasses.dataclass
class Site:

    id: str
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            id=dto["id"],
            name=dto["name"],
            created_at=datetime.datetime.fromisoformat(dto["created_at"]),
            updated_at=datetime.datetime.fromisoformat(dto["updated_at"]),
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
