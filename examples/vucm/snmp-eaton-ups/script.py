import asyncio
import functools
import os

from pysnmp.entity.rfc3413.oneliner import cmdgen

import enapter


async def main():
    device_factory = functools.partial(
        EatonUPS,
        snmp_community=os.environ["ENAPTER_SNMP_COMMUNITY"],
        snmp_host=os.environ["ENAPTER_SNMP_HOST"],
        snmp_port=os.environ["ENAPTER_SNMP_PORT"],
    )
    await enapter.vucm.run(device_factory)


class EatonUPS(enapter.vucm.Device):
    def __init__(self, snmp_community, snmp_host, snmp_port, **kwargs):
        super().__init__(**kwargs)

        self.telemetry = {}
        self.properties = {}

        self.cmd_gen = cmdgen.CommandGenerator()
        self.auth_data = cmdgen.CommunityData(snmp_community)
        self.transport_target = cmdgen.UdpTransportTarget((snmp_host, snmp_port))

    async def task_get_telemetry_data(self):
        while True:
            if (value := self.snmp_get("1.3.6.1.4.1.534.1.6.1.0")) is not None:
                self.telemetry["temperature"] = int(value)

            if (value := self.snmp_get("1.3.6.1.4.1.534.1.2.4.0")) is not None:
                self.telemetry["capacity"] = int(value)

            if (value := self.snmp_get("1.3.6.1.4.1.534.1.2.5.0")) is not None:
                self.telemetry["status"] = str(value)

            if (value := self.snmp_get("1.3.6.1.2.1.33.1.3.3.1.2.1")) is not None:
                self.telemetry["grid_freq"] = int(value) * 0.1

            if (value := self.snmp_get("1.3.6.1.4.1.534.1.4.2.0")) is not None:
                self.telemetry["ups_freq"] = int(value) * 0.1

            if (value := self.snmp_get("1.3.6.1.4.1.534.1.3.4.1.2.1")) is not None:
                self.telemetry["grid_v"] = int(value)

            if (value := self.snmp_get("1.3.6.1.4.1.534.1.4.1.0")) is not None:
                self.telemetry["out_load"] = int(value)

            if (value := self.snmp_get("1.3.6.1.4.1.534.1.4.4.1.4.1")) is not None:
                self.telemetry["ac_out_active_power"] = int(value)

            await asyncio.sleep(10)

    async def task_get_properties_data(self):
        while True:
            if (value := self.snmp_get("1.3.6.1.2.1.33.1.1.2.0")) is not None:
                self.properties["model"] = str(value)
            if (value := self.snmp_get("1.3.6.1.2.1.33.1.1.1.0")) is not None:
                self.properties["manufacturer"] = str(value)
            if (value := self.snmp_get("1.3.6.1.2.1.33.1.1.3.0")) is not None:
                self.properties["fw_ver"] = str(value)
            if (value := self.snmp_get("1.3.6.1.2.1.33.1.1.4.0")) is not None:
                self.properties["agent_ver"] = str(value)
            await asyncio.sleep(60)

    async def task_telemetry_sender(self):
        while True:
            await self.send_telemetry(self.telemetry)
            await asyncio.sleep(1)

    async def task_properties_publisher(self):
        while True:
            await self.send_properties(self.properties)
            await asyncio.sleep(10)

    def snmp_get(self, oid):
        result = self.cmd_gen.getCmd(self.auth_data, self.transport_target, oid)
        (error_indication, error_status, error_index, var_binds) = result

        if error_indication:
            await self.log.error(f"error indication: {error_indication}")
            return None

        if error_status:
            status = error_status.prettyPrint()
            index = error_index and var_binds[int(error_index) - 1] or "?"
            await self.log.error(f"error status: {status} at {index}")
            return None

        first_val = None

        for name, val in var_binds:
            await self.log.debug(f"{name.prettyPrint()} = {val.prettyPrint()}")
            if first_val is None:
                first_val = val

        return first_val


if __name__ == "__main__":
    asyncio.run(main())
