import asyncio
import csv
import functools
import glob
from datetime import datetime

import enapter


def parse_timestamp(date_str, time_str):
    """
    Combine date and time strings into a UNIX timestamp (int), or return None if parsing fails.
    """
    if date_str and time_str:
        try:
            dt_str = f"{date_str} {time_str}"
            date = datetime.strptime(dt_str, "%d/%m/%Y %H:%M:%S")
            return int(date.timestamp())
        except Exception as e:
            print(f"Failed to parse timestamp: {e}")
            return None
    return None


async def main():
    csv_files = sorted(glob.glob("*.csv"))
    device_factory = functools.partial(CSVBackup, csv_files=csv_files)
    await enapter.vucm.run(device_factory)


class CSVBackup(enapter.vucm.Device):
    def __init__(self, csv_files, **kwargs):
        super().__init__(**kwargs)
        self.csv_files = csv_files

    async def task_send_csv_telemetry(self):
        """
        Read CSV file line by line, send each row as telemetry every second.
        """
        while True:
            for f in self.csv_files:
                try:
                    with open(f, newline="") as csv_file:
                        reader = csv.DictReader(csv_file)
                        headers = reader.fieldnames or []
                        for row in reader:
                            telemetry = {}
                            telemetry["status"] = "ok"
                            for key in headers:
                                if key in ("Date", "Time"):
                                    continue
                                value = row.get(key)
                                telemetry[key] = value if value != "" else None
                                await self.log.info(f" {key}: {telemetry[key]}")
                            telemetry["timestamp"] = parse_timestamp(
                                row.get("Date"), row.get("Time")
                            )
                            await self.send_telemetry(telemetry)
                            await asyncio.sleep(1)
                except Exception as e:
                    await self.log.error(f"Failed to read CSV: {e}")
                    await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
