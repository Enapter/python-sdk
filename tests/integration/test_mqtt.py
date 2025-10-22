import asyncio
import time

import aiomqtt


class TestClient:

    async def test_sanity(self, enapter_mqtt_client):
        async with asyncio.TaskGroup() as tg:
            heartbit_sender = HeartbitSender(tg, enapter_mqtt_client)
            async with enapter_mqtt_client.subscribe(heartbit_sender.topic) as messages:
                msg = await messages.__anext__()
                assert int(msg.payload) <= time.time()
            heartbit_sender.cancel()

    async def test_consume_after_another_subscriber_left(self, enapter_mqtt_client):
        async with asyncio.TaskGroup() as tg:
            heartbit_sender = HeartbitSender(tg, enapter_mqtt_client)
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
            heartbit_sender.cancel()

    async def test_two_subscriptions(self, enapter_mqtt_client):
        async with asyncio.TaskGroup() as tg:
            heartbit_sender = HeartbitSender(tg, enapter_mqtt_client)
            for i in range(2):
                async with enapter_mqtt_client.subscribe(
                    heartbit_sender.topic
                ) as messages:
                    msg = await messages.__anext__()
                    assert int(msg.payload) <= time.time()
            heartbit_sender.cancel()

    async def test_two_subscribers(self, enapter_mqtt_client):
        async with asyncio.TaskGroup() as tg:
            heartbit_sender = HeartbitSender(tg, enapter_mqtt_client)
            async with enapter_mqtt_client.subscribe(
                heartbit_sender.topic
            ) as messages_1:
                async with enapter_mqtt_client.subscribe(
                    heartbit_sender.topic
                ) as messages_2:
                    for messages in [messages_1, messages_2]:
                        msg = await messages.__anext__()
                        assert int(msg.payload) <= time.time()
            heartbit_sender.cancel()

    async def test_broker_restart(self, mosquitto_container, enapter_mqtt_client):
        async with asyncio.TaskGroup() as tg:
            heartbit_sender = HeartbitSender(tg, enapter_mqtt_client)
            async with enapter_mqtt_client.subscribe(heartbit_sender.topic) as messages:
                msg = await messages.__anext__()
                assert int(msg.payload) <= time.time()
                mosquitto_container.restart()
                msg = await messages.__anext__()
                assert int(msg.payload) <= time.time()
            heartbit_sender.cancel()


class HeartbitSender:

    def __init__(
        self, task_group, enapter_mqtt_client, topic="heartbits", interval=0.5
    ):
        self.enapter_mqtt_client = enapter_mqtt_client
        self.topic = topic
        self.interval = interval
        self._task = task_group.create_task(self._run())

    def cancel(self):
        self._task.cancel()

    async def _run(self):
        while True:
            payload = str(int(time.time()))
            try:
                await self.enapter_mqtt_client.publish(self.topic, payload)
            except aiomqtt.MqttError as e:
                print(f"failed to publish heartbit: {e}")
            await asyncio.sleep(self.interval)
