"""Unit tests for the Blueprints HTTP API client."""

import io
import zipfile
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

import enapter
from enapter.http.api.blueprints.blueprint import BlueprintView


@pytest.fixture
def mock_client():
    """Fixture to provide a mocked httpx.AsyncClient."""
    return MagicMock(spec=httpx.AsyncClient)


@pytest.fixture
def blueprints_client(mock_client):
    """Fixture to provide a Blueprints API client with a mocked internal client."""
    return enapter.http.api.blueprints.Client(client=mock_client)


@pytest.mark.asyncio
async def test_get_blueprint(blueprints_client, mock_client):
    """Test getting a specific blueprint by ID."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "blueprint": {
            "id": "bp_123",
            "created_at": "2023-01-01T12:00:00+00:00",
        }
    }
    mock_client.get = AsyncMock(return_value=mock_response)

    blueprint = await blueprints_client.get(blueprint_id="bp_123")

    assert blueprint.id == "bp_123"
    mock_client.get.assert_called_once_with("v3/blueprints/bp_123")


@pytest.mark.asyncio
async def test_upload_blueprint(blueprints_client, mock_client):
    """Test uploading a blueprint from bytes."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "blueprint": {
            "id": "bp_123",
            "created_at": "2023-01-01T12:00:00+00:00",
        }
    }
    mock_client.post = AsyncMock(return_value=mock_response)

    data = b"test blueprint data"
    blueprint = await blueprints_client.upload(data=data)

    assert blueprint.id == "bp_123"
    mock_client.post.assert_called_once_with("v3/blueprints/upload", content=data)


@pytest.mark.asyncio
async def test_upload_file(blueprints_client, mock_client, tmp_path):
    """Test uploading a blueprint from a file."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "blueprint": {
            "id": "bp_123",
            "created_at": "2023-01-01T12:00:00+00:00",
        }
    }
    mock_client.post = AsyncMock(return_value=mock_response)

    bp_file = tmp_path / "blueprint.zip"
    data = b"test blueprint file data"
    bp_file.write_bytes(data)

    blueprint = await blueprints_client.upload_file(path=bp_file)

    assert blueprint.id == "bp_123"
    mock_client.post.assert_called_once_with("v3/blueprints/upload", content=data)


@pytest.mark.asyncio
async def test_upload_directory(blueprints_client, mock_client, tmp_path):
    """Test uploading a blueprint from a directory."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "blueprint": {
            "id": "bp_123",
            "created_at": "2023-01-01T12:00:00+00:00",
        }
    }
    mock_client.post = AsyncMock(return_value=mock_response)

    bp_dir = tmp_path / "blueprint_dir"
    bp_dir.mkdir()
    (bp_dir / "main.lua").write_text("print('hello')")

    blueprint = await blueprints_client.upload_directory(path=bp_dir)

    assert blueprint.id == "bp_123"
    mock_client.post.assert_called_once()
    args, kwargs = mock_client.post.call_args
    assert args[0] == "v3/blueprints/upload"

    zipped_content = kwargs["content"]
    with zipfile.ZipFile(io.BytesIO(zipped_content)) as zf:
        assert "main.lua" in zf.namelist()
        assert zf.read("main.lua") == b"print('hello')"


@pytest.mark.asyncio
async def test_download_blueprint(blueprints_client, mock_client):
    """Test downloading a blueprint."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = b"blueprint zip content"
    mock_client.get = AsyncMock(return_value=mock_response)

    content = await blueprints_client.download(blueprint_id="bp_123")

    assert content == b"blueprint zip content"
    mock_client.get.assert_called_once_with(
        "v3/blueprints/bp_123/zip", params={"view": "ORIGINAL"}
    )


@pytest.mark.asyncio
async def test_download_blueprint_compiled(blueprints_client, mock_client):
    """Test downloading a compiled blueprint."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = b"compiled blueprint zip content"
    mock_client.get = AsyncMock(return_value=mock_response)

    content = await blueprints_client.download(
        blueprint_id="bp_123", view=BlueprintView.COMPILED
    )

    assert content == b"compiled blueprint zip content"
    mock_client.get.assert_called_once_with(
        "v3/blueprints/bp_123/zip", params={"view": "COMPILED"}
    )


@pytest.mark.asyncio
async def test_validate_blueprint(blueprints_client, mock_client):
    """Test validating a blueprint from bytes."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_client.post = AsyncMock(return_value=mock_response)

    data = b"test blueprint data"
    await blueprints_client.validate(data=data)

    mock_client.post.assert_called_once_with("v3/blueprints/validate", content=data)


@pytest.mark.asyncio
async def test_validate_blueprint_with_errors(blueprints_client, mock_client):
    """Test validating a blueprint with errors."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"validation_errors": ["Error 1", "Error 2"]}
    mock_client.post = AsyncMock(return_value=mock_response)

    data = b"invalid blueprint data"
    with pytest.raises(enapter.http.api.MultiError) as excinfo:
        await blueprints_client.validate(data=data)

    assert len(excinfo.value.errors) == 2
    assert excinfo.value.errors[0].message == "Error 1"
    assert excinfo.value.errors[1].message == "Error 2"


@pytest.mark.asyncio
async def test_validate_file(blueprints_client, mock_client, tmp_path):
    """Test validating a blueprint from a file."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_client.post = AsyncMock(return_value=mock_response)

    bp_file = tmp_path / "blueprint.zip"
    data = b"test blueprint file data"
    bp_file.write_bytes(data)

    await blueprints_client.validate_file(path=bp_file)

    mock_client.post.assert_called_once_with("v3/blueprints/validate", content=data)


@pytest.mark.asyncio
async def test_validate_directory(blueprints_client, mock_client, tmp_path):
    """Test validating a blueprint from a directory."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_client.post = AsyncMock(return_value=mock_response)

    bp_dir = tmp_path / "blueprint_dir"
    bp_dir.mkdir()
    (bp_dir / "main.lua").write_text("print('hello')")

    await blueprints_client.validate_directory(path=bp_dir)

    mock_client.post.assert_called_once()
    args, kwargs = mock_client.post.call_args
    assert args[0] == "v3/blueprints/validate"

    zipped_content = kwargs["content"]
    with zipfile.ZipFile(io.BytesIO(zipped_content)) as zf:
        assert "main.lua" in zf.namelist()
        assert zf.read("main.lua") == b"print('hello')"
