import dataclasses
from typing import Any, Literal, Self

from .location import Location


@dataclasses.dataclass
class Site:

    id: str
    name: str
    timezone: str
    version: Literal["V3"]
    location: Location | None = None

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            id=dto["id"],
            name=dto["name"],
            timezone=dto["timezone"],
            version=dto["version"],
            location=(
                Location.from_dto(dto["location"])
                if dto.get("location") is not None
                else None
            ),
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "timezone": self.timezone,
            "version": self.version,
            "location": self.location.to_dto() if self.location is not None else None,
        }
