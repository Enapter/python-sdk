import asyncio
import contextlib
import functools
import os

import aiohttp
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


class WttrInFactory:
    def __init__(self, location=None):
        self.stack = contextlib.AsyncExitStack()
        if location is None:
            location = os.environ["WTTR_IN_LOCATION"]
        self.location = location

    async def __aenter__(self):
        self.client = await self.stack.enter_async_context(python_weather.Client())
        return self

    async def __aexit__(self, *exc):
        await self.stack.aclose()

    def __call__(self, **kwargs):
        return WttrIn(client=self.client, location=self.location, **kwargs)


class WttrIn(enapter.vucm.Device):
    def __init__(self, client, location, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self.location = location

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
            except aiohttp.ClientError as e:
                self.alerts.add("http_error")
                await self.log.error(f"failed to get weather: {e}")
            finally:
                await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
