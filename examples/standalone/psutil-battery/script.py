import asyncio
from typing import Any, Dict, Tuple

import psutil

import enapter


async def main():
    await enapter.vucm.run(PSUtilBattery)


class PSUtilBattery(enapter.vucm.Device):
    @enapter.vucm.device_task
    async def data_sender(self):
        while True:
            telemetry, properties, delay = await self.gather_data()
            await self.send_telemetry(telemetry)
            await self.send_properties(properties)
            await asyncio.sleep(delay)

    async def gather_data(self) -> Tuple[Dict[str, Any], Dict[str, Any], int]:
        try:
            battery = psutil.sensors_battery()
        except Exception as e:
            await self.log.error(f"failed to gather data: {e}")
            self.alerts.add("gather_data_error")
            return {}, {}, 10
        self.alerts.clear()

        telemetry: Dict[str, Any] = {}
        properties: Dict[str, Any] = {"battery_installed": battery is not None}

        if battery is not None:
            telemetry = {
                "charge_percent": battery.percent,
                "power_plugged": battery.power_plugged,
            }
            if not battery.power_plugged:
                telemetry["time_until_full_discharge"] = battery.secsleft

        return telemetry, properties, 5


if __name__ == "__main__":
    asyncio.run(main())
