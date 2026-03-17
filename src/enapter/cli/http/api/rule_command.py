"""Rule command group."""

import argparse

from enapter import cli


class RuleCommand(cli.Command):
    """Command group for Rule management."""

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        """Register the command group in the subparsers."""
        parser = parent.add_parser(
            "rule", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="rule_command", required=True)
        # TODO: Register sub-commands here
        # For now, we'll add a dummy sub-parser so it doesn't fail on registration
        subparsers.add_parser("list")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the sub-command."""
        match args.rule_command:
            case "list":
                print("List rules command placeholder")
            case _:
                raise NotImplementedError(args.rule_command)
