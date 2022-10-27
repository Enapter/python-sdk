import asyncio
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
        self._lock = asyncio.Lock()
        self._client = None
        self._client_ready = asyncio.Event()

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
        client = None

        while True:
            await self._client_ready.wait()
            async with self._lock:
                if self._client_ready.is_set():
                    client = self._client
                    break

        await client.publish(*args, **kwargs)

    @async_.generator
    async def subscribe(self, topic):
        while True:
            client = None

            while True:
                await self._client_ready.wait()
                async with self._lock:
                    if self._client_ready.is_set():
                        client = self._client
                        break

            try:
                async with client.filtered_messages(topic) as messages:
                    await client.subscribe(topic)
                    async for msg in messages:
                        yield msg

            except asyncio_mqtt.MqttError as e:
                self._logger.error(e)
                retry_interval = 5
                await asyncio.sleep(retry_interval)

    async def _run(self):
        self._logger.info("starting")

        self._started.set()

        while True:
            try:
                async with self._connect() as client:
                    async with self._lock:
                        self._client = client
                        self._client_ready.set()
                        self._logger.info("client ready")

                    async with client.unfiltered_messages() as messages:
                        async for message in messages:
                            self._logger.warn(
                                "received unfiltered message: %s", message.topic
                            )
            except asyncio_mqtt.MqttError as e:
                self._logger.error(e)
                retry_interval = 5
                await asyncio.sleep(retry_interval)
            finally:
                async with self._lock:
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
