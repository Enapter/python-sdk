import asyncio
import os
import time

import enapter


async def main() -> None:
    hardware_id = os.environ["HARDWARE_ID"]
    channel_id = os.environ["CHANNEL_ID"]
    config = enapter.mqtt.api.Config(
        host=os.environ["MQTT_HOST"],
        port=int(os.environ["MQTT_PORT"]),
        tls_config=enapter.mqtt.api.TLSConfig(
            secret_key=os.environ["MQTT_TLS_SECRET_KEY"],
            cert=os.environ["MQTT_TLS_CERT"],
            ca_cert=os.environ["MQTT_TLS_CA_CERT"],
        ),
    )
    async with enapter.mqtt.api.Client(config=config) as client:
        device_channel = client.device_channel(
            hardware_id=hardware_id, channel_id=channel_id
        )
        ucm_channel = client.device_channel(
            hardware_id=hardware_id, channel_id=channel_id
        )
        simulator = RL6Simulator(device_channel=device_channel, ucm_channel=ucm_channel)
        await simulator.run()


class RL6Simulator:

    def __init__(
        self,
        device_channel: enapter.mqtt.api.device.Channel,
        ucm_channel: enapter.mqtt.api.device.Channel,
    ) -> None:
        self.device_channel = device_channel
        self.ucm_channel = ucm_channel
        self.loads = {
            "r1": False,
            "r2": False,
            "r3": False,
            "r4": False,
            "r5": False,
            "r6": False,
        }

    async def run(self) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.command_handler())
            tg.create_task(self.telemetry_publisher())
            tg.create_task(self.properties_publisher())
            # NOTE: The following two tasks are necessary only when connecting
            # to Cloud v2.
            tg.create_task(self.ucm_properties_publisher())
            tg.create_task(self.ucm_telemetry_publisher())

    async def command_handler(self) -> None:
        async with self.device_channel.subscribe_to_command_requests() as requests:
            async for request in requests:
                match request.name:
                    case "enable_load":
                        response = self.handle_enable_load_command(request)
                    case "disable_load":
                        response = self.handle_disable_load_command(request)
                    case _:
                        response = self.handle_unknown_command(request)
                try:
                    await self.device_channel.publish_command_response(response)
                except enapter.mqtt.Error as e:
                    print("failed to publish command response: " + str(e))

    def handle_enable_load_command(
        self,
        request: enapter.mqtt.api.device.CommandRequest,
    ) -> enapter.mqtt.api.device.CommandResponse:
        load = request.arguments.get("load")
        if load not in self.loads:
            return request.new_response(
                state=enapter.mqtt.api.device.CommandState.ERROR,
                payload={"reason": "load invalid or missing"},
            )
        self.loads[load] = True
        return request.new_response(
            state=enapter.mqtt.api.device.CommandState.COMPLETED, payload={}
        )

    def handle_disable_load_command(
        self,
        request: enapter.mqtt.api.device.CommandRequest,
    ) -> enapter.mqtt.api.device.CommandResponse:
        load = request.arguments.get("load")
        if load not in self.loads:
            return request.new_response(
                state=enapter.mqtt.api.device.CommandState.ERROR,
                payload={"reason": "load invalid or missing"},
            )
        self.loads[load] = False
        return request.new_response(
            state=enapter.mqtt.api.device.CommandState.COMPLETED, payload={}
        )

    def handle_unknown_command(
        self,
        request: enapter.mqtt.api.device.CommandRequest,
    ) -> enapter.mqtt.api.device.CommandResponse:
        return request.new_response(
            state=enapter.mqtt.api.device.CommandState.ERROR,
            payload={"reason": "command unknown"},
        )

    async def telemetry_publisher(self) -> None:
        while True:
            telemetry = enapter.mqtt.api.device.Telemetry(
                timestamp=int(time.time()), alerts=[], values=self.loads.copy()
            )
            try:
                await self.device_channel.publish_telemetry(telemetry)
            except enapter.mqtt.Error as e:
                print("failed to publish telemetry: " + str(e))
            await asyncio.sleep(1)

    async def properties_publisher(self) -> None:
        while True:
            properties = enapter.mqtt.api.device.Properties(
                timestamp=int(time.time()), values={}
            )
            try:
                await self.device_channel.publish_properties(properties)
            except enapter.mqtt.Error as e:
                print("failed to publish properties: " + str(e))
            await asyncio.sleep(10)

    async def ucm_telemetry_publisher(self) -> None:
        while True:
            telemetry = enapter.mqtt.api.device.Telemetry(
                timestamp=int(time.time()), alerts=[], values={}
            )
            try:
                await self.ucm_channel.publish_telemetry(telemetry)
            except enapter.mqtt.Error as e:
                print("failed to publish ucm telemetry: " + str(e))
            await asyncio.sleep(1)

    async def ucm_properties_publisher(self) -> None:
        while True:
            properties = enapter.mqtt.api.device.Properties(
                timestamp=int(time.time()), values={"virtual": True, "lua_api_ver": 1}
            )
            try:
                await self.ucm_channel.publish_properties(properties)
            except enapter.mqtt.Error as e:
                print("failed to publish ucm properties: " + str(e))
            await asyncio.sleep(10)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
