import argparse
import json
import logging

from enapter import cli, http

from .command_arguments import parse_command_arguments

LOGGER = logging.getLogger(__name__)


class CommandExecuteCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "execute", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "-d",
            "--device-id",
            required=True,
            help="ID or slug of the device to execute the command on",
        )
        parser.add_argument(
            "-a",
            "--arguments",
            type=parse_command_arguments,
            help="JSON string of arguments to pass to the command",
        )
        parser.add_argument(
            "-l",
            "--log",
            action="store_true",
            help="Expand command execution log in the output",
        )
        parser.add_argument("name", help="Name of the command to execute")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            execution = await client.commands.execute(
                device_id=args.device_id,
                name=args.name,
                arguments=args.arguments,
                expand_log=args.log,
            )
            print(json.dumps(execution.to_dto()))
