import asyncio
import time

import enapter


async def subscriber(client: enapter.mqtt.Client) -> None:
    async with client.subscribe("/+") as messages:
        async for msg in messages:
            print(msg.topic, msg.payload.decode())


async def publisher(client: enapter.mqtt.Client) -> None:
    while True:
        await client.publish(topic="/time", payload=str(time.time()))
        await asyncio.sleep(1)


async def main() -> None:
    config = enapter.mqtt.Config(host="127.0.0.1", port=1883)
    async with enapter.mqtt.Client(config=config) as client:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(subscriber(client))
            tg.create_task(publisher(client))


if __name__ == "__main__":
    asyncio.run(main())
