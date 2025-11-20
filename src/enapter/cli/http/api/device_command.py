import argparse

from enapter import cli

from .device_assign_blueprint_command import DeviceAssignBlueprintCommand
from .device_create_standalone_command import DeviceCreateStandaloneCommand
from .device_delete_command import DeviceDeleteCommand
from .device_generate_communication_config_command import (
    DeviceGenerateCommunicationConfigCommand,
)
from .device_get_command import DeviceGetCommand
from .device_list_command import DeviceListCommand
from .device_update_command import DeviceUpdateCommand


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
            DeviceAssignBlueprintCommand,
            DeviceCreateStandaloneCommand,
            DeviceDeleteCommand,
            DeviceGenerateCommunicationConfigCommand,
            DeviceGetCommand,
            DeviceListCommand,
            DeviceUpdateCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.http_api_device_command:
            case "assign-blueprint":
                await DeviceAssignBlueprintCommand.run(args)
            case "create-standalone":
                await DeviceCreateStandaloneCommand.run(args)
            case "delete":
                await DeviceDeleteCommand.run(args)
            case "generate-communication-config":
                await DeviceGenerateCommunicationConfigCommand.run(args)
            case "get":
                await DeviceGetCommand.run(args)
            case "list":
                await DeviceListCommand.run(args)
            case "update":
                await DeviceUpdateCommand.run(args)
            case _:
                raise NotImplementedError(args.device_command)
