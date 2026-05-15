"""Rule Engine HTTP API client."""

import time
from typing import Any, AsyncGenerator, Callable

import httpx

from enapter import async_
from enapter.http import api

from .engine import Engine
from .rule import Rule
from .rule_script import RuleScript


class Client:
    """Client for Rule Engine management."""

    def __init__(
        self,
        client: httpx.AsyncClient,
        rule_slug_generator: Callable[[], str] | None = None,
    ) -> None:
        """Initialize the client."""
        self._client = client
        self._rule_slug_generator = rule_slug_generator or random_rule_slug

    async def get(self, site_id: str | None = None) -> Engine:
        """Get the rule engine state."""
        url = self._url(site_id)
        response = await self._client.get(url)
        await api.check_error(response)
        return Engine.from_dto(response.json()["engine"])

    async def suspend(self, site_id: str | None = None) -> Engine:
        """Suspend the rule engine."""
        url = f"{self._url(site_id)}/suspend"
        response = await self._client.post(url)
        await api.check_error(response)
        return Engine.from_dto(response.json()["engine"])

    async def resume(self, site_id: str | None = None) -> Engine:
        """Resume the rule engine."""
        url = f"{self._url(site_id)}/resume"
        response = await self._client.post(url)
        await api.check_error(response)
        return Engine.from_dto(response.json()["engine"])

    @async_.generator
    async def list_rules(
        self, site_id: str | None = None, offset: int = 0, limit: int | None = None
    ) -> AsyncGenerator[Rule, None]:
        """List all rules."""

        # 1. Probe request: Older gateways will reject requests with unknown parameters
        # like 'offset'. We make an initial request with offset=0 (which is omitted
        # from params) to safely check if the gateway supports pagination.
        rules, total_count = await self._list_rules(site_id=site_id, offset=0)

        if not rules:
            return

        # 2. Legacy gateway fallback: If the API returns rules but omits 'total_count',
        # our default will be 0. Since we already checked that we have rules,
        # total_count=0 indicates an old, unpaginated rule engine.
        # It returns all rules at once. We simulate pagination locally and return
        # immediately to avoid making subsequent requests with offset > 0,
        # which would result in an error.
        if total_count == 0:
            sliced_rules = rules[offset:]
            if limit is not None:
                sliced_rules = sliced_rules[:limit]

            for rule in sliced_rules:
                yield rule
            return

        # 3. Modern gateway: The gateway returned a positive 'total_count', indicating it
        # supports standard pagination parameters. We delegate to the paginate utility.
        async def fetch(current_offset: int) -> list[Rule]:
            page_rules, _ = await self._list_rules(
                site_id=site_id, offset=current_offset
            )
            return page_rules

        async with api.paginate(fetch, offset=offset, limit=limit) as stream:
            async for rule in stream:
                yield rule

    async def _list_rules(
        self, site_id: str | None, offset: int
    ) -> tuple[list[Rule], int]:
        url = f"{self._url(site_id)}/rules"
        params = {}

        # We must NOT send offset=0 to legacy gateways, as they actively reject
        # unknown parameters with a fatal error.
        if offset != 0:
            params["offset"] = offset

        response = await self._client.get(url, params=params)
        await api.check_error(response)

        payload = response.json()
        rules = [Rule.from_dto(dto) for dto in payload["rules"]]
        total_count = payload.get("total_count", 0)

        return rules, total_count

    async def get_rule(self, rule_id: str, site_id: str | None = None) -> Rule:
        """Get a single rule."""
        url = f"{self._url(site_id)}/rules/{rule_id}"
        response = await self._client.get(url)
        await api.check_error(response)
        return Rule.from_dto(response.json()["rule"])

    async def create_rule(
        self,
        script: RuleScript,
        slug: str | None = None,
        site_id: str | None = None,
        disable: bool | None = None,
    ) -> Rule:
        """Create a new rule."""
        if slug is None:
            slug = self._rule_slug_generator()

        url = f"{self._url(site_id)}/rules"
        payload: dict[str, Any] = {
            "slug": slug,
            "script": script.to_dto(),
        }
        if disable is not None:
            payload["disable"] = disable

        response = await self._client.post(url, json=payload)
        await api.check_error(response)
        return Rule.from_dto(response.json()["rule"])

    async def update_rule(
        self,
        rule_id: str,
        slug: str,
        site_id: str | None = None,
    ) -> Rule:
        """Update a rule's slug."""
        url = f"{self._url(site_id)}/rules/{rule_id}"
        payload = {"slug": slug}
        response = await self._client.patch(url, json=payload)
        await api.check_error(response)
        return Rule.from_dto(response.json()["rule"])

    async def update_rule_script(
        self,
        rule_id: str,
        script: RuleScript,
        site_id: str | None = None,
    ) -> Rule:
        """Update a rule's script."""
        url = f"{self._url(site_id)}/rules/{rule_id}/update_script"
        payload = {"script": script.to_dto()}
        response = await self._client.post(url, json=payload)
        await api.check_error(response)
        return Rule.from_dto(response.json()["rule"])

    async def enable_rule(self, rule_id: str, site_id: str | None = None) -> Rule:
        """Enable a rule."""
        url = f"{self._url(site_id)}/rules/{rule_id}/enable"
        response = await self._client.post(url)
        await api.check_error(response)
        return Rule.from_dto(response.json()["rule"])

    async def disable_rule(self, rule_id: str, site_id: str | None = None) -> Rule:
        """Disable a rule."""
        url = f"{self._url(site_id)}/rules/{rule_id}/disable"
        response = await self._client.post(url)
        await api.check_error(response)
        return Rule.from_dto(response.json()["rule"])

    async def delete_rule(self, rule_id: str, site_id: str | None = None) -> None:
        """Delete a rule."""
        url = f"{self._url(site_id)}/rules/{rule_id}"
        response = await self._client.delete(url)
        await api.check_error(response)

    def _url(self, site_id: str | None) -> str:
        """Construct the URL for the rule engine endpoint."""
        if site_id is not None:
            return f"v3/sites/{site_id}/rule_engine"
        return "v3/site/rule_engine"


def random_rule_slug() -> str:
    timestamp = int(time.time())
    return f"rule-{timestamp}"
