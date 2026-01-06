import asyncio
import json

import enapter


async def main():
    config = enapter.http.api.Config.from_env()
    async with enapter.http.api.Client(config=config) as client:
        async with client.sites.list() as sites:
            async for site in sites:
                print(json.dumps(site.to_dto()))


if __name__ == "__main__":
    asyncio.run(main())
