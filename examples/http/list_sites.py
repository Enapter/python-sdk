import asyncio

import enapter


async def main():
    config = enapter.http.api.Config.from_env()
    async with enapter.http.api.Client(config=config) as client:
        async for site in client.sites.list():
            print(site)


if __name__ == "__main__":
    asyncio.run(main())
