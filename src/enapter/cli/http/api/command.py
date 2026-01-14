import argparse

from enapter import cli

from .blueprint_command import BlueprintCommand
from .command_command import CommandCommand
from .device_command import DeviceCommand
from .site_command import SiteCommand
from .telemetry_command import TelemetryCommand


class Command(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "api", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="api_command", required=True)
        for command in [
            BlueprintCommand,
            CommandCommand,
            DeviceCommand,
            SiteCommand,
            TelemetryCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.api_command:
            case "blueprint":
                await BlueprintCommand.run(args)
            case "command":
                await CommandCommand.run(args)
            case "device":
                await DeviceCommand.run(args)
            case "site":
                await SiteCommand.run(args)
            case "telemetry":
                await TelemetryCommand.run(args)
            case _:
                raise NotImplementedError(args.device_command)
