import argparse
import logging

from enapter import log

from . import http, mcp


class App:

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args

    @classmethod
    def new(cls) -> "App":
        parser = argparse.ArgumentParser(
            prog="enapter", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("-v", "--verbose", action="store_true")
        subparsers = parser.add_subparsers(dest="command", required=True)
        for command in [
            http.Command,
            mcp.Command,
        ]:
            command.register(subparsers)
        return cls(args=parser.parse_args())

    async def run(self) -> None:
        log.configure(level=logging.DEBUG if self.args.verbose else logging.INFO)
        match self.args.command:
            case "http":
                await http.Command.run(self.args)
            case "mcp":
                await mcp.Command.run(self.args)
            case _:
                raise NotImplementedError(self.args.command)
