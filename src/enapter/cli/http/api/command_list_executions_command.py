import argparse
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
            default=-1,
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
            required=True,
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        if args.limit == 0:
            return
        async with http.api.Client(http.api.Config.from_env()) as client:
            async with client.commands.list_executions(
                device_id=args.device_id,
                order=http.api.commands.ListExecutionsOrder(args.order.upper()),
            ) as stream:
                count = 0
                async for device in stream:
                    print(json.dumps(device.to_dto()))
                    count += 1
                    if args.limit > 0 and count == args.limit:
                        break
