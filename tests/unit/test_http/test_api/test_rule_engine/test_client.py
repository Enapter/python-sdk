"""Unit tests for the Rule Engine HTTP API client."""

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
    """Fixture to provide a Rule Engine API client with a mocked internal client."""
    return enapter.http.api.rule_engine.Client(client=mock_httpx_client)


@pytest.mark.asyncio
async def test_get_engine(client, mock_httpx_client):
    """Test getting the rule engine state."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "engine": {"id": "re_123", "state": "ACTIVE", "timezone": "UTC"}
    }
    mock_httpx_client.get = AsyncMock(return_value=mock_response)

    engine = await client.get()

    assert engine.id == "re_123"
    assert engine.state == enapter.http.api.rule_engine.EngineState.ACTIVE
    mock_httpx_client.get.assert_called_once_with("v3/site/rule_engine")


@pytest.mark.asyncio
async def test_get_engine_with_site_id(client, mock_httpx_client):
    """Test getting the rule engine state for a specific site ID."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "engine": {"id": "re_123", "state": "ACTIVE", "timezone": "UTC"}
    }
    mock_httpx_client.get = AsyncMock(return_value=mock_response)

    engine = await client.get(site_id="site_123")

    assert engine.id == "re_123"
    assert engine.state == enapter.http.api.rule_engine.EngineState.ACTIVE
    mock_httpx_client.get.assert_called_once_with("v3/sites/site_123/rule_engine")


@pytest.mark.asyncio
async def test_suspend_engine(client, mock_httpx_client):
    """Test suspending the rule engine."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "engine": {"id": "re_123", "state": "SUSPENDED", "timezone": "UTC"}
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    engine = await client.suspend(site_id="site_123")

    assert engine.state == enapter.http.api.rule_engine.EngineState.SUSPENDED
    mock_httpx_client.post.assert_called_once_with(
        "v3/sites/site_123/rule_engine/suspend"
    )


@pytest.mark.asyncio
async def test_resume_engine(client, mock_httpx_client):
    """Test resuming the rule engine."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "engine": {"id": "re_123", "state": "ACTIVE", "timezone": "UTC"}
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    engine = await client.resume()

    assert engine.state == enapter.http.api.rule_engine.EngineState.ACTIVE
    mock_httpx_client.post.assert_called_once_with("v3/site/rule_engine/resume")


@pytest.mark.asyncio
async def test_list_rules(client, mock_httpx_client):
    """Test listing rules."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rules": [
            {
                "id": "rule_1",
                "slug": "rule-1",
                "disabled": False,
                "state": "STARTED",
                "script": {"code": "cHJpbnQoJzEnKQ==", "runtime_version": "V3"},
            },
            {
                "id": "rule_2",
                "slug": "rule-2",
                "disabled": True,
                "state": "STOPPED",
                "script": {"code": "cHJpbnQoJzInKQ==", "runtime_version": "V3"},
            },
        ],
        "total_count": 2,
    }
    mock_httpx_client.get = AsyncMock(
        side_effect=[
            mock_response,
            mock_response,
            MagicMock(
                spec=httpx.Response,
                status_code=200,
                json=lambda: {"rules": [], "total_count": 2},
            ),
        ]
    )

    rules = []
    async with client.list_rules(site_id="site_123") as stream:
        async for rule in stream:
            rules.append(rule)

    assert len(rules) == 2
    assert rules[0].id == "rule_1"
    assert rules[0].slug == "rule-1"
    assert rules[0].state == enapter.http.api.rule_engine.RuleState.STARTED
    assert rules[1].id == "rule_2"
    assert rules[1].disabled is True
    assert rules[1].state == enapter.http.api.rule_engine.RuleState.STOPPED
    assert mock_httpx_client.get.call_count == 3


@pytest.mark.asyncio
async def test_list_rules_pagination(client, mock_httpx_client):
    """Test listing rules with pagination."""
    mock_response_1 = MagicMock(spec=httpx.Response)
    mock_response_1.status_code = 200
    mock_response_1.json.return_value = {
        "rules": [
            {
                "id": f"rule_{i}",
                "slug": f"rule-{i}",
                "disabled": False,
                "state": "STARTED",
                "script": {"code": "cHJpbnQoJzEnKQ==", "runtime_version": "V3"},
            }
            for i in range(50)
        ],
        "total_count": 51,
    }

    mock_response_2 = MagicMock(spec=httpx.Response)
    mock_response_2.status_code = 200
    mock_response_2.json.return_value = {
        "rules": [
            {
                "id": "rule_50",
                "slug": "rule-50",
                "disabled": False,
                "state": "STARTED",
                "script": {"code": "cHJpbnQoJzEnKQ==", "runtime_version": "V3"},
            }
        ],
        "total_count": 51,
    }

    mock_response_3 = MagicMock(spec=httpx.Response)
    mock_response_3.status_code = 200
    mock_response_3.json.return_value = {"rules": [], "total_count": 51}

    mock_httpx_client.get = AsyncMock(
        side_effect=[
            mock_response_1,
            mock_response_1,
            mock_response_2,
            mock_response_3,
        ]
    )

    rules = []
    async with client.list_rules(site_id="site_123") as stream:
        async for rule in stream:
            rules.append(rule)

    assert len(rules) == 51
    assert rules[0].id == "rule_0"
    assert rules[50].id == "rule_50"

    assert mock_httpx_client.get.call_count == 4


@pytest.mark.asyncio
async def test_list_rules_unpaginated_workaround(client, mock_httpx_client):
    """Test listing rules when the API ignores pagination and total_count is missing."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    # No "total_count" in the payload
    mock_response.json.return_value = {
        "rules": [
            {
                "id": "rule_1",
                "slug": "rule-1",
                "disabled": False,
                "state": "STARTED",
                "script": {"code": "cHJpbnQoJzEnKQ==", "runtime_version": "V3"},
            }
        ]
    }
    mock_httpx_client.get = AsyncMock(return_value=mock_response)

    rules = []
    # If the workaround is NOT implemented, this will loop forever because paginate()
    # will keep calling _list_rules with increasing offsets, and _list_rules will
    # keep returning the same rule_1.
    async with client.list_rules(site_id="site_123") as stream:
        async for rule in stream:
            rules.append(rule)
            if len(rules) > 10:
                pytest.fail("Infinite loop detected in list_rules")

    # With the workaround, it should only return the rule once (for offset 0)
    # and then terminate because yielded_count >= total_count (1 >= 1).
    assert len(rules) == 1
    assert rules[0].id == "rule_1"
    assert mock_httpx_client.get.call_count == 1


