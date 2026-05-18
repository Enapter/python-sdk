import argparse

from enapter import cli

from .blueprint_profiles_download_command import BlueprintProfilesDownloadCommand


class BlueprintProfilesCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "profiles", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(
            dest="blueprint_profiles_command", required=True
        )
        for command in [
            BlueprintProfilesDownloadCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.blueprint_profiles_command:
            case "download":
                await BlueprintProfilesDownloadCommand.run(args)
            case _:
                raise NotImplementedError(args.blueprint_profiles_command)
