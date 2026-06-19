import asyncio
import csv
import functools
import glob
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import enapter


async def main():
    csv_files = sorted(glob.glob("files/*.csv"))
    print("files", csv_files)
    device_factory = functools.partial(
        CSVBackup, csv_files=csv_files, timezone=os.getenv("TIMEZONE", "Europe/Berlin"),)
    await enapter.vucm.run(device_factory)


class CSVBackup(enapter.vucm.Device):
    def __init__(self, csv_files, timezone, **kwargs):
        super().__init__(**kwargs)
        self.csv_files = csv_files
        self.timezone = timezone

    async def task_send_csv_telemetry(self):
        """
        Read CSV file line by line, send each row as telemetry every second.
        """
        read_csv_files = 0
        while True:
            if read_csv_files == len(self.csv_files):
                break
            for f in self.csv_files:
                await self.log.info(f"reading file: {f}")
                try:
                    with open(f, newline="") as csv_file:
                        reader = csv.DictReader(csv_file)
                        headers = reader.fieldnames or []
                        for row in reader:
                            telemetry = {}
                            telemetry["status"] = "ok"
                            for key in headers:
                                value = row.get(key)
                                if key in ("Date", "Time"):
                                    telemetry[key] = value
                                else:
                                    telemetry[key] = float(value) if value != "" else None
                                await self.log.info(f"read {key}: {telemetry[key]}")
                            self._add_timestamp_if_present(telemetry)
                            await self.send_telemetry(telemetry)
                            await asyncio.sleep(1)
                except Exception as e:
                    await self.log.error(f"Failed to read CSV: {e}")
                    await asyncio.sleep(5)
                finally:
                    read_csv_files += 1
                    await self.log.info(f"finished reading file: {f}")
            break
        await self.log.info(f"all read")

    def _add_timestamp_if_present(self, telemetry):
        """If 'Date' and 'Time' are present, combine and convert to timestamp."""
        date_str = telemetry.get("Date")
        time_str = telemetry.get("Time")
        if date_str and time_str:
            dt_str = f"{date_str} {time_str}"
            naive_dt = datetime.strptime(dt_str, "%d/%m/%Y %H:%M:%S")
            tz_aware_dt = naive_dt.replace(tzinfo=ZoneInfo(self.timezone))
            telemetry["timestamp"] = int(tz_aware_dt.timestamp())
            telemetry.pop("Date")
            telemetry.pop("Time") 


if __name__ == "__main__":
    asyncio.run(main())
