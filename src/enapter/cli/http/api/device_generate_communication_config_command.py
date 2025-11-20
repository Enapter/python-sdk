import argparse
import json

from enapter import cli, http


class DeviceGenerateCommunicationConfigCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "generate-communication-config",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument(
            "id", type=str, help="ID or slug of the device to get information about"
        )
        parser.add_argument(
            "-p",
            "--protocol",
            help="Communication protocol",
            choices=["mqtt", "mqtts"],
            default="mqtts",
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            config = await client.devices.generate_communication_config(
                args.id,
                mqtt_protocol=http.api.devices.MQTTProtocol(args.protocol.upper()),
            )
            print(json.dumps(config.to_dto()))
