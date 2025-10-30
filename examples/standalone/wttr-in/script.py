import asyncio
import os

import python_weather

import enapter


async def main():
    async with python_weather.Client() as client:
        await enapter.standalone.run(
            WttrIn(client=client, location=os.environ["WTTR_IN_LOCATION"])
        )


class WttrIn(enapter.standalone.Device):

    def __init__(self, client, location):
        super().__init__()
        self.client = client
        self.location = location

    async def run(self):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.properties_sender())
            tg.create_task(self.telemetry_sender())

    async def properties_sender(self):
        while True:
            await self.send_properties({"location": self.location})
            await asyncio.sleep(10)

    async def telemetry_sender(self):
        while True:
            try:
                weather = await self.client.get(self.location)
                await self.send_telemetry({"temperature": weather.temperature})
            except Exception as e:
                await self.log.error(f"failed to get weather: {e}")
                await self.send_telemetry({"alerts": ["wttr_in_error"]})
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
