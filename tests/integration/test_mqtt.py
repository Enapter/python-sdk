import asyncio
import contextlib
import time

import aiomqtt

import enapter


class TestClient:
    async def test_sanity(self, enapter_mqtt_client):
        async with contextlib.AsyncExitStack() as stack:
            heartbit_sender = await stack.enter_async_context(
                HeartbitSender(enapter_mqtt_client)
            )
            messages = await stack.enter_async_context(
                enapter_mqtt_client.subscribe(heartbit_sender.topic)
            )
            msg = await messages.__anext__()
            assert int(msg.payload) <= time.time()

    async def test_consume_after_another_subscriber_left(self, enapter_mqtt_client):
        async with contextlib.AsyncExitStack() as stack:
            heartbit_sender = await stack.enter_async_context(
                HeartbitSender(enapter_mqtt_client)
            )
            async with enapter_mqtt_client.subscribe(
                heartbit_sender.topic
            ) as messages_1:
                msg = await messages_1.__anext__()
                assert int(msg.payload) <= time.time()
                async with enapter_mqtt_client.subscribe(
                    heartbit_sender.topic
                ) as messages_2:
                    msg = await messages_2.__anext__()
                    assert int(msg.payload) <= time.time()
                msg = await messages_1.__anext__()
                assert int(msg.payload) <= time.time()

    async def test_two_subscriptions(self, enapter_mqtt_client):
        async with contextlib.AsyncExitStack() as stack:
            heartbit_sender = await stack.enter_async_context(
                HeartbitSender(enapter_mqtt_client)
            )
            for i in range(2):
                async with enapter_mqtt_client.subscribe(
                    heartbit_sender.topic
                ) as messages:
                    msg = await messages.__anext__()
                    assert int(msg.payload) <= time.time()

    async def test_two_subscribers(self, enapter_mqtt_client):
        async with contextlib.AsyncExitStack() as stack:
            heartbit_sender = await stack.enter_async_context(
                HeartbitSender(enapter_mqtt_client)
            )
            messages_1 = await stack.enter_async_context(
                enapter_mqtt_client.subscribe(heartbit_sender.topic)
            )
            messages_2 = await stack.enter_async_context(
                enapter_mqtt_client.subscribe(heartbit_sender.topic)
            )
            for messages in [messages_1, messages_2]:
                msg = await messages.__anext__()
                assert int(msg.payload) <= time.time()

    async def test_broker_restart(self, mosquitto_container, enapter_mqtt_client):
        async with contextlib.AsyncExitStack() as stack:
            heartbit_sender = await stack.enter_async_context(
                HeartbitSender(enapter_mqtt_client)
            )
            messages = await stack.enter_async_context(
                enapter_mqtt_client.subscribe(heartbit_sender.topic)
            )
            msg = await messages.__anext__()
            assert int(msg.payload) <= time.time()
            mosquitto_container.restart()
            msg = await messages.__anext__()
            assert int(msg.payload) <= time.time()


class HeartbitSender(enapter.async_.Routine):
    def __init__(self, enapter_mqtt_client, topic="heartbits", interval=0.5):
        self.enapter_mqtt_client = enapter_mqtt_client
        self.topic = topic
        self.interval = interval

    async def _run(self):
        self._started.set()

        while True:
            payload = str(int(time.time()))
            try:
                await self.enapter_mqtt_client.publish(self.topic, payload)
            except aiomqtt.error.MqttError as e:
                print(f"failed to publish heartbit: {e}")
            await asyncio.sleep(self.interval)
