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
                "device_id": "dev_123",
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
                "device_id": "dev_123",
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
async def test_get_execution(commands_client, mock_client):
    """Test getting a specific command execution."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "execution": {
            "id": "exec_1",
            "device_id": "dev_123",
            "state": "SUCCESS",
            "created_at": "2023-01-01T00:00:00Z",
            "request": {"name": "ping", "arguments": {}},
            "response": {
                "state": "SUCCEEDED",
                "payload": {"value": "pong"},
                "received_at": "2023-01-01T00:00:01Z",
            },
        }
    }
    mock_client.get = AsyncMock(return_value=mock_response)

    execution = await commands_client.get_execution(
        device_id="dev_123", execution_id="exec_1"
    )

    assert execution.id == "exec_1"
    assert execution.device_id == "dev_123"
    mock_client.get.assert_called_once_with(
        "v3/devices/dev_123/command_executions/exec_1", params={"expand": ""}
    )


@pytest.mark.asyncio
async def test_execute(commands_client, mock_client):
    """Test executing a command."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "execution": {
            "id": "exec_1",
            "device_id": "dev_123",
            "state": "SUCCESS",
            "created_at": "2023-01-01T00:00:00Z",
            "request": {"name": "ping", "arguments": {}},
            "response": {
                "state": "SUCCEEDED",
                "payload": {"value": "pong"},
                "received_at": "2023-01-01T00:00:01Z",
            },
        }
    }
    mock_client.post = AsyncMock(return_value=mock_response)

    execution = await commands_client.execute(device_id="dev_123", name="ping")

    assert execution.id == "exec_1"
    assert execution.device_id == "dev_123"
    mock_client.post.assert_called_once_with(
        "v3/devices/dev_123/execute_command",
        params={"expand": ""},
        json={"name": "ping", "arguments": {}},
    )


@pytest.mark.asyncio
async def test_create_execution(commands_client, mock_client):
    """Test creating a command execution."""
    mock_post_response = MagicMock(spec=httpx.Response)
    mock_post_response.status_code = 201
    mock_post_response.json.return_value = {"execution_id": "exec_1"}

    mock_get_response = MagicMock(spec=httpx.Response)
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {
        "execution": {
            "id": "exec_1",
            "device_id": "dev_123",
            "state": "SUCCESS",
            "created_at": "2023-01-01T00:00:00Z",
            "request": {"name": "ping", "arguments": {}},
            "response": {
                "state": "SUCCEEDED",
                "payload": {"value": "pong"},
                "received_at": "2023-01-01T00:00:01Z",
            },
        }
    }

    mock_client.post = AsyncMock(return_value=mock_post_response)
    mock_client.get = AsyncMock(return_value=mock_get_response)

    execution = await commands_client.create_execution(device_id="dev_123", name="ping")

    assert execution.id == "exec_1"
    assert execution.device_id == "dev_123"
    mock_client.post.assert_called_once_with(
        "v3/devices/dev_123/command_executions", json={"name": "ping", "arguments": {}}
    )
    mock_client.get.assert_called_once_with(
        "v3/devices/dev_123/command_executions/exec_1", params={"expand": ""}
    )


@pytest.mark.asyncio
async def test_list_executions_with_both_ids(commands_client, mock_client):
    """Test that list_executions passes device_id.in when both site_id and device_id are provided."""
    mock_response_1 = MagicMock(spec=httpx.Response)
    mock_response_1.status_code = 200
    mock_response_1.json.return_value = {
        "executions": [
            {
                "id": "exec_1",
                "device_id": "dev_123",
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
    async with commands_client.list_executions(
        site_id="site_123", device_id="dev_123"
    ) as stream:
        async for exec in stream:
            executions.append(exec)

    assert len(executions) == 1
    assert executions[0].id == "exec_1"
    mock_client.get.assert_any_call(
        "v3/sites/site_123/commands/executions",
        params={
            "order": "CREATED_AT_ASC",
            "limit": 50,
            "offset": 0,
            "device_id.in": "dev_123",
        },
    )


@pytest.mark.asyncio
async def test_list_executions_without_id_raises_error(commands_client):
    """Test that list_executions raises ValueError if neither device_id nor site_id is provided."""
    with pytest.raises(
        ValueError, match="either device_id or site_id must be provided"
    ):
        async with commands_client.list_executions() as stream:
            async for _ in stream:
                pass
