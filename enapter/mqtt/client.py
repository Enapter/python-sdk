import asyncio
import collections
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
        self._client = None
        self._client_ready = asyncio.Event()
        self._subscribers = collections.defaultdict(int)

    @staticmethod
    def _new_logger(config):
        extra = {"host": config.host, "port": config.port}
        return logging.LoggerAdapter(LOGGER, extra=extra)

    def config(self):
        return self._config

    async def publish(self, *args, **kwargs):
        client = await self._wait_client()
        await client.publish(*args, **kwargs)

    @enapter.async_.generator
    async def subscribe(self, topic):
        while True:
            client = await self._wait_client()

            try:
                async with client.messages() as messages:
                    async with self._subscribe(client, topic):
                        async for msg in messages:
                            if msg.topic.matches(topic):
                                yield msg

            except aiomqtt.MqttError as e:
                self._logger.error(e)
                retry_interval = 5
                await asyncio.sleep(retry_interval)

    @contextlib.asynccontextmanager
    async def _subscribe(self, client, topic):
        first_subscriber = not self._subscribers[topic]
        self._subscribers[topic] += 1
        try:
            if first_subscriber:
                await client.subscribe(topic)
            yield
        finally:
            self._subscribers[topic] -= 1
            assert not self._subscribers[topic] < 0
            last_unsubscriber = not self._subscribers[topic]
            if last_unsubscriber:
                del self._subscribers[topic]
                await client.unsubscribe(topic)

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

                    # tracking disconnect
                    async with client.messages() as messages:
                        async for msg in messages:
                            pass
            except aiomqtt.MqttError as e:
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
            async with aiomqtt.Client(
                hostname=host,
                port=self._config.port,
                username=self._config.user,
                password=self._config.password,
                logger=self._logger,
                tls_context=self._tls_context,
            ) as client:
                yield client
        except asyncio.CancelledError:
            # FIXME: A cancelled `aiomqtt.Client.connect` leaks resources.
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
