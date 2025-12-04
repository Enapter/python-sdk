import argparse
import json

from enapter import cli, http


class DeviceListCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "list", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "-l",
            "--limit",
            type=int,
            help="Maximum number of devices to list",
            default=-1,
        )
        parser.add_argument(
            "-m",
            "--manifest",
            action="store_true",
            help="Expand device manifest information",
        )
        parser.add_argument(
            "-p",
            "--properties",
            action="store_true",
            help="Expand device properties information",
        )
        parser.add_argument(
            "-c",
            "--connectivity",
            action="store_true",
            help="Expand device connectivity information",
        )
        parser.add_argument(
            "--communication",
            action="store_true",
            help="Expand device communication information",
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        if args.limit == 0:
            return
        async with http.api.Client(http.api.Config.from_env()) as client:
            async with client.devices.list(
                expand_manifest=args.manifest,
                expand_properties=args.properties,
                expand_connectivity=args.connectivity,
                expand_communication=args.communication,
            ) as stream:
                count = 0
                async for device in stream:
                    print(json.dumps(device.to_dto()))
                    count += 1
                    if args.limit > 0 and count == args.limit:
                        break
