import dataclasses
from typing import Any


@dataclasses.dataclass
class Location:

    name: str
    latitude: float | None
    longitude: float | None

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> "Location":
        return cls(
            name=dto["name"],
            latitude=dto.get("latitude"),
            longitude=dto.get("longitude"),
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
