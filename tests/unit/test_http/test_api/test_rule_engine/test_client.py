from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from enapter.http.api.rule_engine.client import Client


@pytest.fixture
def mock_httpx_client():
    return MagicMock(spec=httpx.AsyncClient)


@pytest.fixture
def client(mock_httpx_client):
    return Client(client=mock_httpx_client)


@pytest.mark.asyncio
async def test_get_engine(client, mock_httpx_client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "engine": {"id": "re_123", "state": "ACTIVE", "timezone": "UTC"}
    }
    mock_httpx_client.get = AsyncMock(return_value=mock_response)

    engine = await client.get()

    assert engine.id == "re_123"
    assert engine.state == "ACTIVE"
    mock_httpx_client.get.assert_called_once_with("v3/site/rule_engine")


@pytest.mark.asyncio
async def test_get_engine_with_site_id(client, mock_httpx_client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "engine": {"id": "re_123", "state": "ACTIVE", "timezone": "UTC"}
    }
    mock_httpx_client.get = AsyncMock(return_value=mock_response)

    engine = await client.get(site_id="site_123")

    assert engine.id == "re_123"
    assert engine.state == "ACTIVE"
    mock_httpx_client.get.assert_called_once_with("v3/sites/site_123/rule_engine")


@pytest.mark.asyncio
async def test_suspend_engine(client, mock_httpx_client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "engine": {"id": "re_123", "state": "SUSPENDED", "timezone": "UTC"}
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    engine = await client.suspend(site_id="site_123")

    assert engine.state == "SUSPENDED"
    mock_httpx_client.post.assert_called_once_with(
        "v3/sites/site_123/rule_engine/suspend"
    )


@pytest.mark.asyncio
async def test_resume_engine(client, mock_httpx_client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "engine": {"id": "re_123", "state": "ACTIVE", "timezone": "UTC"}
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    engine = await client.resume()

    assert engine.state == "ACTIVE"
    mock_httpx_client.post.assert_called_once_with("v3/site/rule_engine/resume")
