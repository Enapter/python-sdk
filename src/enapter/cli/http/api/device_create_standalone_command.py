import argparse
import json

from enapter import cli, http


class DeviceCreateStandaloneCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "create-standalone", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "name", help="ID or slug of the device to get information about"
        )
        parser.add_argument(
            "-s", "--site-id", help="Site ID to create device in", default=None
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            device = await client.devices.create_standalone(
                args.name, site_id=args.site_id
            )
            print(json.dumps(device.to_dto()))
