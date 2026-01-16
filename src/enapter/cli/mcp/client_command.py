import argparse

from enapter import cli

from .client_ping_command import ClientPingCommand


class ClientCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "client", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "-u", "--url", default="http://127.0.0.1:8000/mcp", help="MCP server URL"
        )
        subparsers = parser.add_subparsers(dest="client_command", required=True)
        for command in [
            ClientPingCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.client_command:
            case "ping":
                await ClientPingCommand.run(args)
            case _:
                raise NotImplementedError(args.client_command)
