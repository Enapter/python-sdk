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
        return await self.exec(self.fan.on if on else self.fan.off)

    async def cmd_mode(self, mode: str):
        if mode == "normal":
            miio_mode = miio.fan_common.OperationMode.Normal
        elif mode == "nature":
            miio_mode = miio.fan_common.OperationMode.Nature
        else:
            raise ValueError(f"unexpected mode: {mode}")

        return await self.exec(self.fan.set_mode, miio_mode)

    async def cmd_buzzer(self, on: bool = False):
        return await self.exec(self.fan.set_buzzer, on)

    async def cmd_speed(self, speed: int):
        return await self.exec(self.fan.set_speed, speed)

    async def task_telemetry_sender(self):
        while True:
            status = await self.exec(self.fan.status)
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

    async def exec(self, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, functools.partial(func, *args, **kwargs)
        )


if __name__ == "__main__":
    asyncio.run(main())
