import argparse

from enapter import cli

from . import api


class Command(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "http", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="http_command", required=True)
        for command in [
            api.Command,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.http_command:
            case "api":
                await api.Command.run(args)
            case _:
                raise NotImplementedError(args.http_command)
