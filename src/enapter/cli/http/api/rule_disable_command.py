"""Rule disable command."""

import argparse
import json

from enapter import cli, http


class RuleDisableCommand(cli.Command):
    """Command to disable a rule."""

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        """Register the command in the subparsers."""
        parser = parent.add_parser(
            "disable", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", help="Rule ID")
        parser.add_argument("--site-id", help="Site ID")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the command."""
        async with http.api.Client(http.api.Config.from_env()) as client:
            rule = await client.rule_engine.disable_rule(
                rule_id=args.id, site_id=args.site_id
            )
            print(json.dumps(rule.to_dto()))
