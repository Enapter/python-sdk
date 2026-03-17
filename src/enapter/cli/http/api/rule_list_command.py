"""Rule list command."""

import argparse
import json

from enapter import cli, http


class RuleListCommand(cli.Command):
    """Command to list rules."""

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        """Register the command in the subparsers."""
        parser = parent.add_parser(
            "list", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("--site-id", help="Site ID")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the command."""
        async with http.api.Client(http.api.Config.from_env()) as client:
            rules = await client.rule_engine.list_rules(site_id=args.site_id)
            for rule in rules:
                print(json.dumps(rule.to_dto()))
