import asyncio
import os

import miio

import enapter


async def main():
    await enapter.standalone.run(
        Fan1C(ip=os.environ["MIIO_IP"], token=os.environ["MIIO_TOKEN"])
    )


class Fan1C(enapter.standalone.Device):

    def __init__(self, ip, token):
        super().__init__()
        self.fan = miio.Fan1C(ip=ip, token=token)

    async def run(self):
        while True:
            status = await asyncio.to_thread(self.fan.status)
            await self.send_telemetry(
                {
                    "on": status.is_on,
                    "mode": status.mode.value,
                    "buzzer": status.buzzer,
                    "speed": status.speed,
                },
            )
            await asyncio.sleep(1)

    async def cmd_power(self, on: bool = False):
        return await asyncio.to_thread(self.fan.on if on else self.fan.off)

    async def cmd_mode(self, mode: str):
        miio_mode = miio.fan_common.OperationMode(mode)
        return await asyncio.to_thread(self.fan.set_mode, miio_mode)

    async def cmd_buzzer(self, on: bool = False):
        return await asyncio.to_thread(self.fan.set_buzzer, on)

    async def cmd_speed(self, speed: int):
        return await asyncio.to_thread(self.fan.set_speed, speed)


if __name__ == "__main__":
    asyncio.run(main())
