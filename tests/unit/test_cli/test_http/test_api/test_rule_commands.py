import argparse

from enapter.cli.http.api.rule_create_command import RuleCreateCommand
from enapter.cli.http.api.rule_delete_command import RuleDeleteCommand
from enapter.cli.http.api.rule_disable_command import RuleDisableCommand
from enapter.cli.http.api.rule_enable_command import RuleEnableCommand
from enapter.cli.http.api.rule_get_command import RuleGetCommand
from enapter.cli.http.api.rule_list_command import RuleListCommand
from enapter.cli.http.api.rule_update_command import RuleUpdateCommand
from enapter.cli.http.api.rule_update_script_command import RuleUpdateScriptCommand


def test_rule_list_command_alias():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    RuleListCommand.register(subparsers)

    # This should succeed now
    args = parser.parse_args(["list", "-s", "site_123"])
    assert args.site_id == "site_123"

    # This should also succeed
    args = parser.parse_args(["list", "--site-id", "site_123"])
    assert args.site_id == "site_123"


def test_rule_list_command_pagination():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    RuleListCommand.register(subparsers)

    args = parser.parse_args(["list", "--limit", "10", "--offset", "20"])
    assert args.limit == 10
    assert args.offset == 20


def test_rule_create_command_alias():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    RuleCreateCommand.register(subparsers)

    args = parser.parse_args(["create", "script.py", "-s", "site_123"])
    assert args.site_id == "site_123"


def test_rule_delete_command_alias():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    RuleDeleteCommand.register(subparsers)

    args = parser.parse_args(["delete", "rule_id", "-s", "site_123"])
    assert args.site_id == "site_123"


def test_rule_disable_command_alias():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    RuleDisableCommand.register(subparsers)

    args = parser.parse_args(["disable", "rule_id", "-s", "site_123"])
    assert args.site_id == "site_123"


def test_rule_enable_command_alias():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    RuleEnableCommand.register(subparsers)

    args = parser.parse_args(["enable", "rule_id", "-s", "site_123"])
    assert args.site_id == "site_123"


def test_rule_get_command_alias():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    RuleGetCommand.register(subparsers)

    args = parser.parse_args(["get", "rule_id", "-s", "site_123"])
    assert args.site_id == "site_123"


def test_rule_update_command_alias():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    RuleUpdateCommand.register(subparsers)

    args = parser.parse_args(
        ["update", "rule_id", "--slug", "new-slug", "-s", "site_123"]
    )
    assert args.site_id == "site_123"


def test_rule_update_script_command_alias():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    RuleUpdateScriptCommand.register(subparsers)

    args = parser.parse_args(
        ["update-script", "rule_id", "script.py", "-s", "site_123"]
    )
    assert args.site_id == "site_123"
