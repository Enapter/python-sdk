import dataclasses
from typing import Any


@dataclasses.dataclass
class Location:

    name: str
    latitude: float
    longitude: float

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> "Location":
        return cls(
            name=dto["name"], latitude=dto["latitude"], longitude=dto["longitude"]
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
