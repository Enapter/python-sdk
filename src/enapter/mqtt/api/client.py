import asyncio
import contextlib
import ssl
import tempfile
from typing import Self

from enapter import mqtt
from enapter.mqtt.api import device

from .config import Config


class Client:

    def __init__(self, config: Config, task_group: asyncio.TaskGroup | None) -> None:
        self._config = config
        self._client = self._new_client(task_group=task_group)

    async def __aenter__(self) -> Self:
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc) -> None:
        await self._client.__aexit__(*exc)

    def device_channel(self, hardware_id: str, channel_id: str) -> device.Channel:
        return device.Channel(
            client=self._client, hardware_id=hardware_id, channel_id=channel_id
        )

    def _new_client(self, task_group: asyncio.TaskGroup | None) -> mqtt.Client:
        return mqtt.Client(
            hostname=self._config.host,
            port=self._config.port,
            username=self._config.user,
            password=self._config.password,
            tls_context=self._new_tls_context(),
            task_group=task_group,
        )

    def _new_tls_context(self) -> ssl.SSLContext | None:
        if self._config.tls is None:
            return None

        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.check_hostname = False
        ctx.load_verify_locations(None, None, self._config.tls.ca_cert)

        with contextlib.ExitStack() as stack:
            certfile = stack.enter_context(tempfile.NamedTemporaryFile())
            certfile.write(self._config.tls.cert.encode())
            certfile.flush()

            keyfile = stack.enter_context(tempfile.NamedTemporaryFile())
            keyfile.write(self._config.tls.secret_key.encode())
            keyfile.flush()

            ctx.load_cert_chain(certfile.name, keyfile=keyfile.name)

        return ctx
