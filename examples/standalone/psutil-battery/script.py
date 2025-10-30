import asyncio

import psutil

import enapter


async def main():
    await enapter.standalone.run(PSUtilBattery())


class PSUtilBattery(enapter.standalone.Device):

    async def run(self):
        while True:
            properties, telemetry = await self.gather_data()
            await self.send_properties(properties)
            await self.send_telemetry(telemetry)
            await asyncio.sleep(10)

    async def gather_data(self):
        try:
            battery = await asyncio.to_thread(psutil.sensors_battery)
        except Exception as e:
            await self.logger.error(f"failed to gather data: {e}")
            return {}, {"alerts": ["gather_data_error"]}

        if battery is None:
            return {"battery_installed": False}, {}

        return {"battery_installed": True}, {
            "charge_percent": battery.percent,
            "power_plugged": battery.power_plugged,
            "time_until_full_discharge": (
                battery.secsleft if not battery.power_plugged else None
            ),
        }


if __name__ == "__main__":
    asyncio.run(main())
