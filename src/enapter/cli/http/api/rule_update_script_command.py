"""Rule update script command."""

import argparse
import json
import sys

from enapter import cli, http


class RuleUpdateScriptCommand(cli.Command):
    """Command to update a rule's script."""

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        """Register the command in the subparsers."""
        parser = parent.add_parser(
            "update-script", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("id", help="Rule ID")
        parser.add_argument(
            "script",
            help="Path to the rule script file, or '-' to read from stdin",
        )
        parser.add_argument("--site-id", help="Site ID")
        parser.add_argument(
            "--runtime-version",
            choices=["V1", "V3"],
            default="V3",
            help="Rule runtime version",
        )
        parser.add_argument(
            "--exec-interval", help="Execution interval (required for V1)"
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the command."""
        if args.script == "-":
            code = sys.stdin.read()
        else:
            with open(args.script, "r", encoding="utf-8") as f:
                code = f.read()

        runtime_version = http.api.rule_engine.RuntimeVersion(args.runtime_version)
        script = http.api.rule_engine.RuleScript(
            code=code,
            runtime_version=runtime_version,
            exec_interval=args.exec_interval,
        )

        async with http.api.Client(http.api.Config.from_env()) as client:
            rule = await client.rule_engine.update_rule_script(
                rule_id=args.id, script=script, site_id=args.site_id
            )
            print(json.dumps(rule.to_dto()))
