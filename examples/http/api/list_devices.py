import asyncio
import json

import enapter


async def main():
    config = enapter.http.api.Config.from_env()
    async with enapter.http.api.Client(config=config) as client:
        async with client.devices.list() as devices:
            async for device in devices:
                print(json.dumps(device.to_dto()))


if __name__ == "__main__":
    asyncio.run(main())
