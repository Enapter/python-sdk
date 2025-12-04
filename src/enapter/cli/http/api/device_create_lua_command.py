import argparse
import json

from enapter import cli, http


class DeviceCreateLuaCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "create-lua", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("-r", "--runtime-id", help="Runtime ID of the Lua device")
        parser.add_argument(
            "-b", "--blueprint-id", help="Blueprint ID of the Lua device"
        )
        parser.add_argument("-s", "--slug", help="Slug of the Lua device")
        parser.add_argument("name", help="Name of the Lua device to create")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            device = await client.devices.create_lua(
                name=args.name,
                runtime_id=args.runtime_id,
                blueprint_id=args.blueprint_id,
                slug=args.slug,
            )
            print(json.dumps(device.to_dto()))
