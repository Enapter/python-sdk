from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

import enapter


@pytest.fixture
def mock_client():
    return MagicMock(spec=httpx.AsyncClient)


@pytest.fixture
def sites_client(mock_client):
    return enapter.http.api.sites.Client(client=mock_client)


@pytest.mark.asyncio
async def test_create_site(sites_client, mock_client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "site": {
            "id": "site_123",
            "name": "Test Site",
            "timezone": "UTC",
            "version": "V3",
            "location": {"name": "Test Location", "latitude": 1.0, "longitude": 2.0},
        }
    }
    mock_client.post = AsyncMock(return_value=mock_response)

    location = enapter.http.api.sites.Location(
        name="Test Location", latitude=1.0, longitude=2.0
    )
    site = await sites_client.create(
        name="Test Site", timezone="UTC", location=location
    )

    assert site.id == "site_123"
    assert site.name == "Test Site"
    assert site.location.name == "Test Location"
    mock_client.post.assert_called_once_with(
        "v3/sites",
        json={
            "name": "Test Site",
            "timezone": "UTC",
            "location": {"name": "Test Location", "latitude": 1.0, "longitude": 2.0},
        },
    )


@pytest.mark.asyncio
async def test_get_site(sites_client, mock_client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "site": {
            "id": "site_123",
            "name": "Test Site",
            "timezone": "UTC",
            "version": "V3",
        }
    }
    mock_client.get = AsyncMock(return_value=mock_response)

    site = await sites_client.get(site_id="site_123")

    assert site.id == "site_123"
    mock_client.get.assert_called_once_with("v3/sites/site_123")


@pytest.mark.asyncio
async def test_list_sites(sites_client, mock_client):
    mock_response_1 = MagicMock(spec=httpx.Response)
    mock_response_1.status_code = 200
    mock_response_1.json.return_value = {
        "sites": [
            {"id": "site_1", "name": "Site 1", "timezone": "UTC", "version": "V3"},
            {"id": "site_2", "name": "Site 2", "timezone": "UTC", "version": "V3"},
        ]
    }

    mock_response_2 = MagicMock(spec=httpx.Response)
    mock_response_2.status_code = 200
    mock_response_2.json.return_value = {"sites": []}

    mock_client.get = AsyncMock(side_effect=[mock_response_1, mock_response_2])

    sites = []
    async with sites_client.list() as s_gen:
        async for s in s_gen:
            sites.append(s)

    assert len(sites) == 2
    assert sites[0].id == "site_1"
    assert sites[1].id == "site_2"
    assert mock_client.get.call_count == 2


@pytest.mark.asyncio
async def test_update_site(sites_client, mock_client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "site": {
            "id": "site_123",
            "name": "Updated Site",
            "timezone": "UTC",
            "version": "V3",
        }
    }
    mock_client.patch = AsyncMock(return_value=mock_response)

    site = await sites_client.update(site_id="site_123", name="Updated Site")

    assert site.name == "Updated Site"
    mock_client.patch.assert_called_once_with(
        "v3/sites/site_123",
        json={"name": "Updated Site", "timezone": None, "location": None},
    )


@pytest.mark.asyncio
async def test_delete_site(sites_client, mock_client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 204
    mock_client.delete = AsyncMock(return_value=mock_response)

    await sites_client.delete(site_id="site_123")

    mock_client.delete.assert_called_once_with("v3/sites/site_123")
