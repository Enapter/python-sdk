"""Rule update command."""

import argparse
import json

from enapter import cli, http


class RuleUpdateCommand(cli.Command):
    """Command to update a rule's slug."""

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        """Register the command in the subparsers."""
        parser = parent.add_parser(
            "update", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", help="Rule ID")
        parser.add_argument("--slug", required=True, help="New rule slug")
        parser.add_argument("--site-id", help="Site ID")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the command."""
        async with http.api.Client(http.api.Config.from_env()) as client:
            rule = await client.rule_engine.update_rule(
                rule_id=args.id, slug=args.slug, site_id=args.site_id
            )
            print(json.dumps(rule.to_dto()))
