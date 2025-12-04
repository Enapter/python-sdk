import argparse
import json
import logging

from enapter import cli, http

LOGGER = logging.getLogger(__name__)


class CommandGetExecutionCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "get-execution", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "-d",
            "--device-id",
            required=True,
            help="ID or slug of the device to get the command execution of",
        )
        parser.add_argument(
            "-l",
            "--log",
            action="store_true",
            help="Expand command execution log in the output",
        )
        parser.add_argument(
            "execution_id", help="ID of the command execution to retrieve"
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            execution = await client.commands.get_execution(
                device_id=args.device_id,
                execution_id=args.execution_id,
                expand_log=args.log,
            )
            print(json.dumps(execution.to_dto()))
