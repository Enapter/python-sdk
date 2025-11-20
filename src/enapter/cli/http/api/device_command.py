import argparse

from enapter import cli

from .device_generate_communication_config_command import (
    DeviceGenerateCommunicationConfigCommand,
)
from .device_get_command import DeviceGetCommand


class DeviceCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "device", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(
            dest="http_api_device_command", required=True
        )
        for command in [
            DeviceGetCommand,
            DeviceGenerateCommunicationConfigCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.http_api_device_command:
            case "get":
                await DeviceGetCommand.run(args)
            case "generate-communication-config":
                await DeviceGenerateCommunicationConfigCommand.run(args)
            case _:
                raise NotImplementedError(args.device_command)
