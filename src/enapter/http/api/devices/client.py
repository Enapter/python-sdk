import httpx

from .communication_config import CommunicationConfig
from .device import Device
from .mqtt_protocol import MQTTProtocol


class Client:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get(self, device_id: str) -> Device:
        url = f"v3/devices/{device_id}"
        response = await self._client.get(url)
        response.raise_for_status()
        return Device.from_dto(response.json()["device"])

    async def generate_communication_config(
        self, device_id: str, mqtt_protocol: MQTTProtocol
    ) -> CommunicationConfig:
        url = f"v3/devices/{device_id}/generate_config"
        response = await self._client.post(url, json={"protocol": mqtt_protocol.value})
        response.raise_for_status()
        return CommunicationConfig.from_dto(response.json()["config"])
