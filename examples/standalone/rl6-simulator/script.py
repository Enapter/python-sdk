import asyncio

import enapter


async def main():
    await enapter.standalone.run(Rl6Simulator())


class Rl6Simulator(enapter.standalone.Device):

    def __init__(self):
        super().__init__()
        self.loads = {
            "r1": False,
            "r2": False,
            "r3": False,
            "r4": False,
            "r5": False,
            "r6": False,
        }

    async def run(self):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.properties_sender())
            tg.create_task(self.telemetry_sender())

    async def properties_sender(self):
        while True:
            await self.send_properties({})
            await asyncio.sleep(10)

    async def telemetry_sender(self):
        while True:
            await self.send_telemetry(self.loads)
            await asyncio.sleep(1)

    async def cmd_enable_load(self, load: str):
        self.loads[load] = True

    async def cmd_disable_load(self, load: str):
        self.loads[load] = False


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
