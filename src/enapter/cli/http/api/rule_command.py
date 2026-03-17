"""Rule command group."""

import argparse

from enapter import cli

from .rule_create_command import RuleCreateCommand
from .rule_delete_command import RuleDeleteCommand
from .rule_disable_command import RuleDisableCommand
from .rule_enable_command import RuleEnableCommand
from .rule_get_command import RuleGetCommand
from .rule_list_command import RuleListCommand
from .rule_update_command import RuleUpdateCommand
from .rule_update_script_command import RuleUpdateScriptCommand


class RuleCommand(cli.Command):
    """Command group for Rule management."""

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        """Register the command group in the subparsers."""
        parser = parent.add_parser(
            "rule", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="rule_command", required=True)
        for command in [
            RuleListCommand,
            RuleGetCommand,
            RuleCreateCommand,
            RuleUpdateCommand,
            RuleUpdateScriptCommand,
            RuleEnableCommand,
            RuleDisableCommand,
            RuleDeleteCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the sub-command."""
        match args.rule_command:
            case "list":
                await RuleListCommand.run(args)
            case "get":
                await RuleGetCommand.run(args)
            case "create":
                await RuleCreateCommand.run(args)
            case "update":
                await RuleUpdateCommand.run(args)
            case "update-script":
                await RuleUpdateScriptCommand.run(args)
            case "enable":
                await RuleEnableCommand.run(args)
            case "disable":
                await RuleDisableCommand.run(args)
            case "delete":
                await RuleDeleteCommand.run(args)
            case _:
                raise NotImplementedError(args.rule_command)
