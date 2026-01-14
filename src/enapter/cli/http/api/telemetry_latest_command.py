import argparse
import json

from enapter import cli, http


class TelemetryLatestCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "latest", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "device_attrs",
            metavar="device:attr1,attr2,...,attrN",
            nargs="+",
            help="Device attributes to get the latest telemetry for",
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            attributes_by_device = {}
            for device_attrs in args.device_attrs:
                device, attrs_str = device_attrs.split(":", 1)
                attributes_by_device[device] = attrs_str.split(",")
            telemetry = await client.telemetry.latest(attributes_by_device)
            dto = {
                device: {
                    attribute: datapoint.to_dto() if datapoint is not None else None
                    for attribute, datapoint in datapoints.items()
                }
                for device, datapoints in telemetry.items()
            }
            print(json.dumps(dto))
