import argparse
import json

from enapter import cli, http

from .site_location import parse_site_location


class SiteCreateCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "create", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("name", help="Name of the site to create")
        parser.add_argument(
            "-t", "--timezone", help="Timezone of the site to create", default="UTC"
        )
        parser.add_argument(
            "-l",
            "--location",
            type=parse_site_location,
            help="Site location in the format NAME,LATITUDE,LONGITUDE",
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            site = await client.sites.create(
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
