import argparse
import json

from enapter import cli, http


class DeviceCreateVUCMCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "create-vucm", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("-s", "--site-id", help="Site ID to create device in")
        parser.add_argument("--hardware-id", help="Hardware ID of the VUCM device")
        parser.add_argument("name", help="Name of the VUCM device to create")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            device = await client.devices.create_vucm(
                name=args.name, site_id=args.site_id, hardware_id=args.hardware_id
            )
            print(json.dumps(device.to_dto()))
