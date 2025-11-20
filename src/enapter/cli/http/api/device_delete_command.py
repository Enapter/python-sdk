import argparse
import logging

from enapter import cli, http

LOGGER = logging.getLogger(__name__)


class DeviceDeleteCommand(cli.Command):

    @staticmethod
    def register(parent: cli.Subparsers) -> None:
        parser = parent.add_parser(
            "delete", formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            "ids", metavar="id", nargs="+", help="ID or slug of the device to delete"
        )

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        async with http.api.Client(http.api.Config.from_env()) as client:
            for id in args.ids:
                try:
                    await client.devices.delete(id)
                except http.api.Error as e:
                    LOGGER.error("failed to delete device %s: %s", id, e)
