"""Unit tests for the Commands HTTP API client."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

import enapter


@pytest.fixture
def mock_client():
    """Fixture to provide a mocked httpx.AsyncClient."""
    return MagicMock(spec=httpx.AsyncClient)


@pytest.fixture
def commands_client(mock_client):
    """Fixture to provide a Commands API client with a mocked internal client."""
    return enapter.http.api.commands.Client(client=mock_client)


@pytest.mark.asyncio
async def test_list_executions_with_device_id(commands_client, mock_client):
    """Test listing command executions for a specific device."""
    mock_response_1 = MagicMock(spec=httpx.Response)
    mock_response_1.status_code = 200
    mock_response_1.json.return_value = {
        "executions": [
            {
                "id": "exec_1",
                "state": "SUCCESS",
                "created_at": "2023-01-01T00:00:00Z",
                "request": {"name": "ping", "arguments": {}},
                "response": {
                    "state": "SUCCEEDED",
                    "payload": {"value": "pong"},
                    "received_at": "2023-01-01T00:00:01Z",
                },
            }
        ]
    }
    mock_response_2 = MagicMock(spec=httpx.Response)
    mock_response_2.status_code = 200
    mock_response_2.json.return_value = {"executions": []}

    mock_client.get = AsyncMock(side_effect=[mock_response_1, mock_response_2])

    executions = []
    async with commands_client.list_executions(device_id="dev_123") as stream:
        async for exec in stream:
            executions.append(exec)

    assert len(executions) == 1
    assert executions[0].id == "exec_1"
    assert mock_client.get.call_count == 2
    mock_client.get.assert_any_call(
        "v3/devices/dev_123/command_executions",
        params={"order": "CREATED_AT_ASC", "limit": 50, "offset": 0},
    )
    mock_client.get.assert_any_call(
        "v3/devices/dev_123/command_executions",
        params={"order": "CREATED_AT_ASC", "limit": 50, "offset": 50},
    )


@pytest.mark.asyncio
async def test_list_executions_with_site_id(commands_client, mock_client):
    """Test listing command executions for all devices in a site."""
    mock_response_1 = MagicMock(spec=httpx.Response)
    mock_response_1.status_code = 200
    mock_response_1.json.return_value = {
        "executions": [
            {
                "id": "exec_1",
                "state": "SUCCESS",
                "created_at": "2023-01-01T00:00:00Z",
                "request": {"name": "ping", "arguments": {}},
                "response": {
                    "state": "SUCCEEDED",
                    "payload": {"value": "pong"},
                    "received_at": "2023-01-01T00:00:01Z",
                },
            }
        ]
    }
    mock_response_2 = MagicMock(spec=httpx.Response)
    mock_response_2.status_code = 200
    mock_response_2.json.return_value = {"executions": []}

    mock_client.get = AsyncMock(side_effect=[mock_response_1, mock_response_2])

    executions = []
    async with commands_client.list_executions(site_id="site_123") as stream:
        async for exec in stream:
            executions.append(exec)

    assert len(executions) == 1
    assert executions[0].id == "exec_1"
    assert mock_client.get.call_count == 2
    mock_client.get.assert_any_call(
        "v3/sites/site_123/commands/executions",
        params={"order": "CREATED_AT_ASC", "limit": 50, "offset": 0},
    )
    mock_client.get.assert_any_call(
        "v3/sites/site_123/commands/executions",
        params={"order": "CREATED_AT_ASC", "limit": 50, "offset": 50},
    )


@pytest.mark.asyncio
async def test_list_executions_with_both_ids_raises_error(commands_client):
    """Test that list_executions raises ValueError if both device_id and site_id are provided."""
    with pytest.raises(
        ValueError, match="device_id and site_id are mutually exclusive"
    ):
        async with commands_client.list_executions(
            device_id="dev_123", site_id="site_123"
        ) as stream:
            async for _ in stream:
                pass


@pytest.mark.asyncio
async def test_list_executions_without_id_raises_error(commands_client):
    """Test that list_executions raises ValueError if neither device_id nor site_id is provided."""
    with pytest.raises(
        ValueError, match="either device_id or site_id must be provided"
    ):
        async with commands_client.list_executions() as stream:
            async for _ in stream:
                pass
