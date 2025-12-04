import argparse

from enapter import cli

from .command_create_execution_command import CommandCreateExecutionCommand
from .command_execute_command import CommandExecuteCommand
from .command_get_execution_command import CommandGetExecutionCommand
from .command_list_executions_command import CommandListExecutionsCommand


class CommandCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "command", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="command_command", required=True)
        for command in [
            CommandCreateExecutionCommand,
            CommandExecuteCommand,
            CommandGetExecutionCommand,
            CommandListExecutionsCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.command_command:
            case "create-execution":
                await CommandCreateExecutionCommand.run(args)
            case "execute":
                await CommandExecuteCommand.run(args)
            case "get-execution":
                await CommandGetExecutionCommand.run(args)
            case "list-executions":
                await CommandListExecutionsCommand.run(args)
            case _:
                raise NotImplementedError(args.command_command)
