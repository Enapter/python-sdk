import asyncio
import time

import enapter


async def main() -> None:
    config = enapter.mqtt.Config(host="127.0.0.1", port=1883)
    async with enapter.mqtt.Client(config=config) as client:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(subscriber(client))
            tg.create_task(publisher(client))


async def subscriber(client: enapter.mqtt.Client) -> None:
    async with client.subscribe("/+") as messages:
        async for msg in messages:
            print(msg.topic, msg.payload.decode())


async def publisher(client: enapter.mqtt.Client) -> None:
    while True:
        try:
            await client.publish(topic="/time", payload=str(time.time()))
        except enapter.mqtt.Error as e:
            print("error", e)
        await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
