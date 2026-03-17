"""Rule delete command."""

import argparse

from enapter import cli, http


class RuleDeleteCommand(cli.Command):
    """Command to delete a rule."""

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        """Register the command in the subparsers."""
        parser = parent.add_parser(
            "delete", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", help="Rule ID")
        parser.add_argument("--site-id", help="Site ID")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the command."""
        async with http.api.Client(http.api.Config.from_env()) as client:
            await client.rule_engine.delete_rule(rule_id=args.id, site_id=args.site_id)
