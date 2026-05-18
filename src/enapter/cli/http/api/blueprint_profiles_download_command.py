import argparse
import logging
import pathlib

from enapter import cli, http

LOGGER = logging.getLogger(__name__)


class BlueprintProfilesDownloadCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "download", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "-o",
            "--output",
            type=pathlib.Path,
            help="Output directory path",
            default=pathlib.Path.cwd(),
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            content = await client.blueprints.download_device_profiles()
            output_path = args.output / "device_profiles.zip"
            with output_path.open("wb") as f:
                f.write(content)
