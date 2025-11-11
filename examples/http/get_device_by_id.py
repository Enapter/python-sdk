import asyncio
import os

import enapter


async def main():
    config = enapter.http.api.Config.from_env()
    device_id = os.environ["DEVICE_ID"]
    async with enapter.http.api.Client(config=config) as client:
        device = await client.devices.get(device_id)
        print(device)


if __name__ == "__main__":
    asyncio.run(main())
