import argparse
import json


def parse_command_arguments(arguments_string: str | None) -> dict:
    if arguments_string is None:
        return {}
    try:
        return json.loads(arguments_string)
    except json.JSONDecodeError as e:
        raise argparse.ArgumentTypeError(f"Decode JSON: {e.msg}")
