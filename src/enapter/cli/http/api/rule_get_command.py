"""Rule get command."""

import argparse
import json

from enapter import cli, http


class RuleGetCommand(cli.Command):
    """Command to get a single rule."""

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        """Register the command in the subparsers."""
        parser = parent.add_parser(
            "get", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", help="Rule ID")
        parser.add_argument("--site-id", help="Site ID")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the command."""
        async with http.api.Client(http.api.Config.from_env()) as client:
            rule = await client.rule_engine.get_rule(
                rule_id=args.id, site_id=args.site_id
            )
            print(json.dumps(rule.to_dto()))
