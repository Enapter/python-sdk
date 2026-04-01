"""Unit tests for the Blueprints HTTP API client."""

import datetime
import io
import zipfile
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

import enapter


@pytest.fixture
def mock_httpx_client():
    """Fixture to provide a mocked httpx.AsyncClient."""
    return MagicMock(spec=httpx.AsyncClient)


@pytest.fixture
def client(mock_httpx_client):
    """Fixture to provide a Blueprints API client with a mocked internal client."""
    return enapter.http.api.blueprints.Client(client=mock_httpx_client)


@pytest.mark.asyncio
async def test_get_blueprint(client, mock_httpx_client):
    """Test getting a blueprint by ID."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "blueprint": {"id": "bp_123", "created_at": "2024-04-01T12:00:00+00:00"}
    }
    mock_httpx_client.get = AsyncMock(return_value=mock_response)

    blueprint = await client.get("bp_123")

    assert blueprint.id == "bp_123"
    assert blueprint.created_at == datetime.datetime.fromisoformat(
        "2024-04-01T12:00:00+00:00"
    )
    mock_httpx_client.get.assert_called_once_with("v3/blueprints/bp_123")


@pytest.mark.asyncio
async def test_upload_data(client, mock_httpx_client):
    """Test uploading raw data as a blueprint."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "blueprint": {"id": "bp_new", "created_at": "2024-04-01T12:00:00+00:00"}
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    data = b"blueprint content"
    blueprint = await client.upload(data)

    assert blueprint.id == "bp_new"
    assert blueprint.created_at == datetime.datetime.fromisoformat(
        "2024-04-01T12:00:00+00:00"
    )
    mock_httpx_client.post.assert_called_once_with("v3/blueprints/upload", content=data)


@pytest.mark.asyncio
async def test_upload_file(client, mock_httpx_client, tmp_path):
    """Test uploading a blueprint file."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "blueprint": {"id": "bp_file", "created_at": "2024-04-01T12:00:00+00:00"}
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    file_path = tmp_path / "manifest.yaml"
    file_path.write_bytes(b"manifest content")

    blueprint = await client.upload_file(file_path)

    assert blueprint.id == "bp_file"
    mock_httpx_client.post.assert_called_once_with(
        "v3/blueprints/upload", content=b"manifest content"
    )


@pytest.mark.asyncio
async def test_upload_directory(client, mock_httpx_client, tmp_path):
    """Test uploading a blueprint directory."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "blueprint": {"id": "bp_dir", "created_at": "2024-04-01T12:00:00+00:00"}
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    # Setup a directory with a file
    dir_path = tmp_path / "blueprint"
    dir_path.mkdir()
    file_path = dir_path / "manifest.yaml"
    file_path.write_bytes(b"manifest content")

    blueprint = await client.upload_directory(dir_path)

    assert blueprint.id == "bp_dir"

    # Verify a zip file was sent
    mock_httpx_client.post.assert_called_once()
    call_args = mock_httpx_client.post.call_args
    assert call_args[0][0] == "v3/blueprints/upload"
    sent_data = call_args[1]["content"]

    # Verify it's a valid zip file containing our file
    with zipfile.ZipFile(io.BytesIO(sent_data)) as zf:
        assert "manifest.yaml" in zf.namelist()
        assert zf.read("manifest.yaml") == b"manifest content"


@pytest.mark.asyncio
async def test_download(client, mock_httpx_client):
    """Test downloading a blueprint."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = b"zip content"
    mock_httpx_client.get = AsyncMock(return_value=mock_response)

    data = await client.download("bp_123")

    assert data == b"zip content"
    mock_httpx_client.get.assert_called_once_with(
        "v3/blueprints/bp_123/zip", params={"view": "ORIGINAL"}
    )


@pytest.mark.asyncio
async def test_validate_success(client, mock_httpx_client):
    """Test successful validation."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    await client.validate(b"blueprint content")

    mock_httpx_client.post.assert_called_once_with(
        "v3/blueprints/validate", content=b"blueprint content"
    )


@pytest.mark.asyncio
async def test_validate_error(client, mock_httpx_client):
    """Test validation with errors."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "validation_errors": ["Invalid manifest", "Missing field"]
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    with pytest.raises(enapter.http.api.MultiError) as exc_info:
        await client.validate(b"blueprint content")

    errors = exc_info.value.errors
    assert len(errors) == 2
    assert errors[0].message == "Invalid manifest"
    assert errors[1].message == "Missing field"
    mock_httpx_client.post.assert_called_once_with(
        "v3/blueprints/validate", content=b"blueprint content"
    )


@pytest.mark.asyncio
async def test_validate_file(client, mock_httpx_client, tmp_path):
    """Test validating a blueprint file."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    file_path = tmp_path / "manifest.yaml"
    file_path.write_bytes(b"manifest content")

    await client.validate_file(file_path)

    mock_httpx_client.post.assert_called_once_with(
        "v3/blueprints/validate", content=b"manifest content"
    )


@pytest.mark.asyncio
async def test_validate_directory(client, mock_httpx_client, tmp_path):
    """Test validating a blueprint directory."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    # Setup a directory with a file
    dir_path = tmp_path / "blueprint"
    dir_path.mkdir()
    file_path = dir_path / "manifest.yaml"
    file_path.write_bytes(b"manifest content")

    await client.validate_directory(dir_path)

    # Verify a zip file was sent
    mock_httpx_client.post.assert_called_once()
    call_args = mock_httpx_client.post.call_args
    assert call_args[0][0] == "v3/blueprints/validate"
    sent_data = call_args[1]["content"]

    # Verify it's a valid zip file containing our file
    with zipfile.ZipFile(io.BytesIO(sent_data)) as zf:
        assert "manifest.yaml" in zf.namelist()
        assert zf.read("manifest.yaml") == b"manifest content"
