"""Rule Engine command group."""

import argparse

from enapter import cli

from .rule_engine_get_command import RuleEngineGetCommand
from .rule_engine_resume_command import RuleEngineResumeCommand
from .rule_engine_suspend_command import RuleEngineSuspendCommand


class RuleEngineCommand(cli.Command):
    """Command group for Rule Engine management."""

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        """Register the command group in the subparsers."""
        parser = parent.add_parser(
            "rule-engine", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="rule_engine_command", required=True)
        for command in [
            RuleEngineGetCommand,
            RuleEngineSuspendCommand,
            RuleEngineResumeCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the sub-command."""
        match args.rule_engine_command:
            case "get":
                await RuleEngineGetCommand.run(args)
            case "suspend":
                await RuleEngineSuspendCommand.run(args)
            case "resume":
                await RuleEngineResumeCommand.run(args)
            case _:
                raise NotImplementedError(args.rule_engine_command)
