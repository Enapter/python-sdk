import asyncio
import time

import enapter


class TestMQTT:
    async def test_sanity(self, enapter_mqtt_client):
        async with HeartbitSender(enapter_mqtt_client) as heartbit_sender:
            async with enapter_mqtt_client.subscribe(heartbit_sender.topic) as messages:
                async for msg in messages:
                    assert int(msg.payload) <= time.time()
                    return


class HeartbitSender(enapter.async_.Routine):
    def __init__(self, enapter_mqtt_client, topic="heartbits", interval=1):
        self.enapter_mqtt_client = enapter_mqtt_client
        self.topic = topic
        self.interval = interval

    async def _run(self):
        self._started.set()

        while True:
            payload = str(int(time.time()))
            await self.enapter_mqtt_client.publish(self.topic, payload)
            await asyncio.sleep(self.interval)
