import argparse
import json

from enapter import cli, http


class DeviceUpdateCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "update", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", type=str, help="ID or slug of the device to update")
        parser.add_argument(
            "-s", "--slug", help="New slug for the device", default=None
        )
        parser.add_argument(
            "-n", "--name", help="New name for the device", default=None
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            device = await client.devices.update(
                args.id, name=args.name, slug=args.slug
            )
            print(json.dumps(device.to_dto()))