@pytest.mark.asyncio
async def test_get_rule(client, mock_httpx_client):
    """Test getting a single rule."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rule": {
            "id": "rule_123",
            "slug": "test-rule",
            "disabled": False,
            "state": "STARTED",
            "script": {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"},
        }
    }
    mock_httpx_client.get = AsyncMock(return_value=mock_response)

    rule = await client.get_rule(rule_id="rule_123", site_id="site_123")

    assert rule.id == "rule_123"
    assert rule.slug == "test-rule"
    assert rule.state == enapter.http.api.rule_engine.RuleState.STARTED
    mock_httpx_client.get.assert_called_once_with(
        "v3/sites/site_123/rule_engine/rules/rule_123"
    )


@pytest.mark.asyncio
async def test_create_rule(client, mock_httpx_client):
    """Test creating a new rule."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rule": {
            "id": "rule_123",
            "slug": "test-rule",
            "disabled": False,
            "state": "STARTED",
            "script": {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"},
        }
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    script = enapter.http.api.rule_engine.RuleScript(
        code="print('hello')",
        runtime_version=enapter.http.api.rule_engine.RuntimeVersion.V3,
    )

    rule = await client.create_rule(
        script=script,
        slug="test-rule",
        site_id="site_123",
    )

    assert rule.id == "rule_123"
    assert rule.slug == "test-rule"
    mock_httpx_client.post.assert_called_once_with(
        "v3/sites/site_123/rule_engine/rules",
        json={
            "slug": "test-rule",
            "script": {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"},
        },
    )


@pytest.mark.asyncio
async def test_create_rule_automatic_slug(mock_httpx_client):
    """Test creating a new rule with automatic slug generation."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rule": {
            "id": "rule_123",
            "slug": "rule_1234567890",
            "disabled": False,
            "state": "STARTED",
            "script": {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"},
        }
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    def rule_slug_generator():
        return "rule_1234567890"

    client = enapter.http.api.rule_engine.Client(
        client=mock_httpx_client, rule_slug_generator=rule_slug_generator
    )

    script = enapter.http.api.rule_engine.RuleScript(
        code="print('hello')",
        runtime_version=enapter.http.api.rule_engine.RuntimeVersion.V3,
    )

    rule = await client.create_rule(script=script, site_id="site_123")

    assert rule.slug == "rule_1234567890"
    mock_httpx_client.post.assert_called_once_with(
        "v3/sites/site_123/rule_engine/rules",
        json={
            "slug": "rule_1234567890",
            "script": {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"},
        },
    )


@pytest.mark.asyncio
async def test_update_rule(client, mock_httpx_client):
    """Test updating a rule's slug."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rule": {
            "id": "rule_123",
            "slug": "new-slug",
            "disabled": False,
            "state": "STARTED",
            "script": {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"},
        }
    }
    mock_httpx_client.patch = AsyncMock(return_value=mock_response)

    rule = await client.update_rule(
        rule_id="rule_123",
        slug="new-slug",
        site_id="site_123",
    )

    assert rule.slug == "new-slug"
    mock_httpx_client.patch.assert_called_once_with(
        "v3/sites/site_123/rule_engine/rules/rule_123",
        json={"slug": "new-slug"},
    )


@pytest.mark.asyncio
async def test_update_rule_script(client, mock_httpx_client):
    """Test updating a rule's script."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rule": {
            "id": "rule_123",
            "slug": "test-rule",
            "disabled": False,
            "state": "STARTED",
            "script": {"code": "cHJpbnQoJ25ldycp", "runtime_version": "V3"},
        }
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    script = enapter.http.api.rule_engine.RuleScript(
        code="print('new')",
        runtime_version=enapter.http.api.rule_engine.RuntimeVersion.V3,
    )

    rule = await client.update_rule_script(
        rule_id="rule_123",
        script=script,
        site_id="site_123",
    )

    assert rule.script.code == "print('new')"
    mock_httpx_client.post.assert_called_once_with(
        "v3/sites/site_123/rule_engine/rules/rule_123/update_script",
        json={"script": {"code": "cHJpbnQoJ25ldycp", "runtime_version": "V3"}},
    )


@pytest.mark.asyncio
async def test_delete_rule(client, mock_httpx_client):
    """Test deleting a rule."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 204
    mock_httpx_client.delete = AsyncMock(return_value=mock_response)

    await client.delete_rule(rule_id="rule_123", site_id="site_123")

    mock_httpx_client.delete.assert_called_once_with(
        "v3/sites/site_123/rule_engine/rules/rule_123"
    )


@pytest.mark.asyncio
async def test_enable_rule(client, mock_httpx_client):
    """Test enabling a rule."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rule": {
            "id": "rule_123",
            "slug": "test-rule",
            "disabled": False,
            "state": "STARTED",
            "script": {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"},
        }
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    rule = await client.enable_rule(rule_id="rule_123", site_id="site_123")

    assert rule.disabled is False
    mock_httpx_client.post.assert_called_once_with(
        "v3/sites/site_123/rule_engine/rules/rule_123/enable"
    )


@pytest.mark.asyncio
async def test_disable_rule(client, mock_httpx_client):
    """Test disabling a rule."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rule": {
            "id": "rule_123",
            "slug": "test-rule",
            "disabled": True,
            "state": "STOPPED",
            "script": {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"},
        }
    }
    mock_httpx_client.post = AsyncMock(return_value=mock_response)

    rule = await client.disable_rule(rule_id="rule_123", site_id="site_123")

    assert rule.disabled is True
    mock_httpx_client.post.assert_called_once_with(
        "v3/sites/site_123/rule_engine/rules/rule_123/disable"
    )


@pytest.mark.asyncio
async def test_list_rules_legacy_with_offset(client, mock_httpx_client):
    """Test legacy gateway with a non-zero offset."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    # Legacy: items present, total_count missing
    mock_response.json.return_value = {
        "rules": [
            {
                "id": "r1",
                "slug": "s1",
                "disabled": False,
                "state": "STARTED",
                "script": {"code": "", "runtime_version": "V3"},
            },
            {
                "id": "r2",
                "slug": "s2",
                "disabled": False,
                "state": "STARTED",
                "script": {"code": "", "runtime_version": "V3"},
            },
            {
                "id": "r3",
                "slug": "s3",
                "disabled": False,
                "state": "STARTED",
                "script": {"code": "", "runtime_version": "V3"},
            },
        ]
    }
    mock_httpx_client.get = AsyncMock(return_value=mock_response)

    rules = []
    # Request offset 1
    async with client.list_rules(site_id="site_123", offset=1) as stream:
        async for rule in stream:
            rules.append(rule)

    assert len(rules) == 2
    assert rules[0].id == "r2"
    assert rules[1].id == "r3"
    # Should only make one request (the probe)
    assert mock_httpx_client.get.call_count == 1


@pytest.mark.asyncio
async def test_list_rules_modern_empty_no_total_count(client, mock_httpx_client):
    """Test modern gateway returning empty results and omitting total_count."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"rules": []}
    mock_httpx_client.get = AsyncMock(return_value=mock_response)

    rules = []
    async with client.list_rules(site_id="site_123") as stream:
        async for rule in stream:
            rules.append(rule)

    assert len(rules) == 0
    assert mock_httpx_client.get.call_count == 1


@pytest.mark.asyncio
async def test_list_rules_modern_offset_beyond_total(client, mock_httpx_client):
    """Test modern gateway when offset is beyond total rules."""
    mock_response_probe = MagicMock(spec=httpx.Response)
    mock_response_probe.status_code = 200
    mock_response_probe.json.return_value = {
        "rules": [
            {
                "id": "r1",
                "slug": "s1",
                "disabled": False,
                "state": "STARTED",
                "script": {"code": "", "runtime_version": "V3"},
            }
        ],
        "total_count": 1,
    }

    mock_response_empty = MagicMock(spec=httpx.Response)
    mock_response_empty.status_code = 200
    mock_response_empty.json.return_value = {"rules": [], "total_count": 1}

    mock_httpx_client.get = AsyncMock(
        side_effect=[mock_response_probe, mock_response_empty]
    )

    rules = []
    # Offset 10 on a site with only 1 rule
    async with client.list_rules(site_id="site_123", offset=10) as stream:
        async for rule in stream:
            rules.append(rule)

    assert len(rules) == 0
    # 1 probe + 1 actual fetch
    assert mock_httpx_client.get.call_count == 2
