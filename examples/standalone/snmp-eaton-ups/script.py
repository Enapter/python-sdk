import asyncio
import os

from pysnmp.entity.rfc3413.oneliner import cmdgen

import enapter


async def main():
    eaton_ups = EatonUPS(
        snmp_community=os.environ["ENAPTER_SNMP_COMMUNITY"],
        snmp_host=os.environ["ENAPTER_SNMP_HOST"],
        snmp_port=os.environ["ENAPTER_SNMP_PORT"],
    )
    await enapter.standalone.run(eaton_ups)


class EatonUPS(enapter.standalone.Device):

    def __init__(self, snmp_community, snmp_host, snmp_port):
        super().__init__()
        self.telemetry = {}
        self.properties = {}
        self.cmd_gen = cmdgen.CommandGenerator()
        self.auth_data = cmdgen.CommunityData(snmp_community)
        self.transport_target = cmdgen.UdpTransportTarget((snmp_host, snmp_port))

    async def run(self):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.get_telemetry_data())
            tg.create_task(self.telemetry_sender())
            tg.create_task(self.properties_sender())

    async def get_telemetry_data(self):
        while True:
            temperature = await self.snmp_get("1.3.6.1.4.1.534.1.6.1.0")
            if temperature is not None:
                self.telemetry["temperature"] = int(temperature)

            capacity = await self.snmp_get("1.3.6.1.4.1.534.1.2.4.0")
            if capacity is not None:
                self.telemetry["capacity"] = int(capacity)

            status = await self.snmp_get("1.3.6.1.4.1.534.1.2.5.0")
            if status is not None:
                if status == 1:
                    status_name = "charge"
                elif status == 2:
                    status_name = "discharge"
                elif status == 3:
                    status_name = "float"
                elif status == 4:
                    status_name = "reset"
                elif status == 5:
                    status_name = "unknown"
                elif status == 6:
                    status_name = "disconnect"
                elif status == 7:
                    status_name = "test"
                elif status == 8:
                    status_name = "check"
                else:
                    raise ValueError(f"unexpected status: {status}")

                self.telemetry["status"] = status_name

            grid_freq = await self.snmp_get("1.3.6.1.2.1.33.1.3.3.1.2.1")
            if grid_freq is not None:
                self.telemetry["grid_freq"] = int(grid_freq) * 0.1

            ups_freq = await self.snmp_get("1.3.6.1.4.1.534.1.4.2.0")
            if ups_freq is not None:
                self.telemetry["ups_freq"] = int(ups_freq) * 0.1

            grid_v = await self.snmp_get("1.3.6.1.4.1.534.1.3.4.1.2.1")
            if grid_v is not None:
                self.telemetry["grid_v"] = int(grid_v)

            out_load = await self.snmp_get("1.3.6.1.4.1.534.1.4.1.0")
            if out_load is not None:
                self.telemetry["out_load"] = int(out_load)

            ac_out_active_power = await self.snmp_get("1.3.6.1.4.1.534.1.4.4.1.4.1")
            if ac_out_active_power is not None:
                self.telemetry["ac_out_active_power"] = int(ac_out_active_power)

            await asyncio.sleep(10)

    @enapter.vucm.device_task
    async def get_properties_data(self):
        while True:
            model = await self.snmp_get("1.3.6.1.2.1.33.1.1.2.0")
            if model is not None:
                self.properties["model"] = str(model)

            manufacturer = await self.snmp_get("1.3.6.1.2.1.33.1.1.1.0")
            if manufacturer is not None:
                self.properties["manufacturer"] = str(manufacturer)

            fw_ver = await self.snmp_get("1.3.6.1.2.1.33.1.1.3.0")
            if fw_ver is not None:
                self.properties["fw_ver"] = str(fw_ver)

            agent_ver = await self.snmp_get("1.3.6.1.2.1.33.1.1.4.0")
            if agent_ver is not None:
                self.properties["agent_ver"] = str(agent_ver)

            await asyncio.sleep(60)

    async def telemetry_sender(self):
        while True:
            await self.send_telemetry(self.telemetry)
            await asyncio.sleep(1)

    async def properties_sender(self):
        while True:
            await self.send_properties(self.properties)
            await asyncio.sleep(10)

    async def snmp_get(self, oid):
        result = await asyncio.to_thread(
            self.cmd_gen.getCmd,
            self.auth_data,
            self.transport_target,
            oid,
        )
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
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
