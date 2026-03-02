import asyncio
import os

from enapter.http.api import Client, Config


async def main():
    token = os.getenv("ENAPTER_API_TOKEN", "YOUR_TOKEN")
    config = Config(base_url="https://api.enapter.com", token=token)

    async with Client(config) as client:
        # Get current rule engine status for the default site
        engine = await client.rule_engine.get()
        print(f"Rule engine ID: {engine.id}")
        print(f"Current state: {engine.state.value}")
        print(f"Timezone: {engine.timezone}")

        # Suspend the rule engine
        # engine = await client.rule_engine.suspend()
        # print(f"Rule engine suspended. Current state: {engine.state}")

        # Resume the rule engine
        # engine = await client.rule_engine.resume()
        # print(f"Rule engine resumed. Current state: {engine.state}")

        # You can also specify a site_id
        # engine = await client.rule_engine.get(site_id="your-site-id")
        # print(f"Rule engine state for site: {engine.state}")


if __name__ == "__main__":
    asyncio.run(main())
