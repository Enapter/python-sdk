import argparse

from enapter.cli.http.api.command_list_executions_command import (
    CommandListExecutionsCommand,
)


def test_register():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    CommandListExecutionsCommand.register(subparsers)

    # Test with device-id
    args = parser.parse_args(["list-executions", "--device-id", "dev_123"])
    assert args.device_id == "dev_123"
    assert args.site_id is None

    # Test with site-id
    args = parser.parse_args(["list-executions", "--site-id", "site_123"])
    assert args.site_id == "site_123"
    assert args.device_id is None

    # Test with both (should succeed)
    args = parser.parse_args(
        ["list-executions", "--device-id", "dev_123", "--site-id", "site_123"]
    )
    assert args.device_id == "dev_123"
    assert args.site_id == "site_123"

    # Test with neither (should still fail as one is required, but SystemExit will be raised by run())
    # Actually, argparse won't raise SystemExit now because I removed the required=True from the group.
    # The run() method will raise cli.CommandError.
    args = parser.parse_args(["list-executions"])
    assert args.device_id is None
    assert args.site_id is None
