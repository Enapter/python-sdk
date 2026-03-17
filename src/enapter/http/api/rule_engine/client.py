"""Rule Engine HTTP API client."""

import time
from typing import Any, Callable

import httpx

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

    async def list_rules(self, site_id: str | None = None) -> list[Rule]:
        """List all rules."""
        url = f"{self._url(site_id)}/rules"
        response = await self._client.get(url)
        await api.check_error(response)
        return [Rule.from_dto(dto) for dto in response.json()["rules"]]

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
