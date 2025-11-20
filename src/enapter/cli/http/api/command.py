import argparse

from enapter import cli

from .device_command import DeviceCommand


class Command(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "api", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="http_api_command", required=True)
        for command in [
            DeviceCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.http_api_command:
            case "device":
                await DeviceCommand.run(args)
            case _:
                raise NotImplementedError(args.device_command)
