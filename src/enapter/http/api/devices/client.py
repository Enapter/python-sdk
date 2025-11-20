from typing import AsyncGenerator

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

    async def get(self, device_id: str) -> Device:
        url = f"v3/devices/{device_id}"
        response = await self._client.get(url)
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

    async def generate_communication_config(
        self, device_id: str, mqtt_protocol: MQTTProtocol
    ) -> CommunicationConfig:
        url = f"v3/devices/{device_id}/generate_config"
        response = await self._client.post(url, json={"protocol": mqtt_protocol.value})
        api.check_error(response)
        return CommunicationConfig.from_dto(response.json()["config"])
