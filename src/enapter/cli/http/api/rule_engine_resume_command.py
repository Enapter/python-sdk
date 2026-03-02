"""Rule Engine resume command."""

import argparse
import json

from enapter import cli, http


class RuleEngineResumeCommand(cli.Command):
    """Command to resume the rule engine."""

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        """Register the command in the subparsers."""
        parser = parent.add_parser(
            "resume", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("-s", "--site-id", help="ID of the site to resume")

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the command."""
        async with http.api.Client(http.api.Config.from_env()) as client:
            engine = await client.rule_engine.resume(site_id=args.site_id)
            print(json.dumps(engine.to_dto()))
