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
        parser.add_argument("-s", "--site-id", help="Site ID")
        parser.add_argument(
            "-l",
            "--limit",
            type=int,
            help="Maximum number of rules to list",
        )
        parser.add_argument(
            "--offset",
            type=int,
            help="Number of rules to skip",
            default=0,
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the command."""
        async with http.api.Client(http.api.Config.from_env()) as client:
            async with client.rule_engine.list_rules(
                site_id=args.site_id, limit=args.limit, offset=args.offset
            ) as stream:
                async for rule in stream:
                    print(json.dumps(rule.to_dto()))
