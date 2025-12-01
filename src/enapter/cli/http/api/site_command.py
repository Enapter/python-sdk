import argparse

from enapter import cli

from .site_create_command import SiteCreateCommand
from .site_delete_command import SiteDeleteCommand
from .site_get_command import SiteGetCommand
from .site_list_command import SiteListCommand
from .site_update_command import SiteUpdateCommand


class SiteCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "site", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="http_api_site_command", required=True)
        for command in [
            SiteCreateCommand,
            SiteDeleteCommand,
            SiteGetCommand,
            SiteListCommand,
            SiteUpdateCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.http_api_site_command:
            case "create":
                await SiteCreateCommand.run(args)
            case "delete":
                await SiteDeleteCommand.run(args)
            case "get":
                await SiteGetCommand.run(args)
            case "list":
                await SiteListCommand.run(args)
            case "update":
                await SiteUpdateCommand.run(args)
            case _:
                raise NotImplementedError(args.device_command)
