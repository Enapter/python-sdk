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
            "-n", "--name", help="Name of the standalone device to create"
        )
        parser.add_argument("--slug", help="Slug of the standalone device to create")
        parser.add_argument("-s", "--site-id", help="Site ID to create device in")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            device = await client.devices.create_standalone(
                name=args.name, site_id=args.site_id, slug=args.slug
            )
            print(json.dumps(device.to_dto()))
