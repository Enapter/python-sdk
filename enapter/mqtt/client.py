import asyncio
import collections
import contextlib
import logging
import ssl
import tempfile

import asyncio_mqtt

from .. import async_, mdns
from .device_channel import DeviceChannel

LOGGER = logging.getLogger(__name__)


class Client(async_.Routine):
    def __init__(self, config):
        self._logger = self._new_logger(config)
        self._config = config
        self._mdns_resolver = mdns.Resolver()
        self._tls_context = self._new_tls_context(config)
        self._client = None
        self._client_ready = asyncio.Event()
        self._subscribers = collections.defaultdict(int)
        self._subscribers_changed = asyncio.Event()

    @staticmethod
    def _new_logger(config):
        extra = {"host": config.host, "port": config.port}
        return logging.LoggerAdapter(LOGGER, extra=extra)

    def config(self):
        return self._config

    def device_channel(self, hardware_id, channel_id):
        return DeviceChannel(
            client=self, hardware_id=hardware_id, channel_id=channel_id
        )

    async def publish(self, *args, **kwargs):
        client = await self._wait_client()
        await client.publish(*args, **kwargs)

    @contextlib.asynccontextmanager
    async def subscribe(self, topic):
        self._subscribers[topic] += 1
        self._subscribers_changed.set()
        self._logger.debug(f"going to subscribe to {topic}")

        try:
            async with self._consume(topic) as messages:
                yield messages

        finally:
            self._subscribers[topic] -= 1
            self._subscribers_changed.set()
            self._logger.debug(f"going to unsubscribe from {topic}")

    @async_.generator
    async def _consume(self, topic):
        while True:
            client = await self._wait_client()

            try:
                async with client.messages() as messages:
                    async for msg in messages:
                        # FIXME: Each consumer processes all messages.
                        if msg.topic.matches(topic):
                            yield msg

            except asyncio_mqtt.MqttError as e:
                self._logger.error(e)
                retry_interval = 5
                await asyncio.sleep(retry_interval)

    async def _wait_client(self):
        await self._client_ready.wait()
        assert self._client_ready.is_set()
        return self._client

    async def _run(self):
        self._logger.info("starting")

        self._started.set()

        while True:
            try:
                async with self._connect() as client:
                    self._client = client
                    self._client_ready.set()
                    self._logger.info("client ready")

                    while True:
                        await self._sync_subscriptions(client)
                        await self._subscribers_changed.wait()
                        self._subscribers_changed.clear()

            except asyncio_mqtt.MqttError as e:
                self._logger.error(e)
                retry_interval = 5
                await asyncio.sleep(retry_interval)
            finally:
                self._client_ready.clear()
                self._client = None
                self._logger.info("client not ready")

    @contextlib.asynccontextmanager
    async def _connect(self):
        host = await self._maybe_resolve_mdns(self._config.host)

        try:
            async with asyncio_mqtt.Client(
                hostname=host,
                port=self._config.port,
                username=self._config.user,
                password=self._config.password,
                logger=self._logger,
                tls_context=self._tls_context,
            ) as client:
                yield client
        except asyncio.CancelledError:
            # FIXME: A cancelled `asyncio_mqtt.Client.connect` leaks resources.
            raise

    async def _sync_subscriptions(self, client):
        subscribers = self._subscribers.copy()

        actions = {}

        for topic, count in list(subscribers.items()):
            if count:
                actions[topic] = client.subscribe
            else:
                actions[topic] = client.unsubscribe
                del self._subscribers[topic]

        for topic, action in actions.items():
            await action(topic)

    @staticmethod
    def _new_tls_context(config):
        if not config.tls_enabled:
            return None

        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.check_hostname = False
        ctx.load_verify_locations(None, None, config.tls_ca_cert)

        with contextlib.ExitStack() as stack:
            certfile = stack.enter_context(tempfile.NamedTemporaryFile())
            certfile.write(config.tls_cert.encode())
            certfile.flush()

            keyfile = stack.enter_context(tempfile.NamedTemporaryFile())
            keyfile.write(config.tls_secret_key.encode())
            keyfile.flush()

            ctx.load_cert_chain(certfile.name, keyfile=keyfile.name)

        return ctx

    async def _maybe_resolve_mdns(self, host):
        if not host.endswith(".local"):
            return host

        while True:
            try:
                return await self._mdns_resolver.resolve(host)
            except Exception as e:
                self._logger.error("failed to resolve mDNS host %r: %s", host, e)
                retry_interval = 5
                await asyncio.sleep(retry_interval)
