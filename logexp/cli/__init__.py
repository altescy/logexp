import argparse

from logexp.version import VERSION
from logexp.cli.subcommand import Subcommand
from logexp.cli import (
    run, init, params, list as list_cmd,
    logs, show, delete, note, prune, rename
)


def main():
    parser = argparse.ArgumentParser("logexp: simple logging tool for machine learning")
    parser.add_argument("--version", action="store_true")

    subparsers = parser.add_subparsers()

    for subcommand in Subcommand.subcommands:
        subcommand.setup(subparsers)

    args = parser.parse_args()
    func = getattr(args, "func", None)

    if args.version and func is None:
        print(VERSION)
    elif func is not None:
        func(args)
    else:
        parser.parse_args(["--help"])
