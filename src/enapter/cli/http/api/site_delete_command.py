import argparse

from enapter import cli, http


class SiteDeleteCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "delete", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", type=str, help="ID of the site to delete")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            await client.sites.delete(args.id)
