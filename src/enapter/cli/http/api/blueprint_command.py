import argparse

from enapter import cli

from .blueprint_download_command import BlueprintDownloadCommand
from .blueprint_get_command import BlueprintGetCommand
from .blueprint_upload_command import BlueprintUploadCommand
from .blueprint_validate_command import BlueprintValidateCommand


class BlueprintCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "blueprint", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="blueprint_command", required=True)
        for command in [
            BlueprintDownloadCommand,
            BlueprintGetCommand,
            BlueprintUploadCommand,
            BlueprintValidateCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.blueprint_command:
            case "download":
                await BlueprintDownloadCommand.run(args)
            case "get":
                await BlueprintGetCommand.run(args)
            case "upload":
                await BlueprintUploadCommand.run(args)
            case "validate":
                await BlueprintValidateCommand.run(args)
            case _:
                raise NotImplementedError(args.command_command)
