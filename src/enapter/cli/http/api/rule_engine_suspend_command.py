"""Rule Engine suspend command."""

import argparse
import json

from enapter import cli, http


class RuleEngineSuspendCommand(cli.Command):
    """Command to suspend the rule engine."""

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        """Register the command in the subparsers."""
        parser = parent.add_parser(
            "suspend", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("-s", "--site-id", help="ID of the site to suspend")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the command."""
        async with http.api.Client(http.api.Config.from_env()) as client:
            engine = await client.rule_engine.suspend(site_id=args.site_id)
            print(json.dumps(engine.to_dto()))
