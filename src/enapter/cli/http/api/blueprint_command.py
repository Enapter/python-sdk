import argparse

from enapter import cli

from .blueprint_download_command import BlueprintDownloadCommand
from .blueprint_upload_command import BlueprintUploadCommand


class BlueprintCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "blueprint", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="blueprint_command", required=True)
        for command in [
            BlueprintDownloadCommand,
            BlueprintUploadCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.blueprint_command:
            case "download":
                await BlueprintDownloadCommand.run(args)
            case "upload":
                await BlueprintUploadCommand.run(args)
            case _:
                raise NotImplementedError(args.command_command)
