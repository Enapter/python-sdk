import asyncio
import functools
import json
import os

import enapter


async def main():
    env_prefix = "ZIGBEE_"
    mqtt_client_config = enapter.mqtt.Config.from_env(prefix=env_prefix)
    device_factory = functools.partial(
        ZigbeeMqtt,
        mqtt_client_config=mqtt_client_config,
        mqtt_topic=os.environ[env_prefix + "MQTT_TOPIC"],
        sensor_manufacturer=os.environ[env_prefix + "SENSOR_MANUFACTURER"],
        sensor_model=os.environ[env_prefix + "SENSOR_MODEL"],
    )
    await enapter.vucm.run(device_factory)


class ZigbeeMqtt(enapter.vucm.Device):
    def __init__(
        self,
        mqtt_client_config,
        mqtt_topic,
        sensor_manufacturer,
        sensor_model,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.telemetry = {}

        self.mqtt_client_config = mqtt_client_config
        self.mqtt_topic = mqtt_topic

        self.sensor_manufacturer = sensor_manufacturer
        self.sensor_model = sensor_model

    async def task_consume(self):
        async with enapter.mqtt.Client(self.mqtt_client_config) as client:
            async with client.subscribe(self.mqtt_topic) as messages:
                async for msg in messages:
                    try:
                        self.telemetry = json.loads(msg.payload)
                    except json.JSONDecodeError as e:
                        await self.log.error(f"failed to decode json payload: {e}")

    async def task_telemetry_sender(self):
        while True:
            await self.send_telemetry(self.telemetry)
            await asyncio.sleep(1)

    async def task_properties_sender(self):
        while True:
            await self.send_properties(
                {
                    "model": self.sensor_model,
                    "manufacturer": self.sensor_manufacturer,
                }
            )
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
