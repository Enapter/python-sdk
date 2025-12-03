import argparse

from enapter import cli

from .device_command import DeviceCommand
from .site_command import SiteCommand


class Command(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "api", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="api_command", required=True)
        for command in [
            DeviceCommand,
            SiteCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.api_command:
            case "device":
                await DeviceCommand.run(args)
            case "site":
                await SiteCommand.run(args)
            case _:
                raise NotImplementedError(args.device_command)
