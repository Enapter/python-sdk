import argparse

from enapter import __version__, cli


class VersionCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parent.add_parser("version", help="Show version")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        print(__version__)
