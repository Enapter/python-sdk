import dataclasses
import datetime
from typing import Any, Dict

from .authorized_role import AuthorizedRole
from .device_type import DeviceType


@dataclasses.dataclass
class Device:

    id: str
    blueprint_id: str
    name: str
    site_id: str
    updated_at: datetime.datetime
    slug: str
    type: DeviceType
    authorized_role: AuthorizedRole

    @classmethod
    def from_dto(cls, dto: Dict[str, Any]) -> "Device":
        return cls(
            id=dto["id"],
            blueprint_id=dto["blueprint_id"],
            name=dto["name"],
            site_id=dto["site_id"],
            updated_at=datetime.datetime.fromisoformat(dto["updated_at"]),
            slug=dto["slug"],
            type=DeviceType(dto["type"]),
            authorized_role=AuthorizedRole(dto["authorized_role"]),
        )
