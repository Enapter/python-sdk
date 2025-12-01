from typing import Any, AsyncGenerator

import httpx

from enapter import async_
from enapter.http import api

from .communication_config import CommunicationConfig
from .device import Device
from .mqtt_protocol import MQTTProtocol


class Client:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create_standalone(self, name: str, site_id: str | None = None) -> Device:
        url = "v3/provisioning/standalone"
        response = await self._client.post(url, json={"name": name, "site_id": site_id})
        api.check_error(response)
        return await self.get(device_id=response.json()["device_id"])

    async def get(
        self,
        device_id: str,
        expand_manifest: bool = False,
        expand_properties: bool = False,
        expand_connectivity: bool = False,
        expand_communication: bool = False,
    ) -> Device:
        url = f"v3/devices/{device_id}"
        expand = {
            "manifest": expand_manifest,
            "properties": expand_properties,
            "connectivity": expand_connectivity,
            "communication": expand_communication,
        }
        params = {"expand": ",".join(k for k, v in expand.items() if v)}
        response = await self._client.get(url, params=params)
        api.check_error(response)
        return Device.from_dto(response.json()["device"])

    @async_.generator
    async def list(self) -> AsyncGenerator[Device, None]:
        url = "v3/devices"
        limit = 50
        offset = 0
        while True:
            response = await self._client.get(
                url, params={"limit": limit, "offset": offset}
            )
            api.check_error(response)
            payload = response.json()
            if not payload["devices"]:
                return
            for dto in payload["devices"]:
                yield Device.from_dto(dto)
            offset += limit

    async def update(
        self, device_id: str, name: str | None = None, slug: str | None = None
    ) -> Device:
        if name is None and slug is None:
            return await self.get(device_id)
        url = f"v3/devices/{device_id}"
        response = await self._client.patch(url, json={"name": name, "slug": slug})
        api.check_error(response)
        return Device.from_dto(response.json()["device"])

    async def delete(self, device_id: str) -> None:
        url = f"v3/devices/{device_id}"
        response = await self._client.delete(url)
        api.check_error(response)

    async def assign_blueprint(self, device_id: str, blueprint_id: str) -> Device:
        url = f"v3/devices/{device_id}/assign_blueprint"
        response = await self._client.post(url, json={"blueprint_id": blueprint_id})
        api.check_error(response)
        return Device.from_dto(response.json()["device"])

    async def generate_communication_config(
        self, device_id: str, mqtt_protocol: MQTTProtocol
    ) -> CommunicationConfig:
        url = f"v3/devices/{device_id}/generate_config"
        response = await self._client.post(url, json={"protocol": mqtt_protocol.value})
        api.check_error(response)
        return CommunicationConfig.from_dto(response.json()["config"])
