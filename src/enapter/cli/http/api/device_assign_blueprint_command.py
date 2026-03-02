import argparse
import json

from enapter import cli, http


class DeviceAssignBlueprintCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "assign-blueprint", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", type=str, help="ID or slug of the device to update")
        parser.add_argument(
            "-b",
            "--blueprint-id",
            help="Blueprint ID to assign to the device",
            required=True,
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            device = await client.devices.assign_blueprint(
                device_id=args.id, blueprint_id=args.blueprint_id
            )
            print(json.dumps(device.to_dto()))
