import asyncio
import functools
import os

import python_weather

import enapter


async def main():
    async with python_weather.Client() as client:
        device_factory = functools.partial(
            WttrIn,
            client=client,
            location=os.environ["WTTR_IN_LOCATION"],
        )
        await enapter.vucm.run(device_factory)


class WttrIn(enapter.vucm.Device):
    def __init__(self, client, location, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self.location = location

    async def task_properties_sender(self):
        while True:
            await self.send_properties(
                {
                    "location": self.location,
                }
            )
            await asyncio.sleep(10)

    async def task_telemetry_sender(self):
        while True:
            try:
                weather = await self.client.get(self.location)
                await self.send_telemetry(
                    {
                        "temperature": weather.current.temperature,
                    }
                )
                self.alerts.clear()
            except Exception as e:
                self.alerts.add("wttr_in_error")
                await self.log.error(f"failed to get weather: {e}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
