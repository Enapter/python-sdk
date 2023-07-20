import asyncio
import os

import enapter

SNMP_HOST = os.environ["ENAPTER_SNMP_HOST"]
SNMP_PORT = os.environ["ENAPTER_SNMP_PORT"]
SNMP_COMMUNITY = os.environ["ENAPTER_SNMP_COMMUNITY"]


def snmpget(oid):
    from pysnmp.entity.rfc3413.oneliner import cmdgen

    global SNMP_HOST
    global SNMP_PORT
    global SNMP_COMMUNITY

    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(SNMP_COMMUNITY),
        cmdgen.UdpTransportTarget((SNMP_HOST, SNMP_PORT)),
        oid,
    )

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print(
                "%s at %s"
                % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1] or "?",
                )
            )
        else:
            for name, val in varBinds:
                # print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                return val


async def main():
    await enapter.vucm.run(EatonUPS)


class EatonUPS(enapter.vucm.Device):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.telemetry = {}
        self.properties = {}

    async def task_get_telemetry_data(self):
        while True:
            if (value := snmpget("1.3.6.1.4.1.534.1.6.1.0")) is not None:
                self.telemetry["temperature"] = int(value)

            if (value := snmpget("1.3.6.1.4.1.534.1.2.4.0")) is not None:
                self.telemetry["capacity"] = int(value)

            if (value := snmpget("1.3.6.1.4.1.534.1.2.5.0")) is not None:
                self.telemetry["status"] = str(value)

            if (value := snmpget("1.3.6.1.2.1.33.1.3.3.1.2.1")) is not None:
                self.telemetry["grid_freq"] = int(value) * 0.1

            if (value := snmpget("1.3.6.1.4.1.534.1.4.2.0")) is not None:
                self.telemetry["ups_freq"] = int(value) * 0.1

            if (value := snmpget("1.3.6.1.4.1.534.1.3.4.1.2.1")) is not None:
                self.telemetry["grid_v"] = int(value)

            if (value := snmpget("1.3.6.1.4.1.534.1.4.1.0")) is not None:
                self.telemetry["out_load"] = int(value)

            if (value := snmpget("1.3.6.1.4.1.534.1.4.4.1.4.1")) is not None:
                self.telemetry["ac_out_active_power"] = int(value)

            await asyncio.sleep(10)

    async def task_get_properties_data(self):
        while True:
            if (value := snmpget("1.3.6.1.2.1.33.1.1.2.0")) is not None:
                self.properties["model"] = str(value)
            if (value := snmpget("1.3.6.1.2.1.33.1.1.1.0")) is not None:
                self.properties["manufacturer"] = str(value)
            if (value := snmpget("1.3.6.1.2.1.33.1.1.3.0")) is not None:
                self.properties["fw_ver"] = str(value)
            if (value := snmpget("1.3.6.1.2.1.33.1.1.4.0")) is not None:
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


if __name__ == "__main__":
    asyncio.run(main())
