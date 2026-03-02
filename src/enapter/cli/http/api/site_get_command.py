import argparse
import json

from enapter import cli, http


class SiteGetCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "get", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "id", nargs="?", type=str, help="ID of the site to retrieve"
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            site = await client.sites.get(args.id)
            print(json.dumps(site.to_dto()))
