import argparse

from enapter import cli

from .telemetry_latest_command import TelemetryLatestCommand
from .telemetry_timeseries_command import TelemetryTimeseriesCommand


class TelemetryCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "telemetry", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="telemetry_command", required=True)
        for command in [
            TelemetryLatestCommand,
            TelemetryTimeseriesCommand,
        ]:
            command.register(subparsers)

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        match args.telemetry_command:
            case "latest":
                await TelemetryLatestCommand.run(args)
            case "timeseries":
                await TelemetryTimeseriesCommand.run(args)
            case _:
                raise NotImplementedError(args.telemetry_command)
