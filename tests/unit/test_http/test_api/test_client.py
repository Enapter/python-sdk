"""Unit tests for the HTTP API client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import enapter


@pytest.mark.asyncio
async def test_client_context_manager():
    """Test that the client can be used as an asynchronous context manager."""
    config = enapter.http.api.config.Config(
        base_url="https://api.enapter.com", token="test_token"
    )
    async with enapter.http.api.client.Client(config=config) as client:
        assert isinstance(client, enapter.http.api.client.Client)


def test_client_properties():
    """Test that the client provides access to sub-clients."""
    config = enapter.http.api.config.Config(
        base_url="https://api.enapter.com", token="test_token"
    )
    client = enapter.http.api.client.Client(config=config)

    assert isinstance(client.devices, enapter.http.api.devices.Client)
    assert isinstance(client.sites, enapter.http.api.sites.Client)
    assert isinstance(client.commands, enapter.http.api.commands.Client)
    assert isinstance(client.blueprints, enapter.http.api.blueprints.Client)
    assert isinstance(client.telemetry, enapter.http.api.telemetry.Client)


@pytest.mark.asyncio
async def test_client_custom_transport():
    """Test that a custom transport can be provided to the client."""
    config = enapter.http.api.config.Config(
        base_url="https://api.enapter.com", token="test_token"
    )
    custom_transport = enapter.http.api.transport.Transport()
    async with enapter.http.api.client.Client(
        config=config, transport=custom_transport
    ) as client:
        assert client.transport is custom_transport


@pytest.mark.asyncio
async def test_client_manages_own_transport():
    """Test that the client manages the lifecycle of its own transport."""
    config = enapter.http.api.config.Config(
        base_url="https://api.enapter.com", token="test_token"
    )
    with patch("enapter.http.api.client.Transport", autospec=True) as transport_mock:
        transport_instance = transport_mock.return_value
        transport_instance.__aenter__ = AsyncMock(return_value=transport_instance)
        transport_instance.__aexit__ = AsyncMock(return_value=None)

        async with enapter.http.api.client.Client(config=config):
            pass

        assert transport_instance.__aenter__.called
        assert transport_instance.__aexit__.called


@pytest.mark.asyncio
async def test_client_does_not_manage_custom_transport():
    """Test that the client does not manage the lifecycle of a custom transport."""
    config = enapter.http.api.config.Config(
        base_url="https://api.enapter.com", token="test_token"
    )
    custom_transport = MagicMock(spec=enapter.http.api.transport.Transport)
    custom_transport.__aenter__ = AsyncMock()
    custom_transport.__aexit__ = AsyncMock()

    async with enapter.http.api.client.Client(
        config=config, transport=custom_transport
    ):
        pass

    assert not custom_transport.__aenter__.called
    assert not custom_transport.__aexit__.called
