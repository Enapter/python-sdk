import argparse

from enapter.cli.http.api.device_list_command import DeviceListCommand
from enapter.cli.http.api.site_list_command import SiteListCommand


def test_site_list_pagination():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    SiteListCommand.register(subparsers)

    args = parser.parse_args(["list", "--limit", "10", "--offset", "20"])
    assert args.limit == 10
    assert args.offset == 20


def test_device_list_pagination():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    DeviceListCommand.register(subparsers)

    args = parser.parse_args(["list", "--limit", "10", "--offset", "20"])
    assert args.limit == 10
    assert args.offset == 20
