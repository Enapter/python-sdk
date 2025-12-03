import argparse
import logging
import pathlib

from enapter import cli, http

LOGGER = logging.getLogger(__name__)


class BlueprintDownloadCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "download", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", help="ID of the blueprint to download")
        parser.add_argument(
            "-o", "--output", type=pathlib.Path, help="Output file path", required=True
        )
        parser.add_argument(
            "-v",
            "--view",
            choices=["original", "compiled"],
            default="original",
            help="Blueprint view type",
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            content = await client.blueprints.download(
                args.id, view=http.api.blueprints.BlueprintView(args.view.upper())
            )
            with open(args.output, "wb") as f:
                f.write(content)
