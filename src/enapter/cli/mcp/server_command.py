import argparse
import asyncio

from enapter import cli, mcp


class ServerCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "server", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("--host", default="127.0.0.1", help="Host to listen on")
        parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
        parser.add_argument(
            "--http-api-base-url",
            default="https://api.enapter.com",
            help="Base URL of Enapter HTTP API",
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with mcp.Server(
            host=args.host, port=args.port, http_api_base_url=args.http_api_base_url
        ):
            await asyncio.Event().wait()
