import argparse
from io import StringIO
from unittest.mock import patch

import pytest

from enapter import __version__
from enapter.cli.version_command import VersionCommand


@pytest.mark.asyncio
async def test_version_command_run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    VersionCommand.register(subparsers)
    args = parser.parse_args(["version"])

    with patch("sys.stdout", new=StringIO()) as fake_out:
        await VersionCommand.run(args)
        assert fake_out.getvalue().strip() == __version__
