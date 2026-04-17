"""Unit tests for the Devices HTTP API client."""

import datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

import enapter


@pytest.fixture
def mock_client():
    """Fixture to provide a mocked httpx.AsyncClient."""
    return MagicMock(spec=httpx.AsyncClient)


@pytest.fixture
def devices_client(mock_client):
    """Fixture to provide a Devices API client with a mocked internal client."""
    return enapter.http.api.devices.Client(client=mock_client)


def create_mock_device_dto(
    device_id: str, raised_alert_names: list[str] | None = None
) -> dict[str, Any]:
    dto: dict[str, Any] = {
        "id": device_id,
        "blueprint_id": "bp_123",
        "name": f"Device {device_id}",
        "site_id": "site_123",
        "updated_at": "2023-10-10T10:00:00Z",
        "slug": f"slug-{device_id}",
        "type": "STANDALONE",
        "authorized_role": "OWNER",
    }
    if raised_alert_names is not None:
        dto["raised_alert_names"] = raised_alert_names
    return dto


@pytest.mark.asyncio
async def test_get_device(devices_client, mock_client):
    """Test getting a specific device without expand."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"device": create_mock_device_dto("dev_1")}
    mock_client.get = AsyncMock(return_value=mock_response)

    device = await devices_client.get(device_id="dev_1")

    assert device.id == "dev_1"
    assert device.raised_alert_names is None
    mock_client.get.assert_called_once_with("v3/devices/dev_1", params={"expand": ""})


@pytest.mark.asyncio
async def test_get_device_expand_raised_alert_names(devices_client, mock_client):
    """Test getting a specific device with expand_raised_alert_names."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "device": create_mock_device_dto(
            "dev_2", raised_alert_names=["alert_1", "alert_2"]
        )
    }
    mock_client.get = AsyncMock(return_value=mock_response)

    device = await devices_client.get(device_id="dev_2", expand_raised_alert_names=True)

    assert device.id == "dev_2"
    assert device.raised_alert_names == ["alert_1", "alert_2"]
    mock_client.get.assert_called_once_with(
        "v3/devices/dev_2", params={"expand": "raised_alert_names"}
    )


@pytest.mark.asyncio
async def test_list_devices(devices_client, mock_client):
    """Test listing devices without expand."""
    mock_response_1 = MagicMock(spec=httpx.Response)
    mock_response_1.status_code = 200
    mock_response_1.json.return_value = {
        "devices": [create_mock_device_dto("dev_1"), create_mock_device_dto("dev_2")]
    }

    mock_response_2 = MagicMock(spec=httpx.Response)
    mock_response_2.status_code = 200
    mock_response_2.json.return_value = {"devices": []}

    mock_client.get = AsyncMock(side_effect=[mock_response_1, mock_response_2])

    devices = []
    async with devices_client.list() as d_gen:
        async for d in d_gen:
            devices.append(d)

    assert len(devices) == 2
    assert devices[0].id == "dev_1"
    assert devices[1].id == "dev_2"
    mock_client.get.assert_any_call(
        "v3/devices", params={"expand": "", "limit": 50, "offset": 0}
    )


@pytest.mark.asyncio
async def test_list_devices_expand_raised_alert_names(devices_client, mock_client):
    """Test listing devices with expand_raised_alert_names."""
    mock_response_1 = MagicMock(spec=httpx.Response)
    mock_response_1.status_code = 200
    mock_response_1.json.return_value = {
        "devices": [
            create_mock_device_dto("dev_1", raised_alert_names=["alert_1"]),
        ]
    }

    mock_response_2 = MagicMock(spec=httpx.Response)
    mock_response_2.status_code = 200
    mock_response_2.json.return_value = {"devices": []}

    mock_client.get = AsyncMock(side_effect=[mock_response_1, mock_response_2])

    devices = []
    async with devices_client.list(expand_raised_alert_names=True) as d_gen:
        async for d in d_gen:
            devices.append(d)

    assert len(devices) == 1
    assert devices[0].id == "dev_1"
    assert devices[0].raised_alert_names == ["alert_1"]
    mock_client.get.assert_any_call(
        "v3/devices", params={"expand": "raised_alert_names", "limit": 50, "offset": 0}
    )


def test_device_to_dto():
    device = enapter.http.api.devices.Device(
        id="dev_1",
        blueprint_id="bp_1",
        name="Device 1",
        site_id="site_1",
        updated_at=datetime.datetime.fromisoformat("2023-10-10T10:00:00+00:00"),
        slug="dev-1",
        type=enapter.http.api.devices.DeviceType.STANDALONE,
        authorized_role=enapter.http.api.devices.AuthorizedRole.OWNER,
        raised_alert_names=["alert_1"],
    )

    dto = device.to_dto()
    assert dto["id"] == "dev_1"
    assert dto["updated_at"] == "2023-10-10T10:00:00+00:00"
    assert dto["type"] == "STANDALONE"
    assert dto["authorized_role"] == "OWNER"
    assert dto["raised_alert_names"] == ["alert_1"]
