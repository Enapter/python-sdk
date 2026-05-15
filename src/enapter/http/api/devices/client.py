import secrets
import time
from typing import AsyncContextManager, AsyncGenerator, List

import httpx

from enapter.http import api

from .communication_config import CommunicationConfig
from .device import Device
from .device_type import DeviceType
from .mqtt_protocol import MQTTProtocol


class Client:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create_standalone(
        self,
        name: str | None = None,
        site_id: str | None = None,
        slug: str | None = None,
    ) -> Device:
        if name is None:
            name = random_device_name(DeviceType.STANDALONE)
        url = "v3/provisioning/standalone"
        response = await self._client.post(
            url, json={"name": name, "site_id": site_id, "slug": slug}
        )
        await api.check_error(response)
        return await self.get(device_id=response.json()["device_id"])

    async def create_vucm(
        self,
        name: str | None = None,
        hardware_id: str | None = None,
        site_id: str | None = None,
    ) -> Device:
        if name is None:
            name = random_device_name(DeviceType.VIRTUAL_UCM)
        if hardware_id is None:
            hardware_id = random_hardware_id()
        url = "v3/provisioning/vucm"
        response = await self._client.post(
            url, json={"name": name, "hardware_id": hardware_id, "site_id": site_id}
        )
        await api.check_error(response)
        return await self.get(
            device_id=response.json()["device_id"], expand_communication=True
        )

    async def create_lua(
        self,
        runtime_id: str,
        blueprint_id: str,
        name: str | None = None,
        slug: str | None = None,
    ) -> Device:
        if name is None:
            name = random_device_name(DeviceType.LUA)
        url = "v3/provisioning/lua_device"
        response = await self._client.post(
            url,
            json={
                "name": name,
                "runtime_id": runtime_id,
                "blueprint_id": blueprint_id,
                "slug": slug,
            },
        )
        await api.check_error(response)
        return await self.get(device_id=response.json()["device_id"])

    async def get(
        self,
        device_id: str,
        expand_manifest: bool = False,
        expand_properties: bool = False,
        expand_connectivity: bool = False,
        expand_communication: bool = False,
        expand_raised_alert_names: bool = False,
    ) -> Device:
        url = f"v3/devices/{device_id}"
        expand = {
            "manifest": expand_manifest,
            "properties": expand_properties,
            "connectivity": expand_connectivity,
            "communication": expand_communication,
            "raised_alert_names": expand_raised_alert_names,
        }
        expand_string = ",".join(k for k, v in expand.items() if v)
        response = await self._client.get(url, params={"expand": expand_string})
        await api.check_error(response)
        return Device.from_dto(response.json()["device"])

    def list(
        self,
        expand_manifest: bool = False,
        expand_properties: bool = False,
        expand_connectivity: bool = False,
        expand_communication: bool = False,
        expand_raised_alert_names: bool = False,
        site_id: str | None = None,
        offset: int = 0,
        limit: int | None = None,
    ) -> AsyncContextManager[AsyncGenerator[Device, None]]:
        """List all devices."""

        async def fetch(current_offset: int) -> List[Device]:
            return await self._list(
                expand_manifest=expand_manifest,
                expand_properties=expand_properties,
                expand_connectivity=expand_connectivity,
                expand_communication=expand_communication,
                expand_raised_alert_names=expand_raised_alert_names,
                site_id=site_id,
                offset=current_offset,
            )

        return api.paginate(fetch, offset=offset, limit=limit)

    async def _list(
        self,
        expand_manifest: bool,
        expand_properties: bool,
        expand_connectivity: bool,
        expand_communication: bool,
        expand_raised_alert_names: bool,
        site_id: str | None,
        offset: int,
    ) -> List[Device]:
        url = "v3/devices" if site_id is None else f"v3/sites/{site_id}/devices"

        expand = {
            "manifest": expand_manifest,
            "properties": expand_properties,
            "connectivity": expand_connectivity,
            "communication": expand_communication,
            "raised_alert_names": expand_raised_alert_names,
        }
        expand_string = ",".join(k for k, v in expand.items() if v)

        response = await self._client.get(
            url, params={"expand": expand_string, "offset": offset}
        )
        await api.check_error(response)
        payload = response.json()
        return [Device.from_dto(dto) for dto in payload.get("devices", [])]

    async def update(
        self, device_id: str, name: str | None = None, slug: str | None = None
    ) -> Device:
        if name is None and slug is None:
            return await self.get(device_id)
        url = f"v3/devices/{device_id}"
        response = await self._client.patch(url, json={"name": name, "slug": slug})
        await api.check_error(response)
        return Device.from_dto(response.json()["device"])

    async def delete(self, device_id: str) -> None:
        url = f"v3/devices/{device_id}"
        response = await self._client.delete(url)
        await api.check_error(response)

    async def assign_blueprint(self, device_id: str, blueprint_id: str) -> Device:
        url = f"v3/devices/{device_id}/assign_blueprint"
        response = await self._client.post(url, json={"blueprint_id": blueprint_id})
        await api.check_error(response)
        return Device.from_dto(response.json()["device"])

    async def generate_communication_config(
        self, device_id: str, mqtt_protocol: MQTTProtocol
    ) -> CommunicationConfig:
        url = f"v3/devices/{device_id}/generate_config"
        response = await self._client.post(url, json={"protocol": mqtt_protocol.value})
        await api.check_error(response)
        return CommunicationConfig.from_dto(response.json()["config"])


def random_device_name(device_type: DeviceType) -> str:
    timestamp = int(time.time())
    return f"{device_type.value}_{timestamp}"


def random_hardware_id() -> str:
    return "V" + secrets.token_hex(16).upper()
