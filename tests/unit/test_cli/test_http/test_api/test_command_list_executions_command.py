import argparse

import pytest

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

    # Test with both (should fail due to mutual exclusivity)
    with pytest.raises(SystemExit):
        parser.parse_args(
            ["list-executions", "--device-id", "dev_123", "--site-id", "site_123"]
        )

    # Test with neither (should fail as one is required)
    with pytest.raises(SystemExit):
        parser.parse_args(["list-executions"])
