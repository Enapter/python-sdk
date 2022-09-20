"""
Run stand-alone VUCM::

    $ export ENAPTER_VUCM_BLOB=<...>
    $ python examples/vucm.py
"""

import asyncio
import random

import enapter


class Example(enapter.vucm.Device):
    async def cmd_ping(self):
        return "pong"

    async def cmd_raise_alert(self):
        self.alerts.add("high_voltage")

    async def cmd_withdraw_alert(self):
        self.alerts.remove("high_voltage")

    async def task_telemetry_publisher(self):
        while True:
            await self.send_telemetry({"voltage": random.random()})
            await asyncio.sleep(1)

    async def task_properties_publisher(self):
        while True:
            await self.send_properties(
                {"serial_number": "0x0042", "model": "Test VUCM"}
            )
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(enapter.vucm.run(Example))
