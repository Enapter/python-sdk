import asyncio
import functools
import json
import os
import socket
from datetime import datetime

import enapter


async def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        sock.bind(("127.0.0.1", int(os.environ["LISTEN_TCP_PORT"])))
        sock.listen()
        sock.setblocking(False)
        device_factory = functools.partial(NIDAQ, socket=sock)
        await enapter.vucm.run(device_factory)


class NIDAQ(enapter.vucm.Device):
    def __init__(self, socket, **kwargs):
        super().__init__(**kwargs)
        self.socket = socket

    async def task_accept_conns(self):
        sock = self.socket
        while True:
            (conn, addr) = await asyncio.get_event_loop().sock_accept(sock)
            asyncio.create_task(self.handle_conn(conn, addr))

    async def handle_conn(self, conn, addr):
        print(addr, "accept")
        data = bytearray()
        try:
            while True:
                try:
                    async with asyncio.timeout(5):
                        chunk = await asyncio.get_event_loop().sock_recv(conn, 1024)
                except TimeoutError:
                    print(addr, "timeout")
                    return
                if chunk:
                    print(addr, "read chunk: ", chunk)
                    data.extend(chunk)
                    continue
                print(addr, "read data: ", data)
                await self._process_and_send_telemetry(data)
                return
        finally:
            print(addr, "close")
            conn.close()

    async def task_properties_sender(self):
        """Periodically send device properties."""
        while True:
            await self.send_properties(
                {"vendor": "National Instruments", "model": "cDAQ 9178"}
            )
            await asyncio.sleep(10)

    async def _process_and_send_telemetry(self, data):
        """Parse, enrich, and send telemetry data."""
        telemetry = {}
        status = "no_data"
        try:
            if data:
                status = "ok"
                telemetry = json.loads(data.decode())
                self._add_timestamp_if_present(telemetry)
            telemetry["status"] = status
            await self.send_telemetry(telemetry)
            self.alerts.clear()
        except Exception as e:
            self.alerts.add("parse_error")
            await self.log.error(f"Failed to process data: {e}")

    def _add_timestamp_if_present(self, telemetry):
        """If 'Date' and 'Time' are present, combine and convert to timestamp."""
        date_str = telemetry.get("Date")
        time_str = telemetry.get("Time")
        if date_str and time_str:
            dt_str = f"{date_str} {time_str}"
            date = datetime.strptime(dt_str, "%d/%m/%Y %H:%M:%S")
            telemetry.pop("Date")
            telemetry.pop("Time")
            telemetry["timestamp"] = int(date.timestamp())


if __name__ == "__main__":
    asyncio.run(main())
