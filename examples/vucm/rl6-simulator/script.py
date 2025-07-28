import asyncio

import enapter


async def main():
    await enapter.vucm.run(Rl6Simulator)


class Rl6Simulator(enapter.vucm.Device):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loads = {
            "r1": False,
            "r2": False,
            "r3": False,
            "r4": False,
            "r5": False,
            "r6": False,
        }

    @enapter.vucm.device_command
    async def enable_load(self, load: str):
        self.loads[load] = True

    @enapter.vucm.device_command
    async def disable_load(self, load: str):
        self.loads[load] = False

    @enapter.vucm.device_task
    async def telemetry_sender(self):
        while True:
            await self.send_telemetry(self.loads)
            await asyncio.sleep(1)

    @enapter.vucm.device_task
    async def properties_sender(self):
        while True:
            await self.send_properties({})
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
