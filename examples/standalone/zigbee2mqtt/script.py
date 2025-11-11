import asyncio
import json
import os

import enapter


async def main():
    env_prefix = "ZIGBEE_"
    mqtt_client_config = enapter.mqtt.Config.from_env(prefix=env_prefix)
    zigbee_mqtt = ZigbeeMqtt(
        mqtt_client_config=mqtt_client_config,
        mqtt_topic=os.environ[env_prefix + "MQTT_TOPIC"],
        sensor_manufacturer=os.environ[env_prefix + "SENSOR_MANUFACTURER"],
        sensor_model=os.environ[env_prefix + "SENSOR_MODEL"],
    )
    await enapter.standalone.run(zigbee_mqtt)


class ZigbeeMqtt(enapter.standalone.Device):

    def __init__(
        self, mqtt_client_config, mqtt_topic, sensor_manufacturer, sensor_model
    ):
        super().__init__()
        self.telemetry = {}
        self.mqtt_client_config = mqtt_client_config
        self.mqtt_topic = mqtt_topic
        self.sensor_manufacturer = sensor_manufacturer
        self.sensor_model = sensor_model

    async def run(self):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.consumer(tg))
            tg.create_task(self.telemetry_sender())
            tg.create_task(self.properties_sender())

    async def consumer(self, tg):
        async with enapter.mqtt.Client(
            self.mqtt_client_config, task_group=tg
        ) as client:
            async with client.subscribe(self.mqtt_topic) as messages:
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
