import argparse
import logging
import pathlib

from enapter import cli, http

LOGGER = logging.getLogger(__name__)


class BlueprintValidateCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "validate", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "path", type=pathlib.Path, help="Path to a directory or a zip file"
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            if args.path.is_dir():
                await client.blueprints.validate_directory(args.path)
            else:
                await client.blueprints.validate_file(args.path)
