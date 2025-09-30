import asyncio
import contextlib
import logging
import ssl
import tempfile

import aiomqtt

import enapter

LOGGER = logging.getLogger(__name__)


class Client(enapter.async_.Routine):
    def __init__(self, config):
        self._logger = self._new_logger(config)
        self._config = config
        self._mdns_resolver = enapter.mdns.Resolver()
        self._tls_context = self._new_tls_context(config)
        self._publisher = None
        self._publisher_connected = asyncio.Event()

    @staticmethod
    def _new_logger(config):
        extra = {"host": config.host, "port": config.port}
        return logging.LoggerAdapter(LOGGER, extra=extra)

    def config(self):
        return self._config

    async def publish(self, *args, **kwargs):
        await self._publisher_connected.wait()
        await self._publisher.publish(*args, **kwargs)

    @enapter.async_.generator
    async def subscribe(self, *topics):
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

    async def _run(self):
        self._logger.info("starting")
        self._started.set()
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
                self._logger.info("publisher disconnected")

    @contextlib.asynccontextmanager
    async def _connect(self):
        host = await self._maybe_resolve_mdns(self._config.host)
        async with aiomqtt.Client(
            hostname=host,
            port=self._config.port,
            username=self._config.user,
            password=self._config.password,
            logger=self._logger,
            tls_context=self._tls_context,
        ) as client:
            yield client

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
