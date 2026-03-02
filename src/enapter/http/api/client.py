from typing import Self

import httpx

from enapter.http.api import (
    blueprints,
    commands,
    devices,
    rule_engine,
    sites,
    telemetry,
)

from .auth import Auth
from .config import Config
from .transport import Transport


class Client:

    def __init__(self, config: Config, transport: Transport | None = None) -> None:
        self._config = config
        self._own_transport = transport is None
        self._transport = transport if transport is not None else Transport()
        self._client = self._new_client()

    def _new_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            auth=self._new_auth(),
            headers=self._new_headers(),
            base_url=self._config.base_url,
            transport=self._transport,
        )

    def _new_auth(self) -> Auth:
        return Auth(token=self._config.token, user=self._config.user)

    def _new_headers(self) -> dict[str, str]:
        headers = {}
        if self._config.allow_http:
            headers["X-Enapter-Allow-HTTP"] = "true"
        return headers

    async def __aenter__(self) -> Self:
        if self._own_transport:
            await self._transport.__aenter__()
        return self

    async def __aexit__(self, *exc) -> None:
        if self._own_transport:
            await self._transport.__aexit__(*exc)

    @property
    def transport(self) -> Transport:
        return self._transport

    @property
    def devices(self) -> devices.Client:
        return devices.Client(client=self._client)

    @property
    def sites(self) -> sites.Client:
        return sites.Client(client=self._client)

    @property
    def commands(self) -> commands.Client:
        return commands.Client(client=self._client)

    @property
    def blueprints(self) -> blueprints.Client:
        return blueprints.Client(client=self._client)

    @property
    def telemetry(self) -> telemetry.Client:
        return telemetry.Client(client=self._client)

    @property
    def rule_engine(self) -> rule_engine.Client:
        return rule_engine.Client(client=self._client)
