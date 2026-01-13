import argparse

from enapter import cli, mcp


class ClientPingCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        _ = parent.add_parser(
            "ping", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with mcp.Client(url=args.url) as client:
            await client.ping()
