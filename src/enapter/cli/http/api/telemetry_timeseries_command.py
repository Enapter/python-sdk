import argparse
import datetime
import json

from enapter import cli, http


class TelemetryTimeseriesCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "timeseries", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "-f",
            "--time-from",
            required=True,
            help="Start time for the telemetry data (ISO 8601 format)",
        )
        parser.add_argument(
            "-t", "--time-to", help="End time for the telemetry data (ISO 8601 format)"
        )
        parser.add_argument(
            "-s",
            "--shape",
            choices=["w", "wide", "l", "long"],
            default="long",
            help="Shape of the output data",
        )
        parser.add_argument(
            "-g",
            "--granularity",
            type=int,
            default=60 * 60,
            help="Granularity of the telemetry data in seconds",
        )
        parser.add_argument(
            "selectors",
            metavar="device:attr1,attr2,...,attrN",
            nargs="+",
            help="Device ID or slug followed by a colon and a comma-separated list of attribute names to fetch the telemetry for",
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        attributes_by_device = {}
        for selector in args.selectors:
            device, attributes = selector.split(":", 1)
            attributes_by_device[device] = attributes.split(",")
        async with http.api.Client(http.api.Config.from_env()) as client:
            time_to = (
                datetime.datetime.fromisoformat(args.time_to)
                if args.time_to is not None
                else datetime.datetime.now(datetime.timezone.utc)
            )
            time_from = (
                datetime.datetime.fromisoformat(args.time_from)
                if args.time_from is not None
                else time_to - datetime.timedelta(minutes=10)
            )
            match args.shape:
                case "l" | "long":
                    await TelemetryTimeseriesCommand._handle_long_timeseries(
                        args, client, time_from, time_to, attributes_by_device
                    )
                case "w" | "wide":
                    await TelemetryTimeseriesCommand._handle_wide_timeseries(
                        args, client, time_from, time_to, attributes_by_device
                    )
                case _:
                    raise NotImplementedError(args.shape)

    @staticmethod
    async def _handle_long_timeseries(
        args: argparse.Namespace,
        client: http.api.Client,
        time_from: datetime.datetime,
        time_to: datetime.datetime,
        attributes_by_device: dict[str, list[str]],
    ) -> None:
        async with client.telemetry.long_timeseries(
            from_=time_from,
            to=time_to,
            granularity=args.granularity,
            selectors=[
                http.api.telemetry.Selector(device=device, attributes=attributes)
                for device, attributes in attributes_by_device.items()
            ],
        ) as stream:
            async for row in stream:
                print(json.dumps(row.to_dto()))

    @staticmethod
    async def _handle_wide_timeseries(
        args: argparse.Namespace,
        client: http.api.Client,
        time_from: datetime.datetime,
        time_to: datetime.datetime,
        attributes_by_device: dict[str, list[str]],
    ) -> None:
        wide_timeseries = await client.telemetry.wide_timeseries(
            from_=time_from,
            to=time_to,
            granularity=args.granularity,
            selectors=[
                http.api.telemetry.Selector(device=device, attributes=attributes)
                for device, attributes in attributes_by_device.items()
            ],
        )
        print(json.dumps(wide_timeseries.to_dto()))
