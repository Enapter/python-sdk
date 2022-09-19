"""
Run stand-alone VUCM::

    $ export ENAPTER_VUCM_BLOB=<...>
    $ python examples/vucm.py
"""

import asyncio
import functools
import random

import enapter


def every(interval):
    def decorator(f):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            while True:
                await f(*args, **kwargs)
                await asyncio.sleep(interval)

        return wrapper

    return decorator


class Example(enapter.vucm.Device):
    async def cmd_ping(self):
        return "pong"

    async def cmd_raise_alert(self):
        self.alerts.add("high_voltage")

    async def cmd_withdraw_alert(self):
        self.alerts.remove("high_voltage")

    async def _create_tasks(self):
        return {
            self.telemetry_publisher(),
            self.properties_publisher(),
        }

    async def telemetry_publisher(self):
        while True:
            await self.send_telemetry({"voltage": random.random()})
            await asyncio.sleep(1)

    async def properties_publisher(self):
        while True:
            await self.send_properties(
                {"serial_number": "0x0042", "model": "Test VUCM"}
            )
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(enapter.vucm.run(Example))
