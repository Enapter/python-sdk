import argparse
import json

from enapter import cli, http


class SiteListCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "list", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "-l",
            "--limit",
            type=int,
            help="Maximum number of sites to list",
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            async with client.sites.list(limit=args.limit) as stream:
                async for site in stream:
                    print(json.dumps(site.to_dto()))
