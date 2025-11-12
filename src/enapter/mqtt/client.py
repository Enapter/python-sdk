import asyncio
import contextlib
import logging
import ssl
from typing import AsyncGenerator

import aiomqtt  # type: ignore

from enapter import async_, mdns

from .message import Message

LOGGER = logging.getLogger(__name__)


class Client(async_.Routine):

    def __init__(
        self,
        hostname: str,
        port: int = 1883,
        *,
        username: str | None = None,
        password: str | None = None,
        tls_context: ssl.SSLContext | None = None,
        task_group: asyncio.TaskGroup | None = None
    ) -> None:
        super().__init__(task_group=task_group)
        self._logger = logging.LoggerAdapter(
            LOGGER, extra={"hostname": hostname, "port": port}
        )
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password
        self._tls_context = tls_context
        self._mdns_resolver = mdns.Resolver()
        self._publisher: aiomqtt.Client | None = None
        self._publisher_connected = asyncio.Event()

    async def publish(self, *args, **kwargs) -> None:
        await self._publisher_connected.wait()
        assert self._publisher is not None
        await self._publisher.publish(*args, **kwargs)

    @async_.generator
    async def subscribe(self, *topics: str) -> AsyncGenerator[Message, None]:
        while True:
            try:
                async with self._connect() as subscriber:
                    for topic in topics:
                        await subscriber.subscribe(topic)
                    self._logger.info("subscriber [%s] connected", ",".join(topics))
                    async for msg in subscriber.messages:
                        yield msg
            except aiomqtt.MqttError as e:
                self._logger.error(e)
                retry_interval = 5
                await asyncio.sleep(retry_interval)

    async def _run(self) -> None:
        self._logger.info("starting")
        while True:
            try:
                async with self._connect() as publisher:
                    self._logger.info("publisher connected")
                    self._publisher = publisher
                    self._publisher_connected.set()
                    async for msg in publisher.messages:
                        pass
            except aiomqtt.MqttError as e:
                self._logger.error(e)
                retry_interval = 5
                await asyncio.sleep(retry_interval)
            finally:
                self._publisher_connected.clear()
                self._publisher = None

    @contextlib.asynccontextmanager
    async def _connect(self) -> AsyncGenerator[aiomqtt.Client, None]:
        hostname = await self._maybe_resolve_hostname()
        async with _new_aiomqtt_client(
            hostname=hostname,
            port=self._port,
            username=self._username,
            password=self._password,
            logger=LOGGER,
            tls_context=self._tls_context,
        ) as client:
            yield client

    async def _maybe_resolve_hostname(self) -> str:
        if not self._hostname.endswith(".local"):
            return self._hostname

        while True:
            try:
                return await self._mdns_resolver.resolve(self._hostname)
            except Exception as e:
                self._logger.error("failed to resolve mDNS host: %s", e)
                retry_interval = 5
                await asyncio.sleep(retry_interval)


@contextlib.asynccontextmanager
async def _new_aiomqtt_client(*args, **kwargs) -> AsyncGenerator[aiomqtt.Client, None]:
    """
    Creates `aiomqtt.Client` shielding `__aenter__` from cancellation.

    See:
        - https://github.com/empicano/aiomqtt/issues/377
    """
    client = aiomqtt.Client(*args, **kwargs)
    setup_task = asyncio.create_task(client.__aenter__())
    try:
        await asyncio.shield(setup_task)
    except asyncio.CancelledError as e:
        await setup_task
        await client.__aexit__(type(e), e, e.__traceback__)
        raise
    try:
        yield client
    except BaseException as e:
        await client.__aexit__(type(e), e, e.__traceback__)
        raise
    else:
        await client.__aexit__(None, None, None)
