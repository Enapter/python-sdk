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
            telemetry = await client.telemetry.latest(attributes_by_device)
            dto = {
                device: {
                    attribute: datapoint.to_dto() if datapoint is not None else None
                    for attribute, datapoint in datapoints.items()
                }
                for device, datapoints in telemetry.items()
            }
            print(json.dumps(dto))
