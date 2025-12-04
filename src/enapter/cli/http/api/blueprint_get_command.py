import argparse
import json
import logging

from enapter import cli, http

LOGGER = logging.getLogger(__name__)


class BlueprintGetCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "get", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", help="ID of the blueprint to get")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            blueprint = await client.blueprints.get(blueprint_id=args.id)
            print(json.dumps(blueprint.to_dto()))
