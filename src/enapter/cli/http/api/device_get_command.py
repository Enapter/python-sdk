import argparse
import json

from enapter import cli, http


class DeviceGetCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "get", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "id", type=str, help="ID or slug of the device to get information about"
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            device = await client.devices.get(args.id)
            print(json.dumps(device.to_dto()))
