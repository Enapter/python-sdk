import argparse

from enapter import cli

from .client_command import ClientCommand
from .server_command import ServerCommand


class Command(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "mcp", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="mcp_command", required=True)
        for command in [
            ClientCommand,
            ServerCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.mcp_command:
            case "client":
                await ClientCommand.run(args)
            case "server":
                await ServerCommand.run(args)
            case _:
                raise NotImplementedError(args.mcp_command)
