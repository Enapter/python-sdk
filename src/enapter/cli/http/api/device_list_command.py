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

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        if args.limit == 0:
            return
        async with http.api.Client(http.api.Config.from_env()) as client:
            async with client.devices.list() as stream:
                count = 0
                async for device in stream:
                    print(json.dumps(device.to_dto()))
                    count += 1
                    if args.limit > 0 and count == args.limit:
                        break
