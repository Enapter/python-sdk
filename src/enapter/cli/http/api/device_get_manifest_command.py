import argparse
import json

from enapter import cli, http


class DeviceGetManifestCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "get-manifest", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", help="ID or slug of the device")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            manifest = await client.devices.get_manifest(args.id)
            print(json.dumps(manifest))
