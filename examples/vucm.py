import asyncio
import random

import enapter


class Test(enapter.vucm.Device):
    async def cmd_ping(self):
        return "pong"

    async def cmd_raise_alert(self):
        self._alert = True

    async def cmd_withdraw_alert(self):
        self._alert = False

    async def _create_tasks(self):
        self._alert = False
        return {
            self._telemetry_publisher(),
            self._properties_publisher(),
        }

    async def _telemetry_publisher(self):
        while True:
            await self._channel.publish_telemetry(
                {
                    "voltage": random.random(),
                    "alerts": ["high_voltage"] if self._alert else [],
                }
            )
            await asyncio.sleep(1)

    async def _properties_publisher(self):
        while True:
            await self._channel.publish_properties(
                {
                    "serial_number": "0x0042",
                    "model": "Test VUCM",
                }
            )
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(enapter.vucm.run(Test))
