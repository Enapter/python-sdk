import argparse
import datetime
import json

from enapter import cli, http


class CommandListExecutionsCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "list-executions", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "-l",
            "--limit",
            type=int,
            help="Maximum number of command executions to list",
        )
        parser.add_argument(
            "-o",
            "--order",
            choices=["created_at_asc", "created_at_desc"],
            help="Order of the listed command executions",
            default="created_at_asc",
        )
        parser.add_argument(
            "-d",
            "--device-id",
            help="ID or slug of the device to list command executions for",
        )
        parser.add_argument(
            "-s",
            "--site-id",
            help="ID of the site to list command executions for",
        )
        parser.add_argument(
            "--created-at-gte",
            help="Don't retrieve command executions older than provided date (ISO 8601 format)",
        )
        parser.add_argument(
            "--created-at-lt",
            help="Don't retrieve command executions newer than provided date (ISO 8601 format)",
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        if args.device_id is None and args.site_id is None:
            raise ValueError("either --device-id or --site-id must be provided")

        created_at_gte = (
            datetime.datetime.fromisoformat(args.created_at_gte)
            if args.created_at_gte is not None
            else None
        )
        created_at_lt = (
            datetime.datetime.fromisoformat(args.created_at_lt)
            if args.created_at_lt is not None
            else None
        )

        async with http.api.Client(http.api.Config.from_env()) as client:
            async with client.commands.list_executions(
                device_id=args.device_id,
                site_id=args.site_id,
                order=http.api.commands.ListExecutionsOrder(args.order.upper()),
                created_at_gte=created_at_gte,
                created_at_lt=created_at_lt,
                limit=args.limit,
            ) as stream:
                async for execution in stream:
                    print(json.dumps(execution.to_dto()))
