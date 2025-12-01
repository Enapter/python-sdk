import dataclasses
import datetime
from typing import Any, Self

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
    manifest: dict[str, Any] | None = None

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            id=dto["id"],
            blueprint_id=dto["blueprint_id"],
            name=dto["name"],
            site_id=dto["site_id"],
            updated_at=datetime.datetime.fromisoformat(dto["updated_at"]),
            slug=dto["slug"],
            type=DeviceType(dto["type"]),
            authorized_role=AuthorizedRole(dto["authorized_role"]),
            manifest=dto.get("manifest"),
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "blueprint_id": self.blueprint_id,
            "name": self.name,
            "site_id": self.site_id,
            "updated_at": self.updated_at.isoformat(),
            "slug": self.slug,
            "type": self.type.value,
            "authorized_role": self.authorized_role.value,
            "manifest": self.manifest,
        }
