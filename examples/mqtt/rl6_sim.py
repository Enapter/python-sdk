import asyncio
import json
import os
import time
from typing import Any, Dict

import enapter


async def main() -> None:
    hardware_id = os.environ["HARDWARE_ID"]
    channel_id = os.environ["CHANNEL_ID"]
    mqtt_config = enapter.mqtt.Config(
        host=os.environ["MQTT_HOST"],
        port=int(os.environ["MQTT_PORT"]),
        tls=enapter.mqtt.TLSConfig(
            secret_key=os.environ["MQTT_TLS_SECRET_KEY"],
            cert=os.environ["MQTT_TLS_CERT"],
            ca_cert=os.environ["MQTT_TLS_CA_CERT"],
        ),
    )
    async with enapter.mqtt.Client(config=mqtt_config) as client:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(command_handler(client, hardware_id, channel_id))
            tg.create_task(telemetry_publisher(client, hardware_id, channel_id))
            tg.create_task(properties_publisher(client, hardware_id, channel_id))
            # NOTE: The following two tasks are necessary only when connecting
            # to Cloud v2.
            tg.create_task(ucm_properties_publisher(client, hardware_id))
            tg.create_task(ucm_telemetry_publisher(client, hardware_id))


async def command_handler(
    client: enapter.mqtt.Client, hardware_id: str, channel_id: str
) -> None:
    async with client.subscribe(
        f"v1/to/{hardware_id}/{channel_id}/v1/command/requests"
    ) as messages:
        async for msg in messages:
            request = json.loads(msg.payload)
            match request["name"]:
                case "enable_load":
                    response = handle_enable_load_command(request)
                case "disable_load":
                    response = handle_disable_load_command(request)
                case _:
                    response = handle_unknown_command(request)
            try:
                await client.publish(
                    topic=f"v1/from/{hardware_id}/{channel_id}/v1/command/responses",
                    payload=json.dumps(response),
                )
            except enapter.mqtt.Error as e:
                print("failed to publish command response: " + str(e))


LOADS = {
    "r1": False,
    "r2": False,
    "r3": False,
    "r4": False,
    "r5": False,
    "r6": False,
}


def handle_enable_load_command(request: Dict[str, Any]) -> Dict[str, Any]:
    arguments = request.get("arguments", {})
    load = arguments.get("load")
    if load not in LOADS:
        return {
            "id": request["id"],
            "state": "error",
            "payload": {"reason": "load invalid or missing"},
        }
    LOADS[load] = True
    return {
        "id": request["id"],
        "state": "completed",
        "payload": {},
    }


def handle_disable_load_command(request: Dict[str, Any]) -> Dict[str, Any]:
    args = request.get("args", {})
    load = args.get("load")
    if load not in LOADS:
        return {
            "id": request["id"],
            "state": "error",
            "payload": {"reason": "load invalid or missing"},
        }
    LOADS[load] = False
    return {
        "id": request["id"],
        "state": "completed",
        "payload": {},
    }


def handle_unknown_command(request: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": request["id"],
        "state": "error",
        "payload": {"reason": "command unknown"},
    }


async def telemetry_publisher(
    client: enapter.mqtt.Client, hardware_id: str, channel_id: str
) -> None:
    while True:
        try:
            telemetry = {
                "timestamp": int(time.time()),
                **LOADS,
            }
            await client.publish(
                topic=f"v1/from/{hardware_id}/{channel_id}/v1/telemetry",
                payload=json.dumps(telemetry),
            )
        except enapter.mqtt.Error as e:
            print("failed to publish telemetry: " + str(e))
        await asyncio.sleep(1)


async def properties_publisher(
    client: enapter.mqtt.Client, hardware_id: str, channel_id: str
) -> None:
    while True:
        try:
            properties = {
                "timestamp": int(time.time()),
            }
            await client.publish(
                topic=f"v1/from/{hardware_id}/{channel_id}/v1/properties",
                payload=json.dumps(properties),
            )
        except enapter.mqtt.Error as e:
            print("failed to publish properties: " + str(e))
        await asyncio.sleep(10)


async def ucm_telemetry_publisher(
    client: enapter.mqtt.Client, hardware_id: str
) -> None:
    while True:
        try:
            telemetry = {
                "timestamp": int(time.time()),
            }
            await client.publish(
                topic=f"v1/from/{hardware_id}/ucm/v1/telemetry",
                payload=json.dumps(telemetry),
            )
        except enapter.mqtt.Error as e:
            print("failed to publish ucm telemetry: " + str(e))
        await asyncio.sleep(1)


async def ucm_properties_publisher(
    client: enapter.mqtt.Client, hardware_id: str
) -> None:
    while True:
        try:
            properties = {
                "timestamp": int(time.time()),
                "virtual": True,
                "lua_api_ver": 1,
            }
            await client.publish(
                topic=f"v1/from/{hardware_id}/ucm/v1/register",
                payload=json.dumps(properties),
            )
        except enapter.mqtt.Error as e:
            print("failed to publish ucm properties: " + str(e))
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
