import asyncio
import functools
import os

import miio

import enapter


async def main():
    device_factory = functools.partial(
        ZhimiFanZA5,
        ip=os.environ["MIIO_IP"],
        token=os.environ["MIIO_TOKEN"],
    )
    await enapter.vucm.run(device_factory)


class ZhimiFanZA5(enapter.vucm.Device):
    def __init__(self, ip, token, **kwargs):
        super().__init__(**kwargs)
        self.fan = miio.FanZA5(ip=ip, token=token)

    async def cmd_power(self, on: bool = False):
        return await self.run_in_thread(self.fan.on if on else self.fan.off)

    async def cmd_mode(self, mode: str):
        miio_mode = miio.fan_common.OperationMode(mode)
        return await self.run_in_thread(self.fan.set_mode, miio_mode)

    async def cmd_buzzer(self, on: bool = False):
        return await self.run_in_thread(self.fan.set_buzzer, on)

    async def cmd_speed(self, speed: int):
        return await self.run_in_thread(self.fan.set_speed, speed)

    async def task_telemetry_sender(self):
        while True:
            status = await self.run_in_thread(self.fan.status)
            await self.send_telemetry(
                {
                    "humidity": status.humidity,
                    "temperature": status.temperature,
                    "on": status.is_on,
                    "mode": status.mode.value,
                    "buzzer": status.buzzer,
                    "speed": status.speed,
                }
            )
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
