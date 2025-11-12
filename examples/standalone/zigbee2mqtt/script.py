import asyncio
import json
import os

import enapter


async def main():
    async with enapter.mqtt.Client(
        hostname=os.environ["ZIGBEE_MQTT_HOST"],
        port=int(os.environ["ZIGBEE_MQTT_PORT"]),
        username=os.environ.get("ZIGBEE_MQTT_USER"),
        password=os.environ.get("ZIGBEE_MQTT_PASSWORD"),
    ) as mqtt_client:
        zigbee_mqtt = ZigbeeMQTT(
            mqtt_client=mqtt_client,
            mqtt_topic=os.environ["ZIGBEE_MQTT_TOPIC"],
            sensor_manufacturer=os.environ["ZIGBEE_SENSOR_MANUFACTURER"],
            sensor_model=os.environ["ZIGBEE_SENSOR_MODEL"],
        )
        await enapter.standalone.run(zigbee_mqtt)


class ZigbeeMQTT(enapter.standalone.Device):

    def __init__(self, mqtt_client, mqtt_topic, sensor_manufacturer, sensor_model):
        super().__init__()
        self.telemetry = {}
        self.mqtt_client = mqtt_client
        self.mqtt_topic = mqtt_topic
        self.sensor_manufacturer = sensor_manufacturer
        self.sensor_model = sensor_model

    async def run(self):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.mqtt_consumer())
            tg.create_task(self.telemetry_sender())
            tg.create_task(self.properties_sender())

    async def mqtt_consumer(self):
        async with self.mqtt_client.subscribe(self.mqtt_topic) as messages:
            async for msg in messages:
                try:
                    self.telemetry = json.loads(msg.payload)
                except json.JSONDecodeError as e:
                    await self.log.error(f"failed to decode json payload: {e}")

    async def telemetry_sender(self):
        while True:
            await self.send_telemetry(self.telemetry)
            await asyncio.sleep(1)

    async def properties_sender(self):
        while True:
            await self.send_properties(
                {
                    "model": self.sensor_model,
                    "manufacturer": self.sensor_manufacturer,
                }
            )
            await asyncio.sleep(10)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
