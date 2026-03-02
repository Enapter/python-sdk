import argparse
import json

from enapter import cli, http

from .site_location import parse_site_location


class SiteUpdateCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "update", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", nargs="?", type=str, help="ID of the site to update")
        parser.add_argument("-n", "--name", type=str, help="New name for the site")
        parser.add_argument(
            "-t", "--timezone", type=str, help="New timezone for the site"
        )
        parser.add_argument(
            "-l",
            "--location",
            type=parse_site_location,
            help="New location for the site",
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            site = await client.sites.update(
                site_id=args.id,
                name=args.name,
                timezone=args.timezone,
                location=(
                    http.api.sites.Location(
                        name=args.location[0],
                        latitude=args.location[1],
                        longitude=args.location[2],
                    )
                    if args.location is not None
                    else None
                ),
            )
            print(json.dumps(site.to_dto()))
