from __future__ import annotations
import typing as tp

import argparse


class Subcommand:
    subcommands: tp.List["Subcommand"] = []

    @classmethod
    def add(cls, name: str, description: str, help_: str) -> tp.Callable:
        def decorator(T: tp.Type[Subcommand]) -> tp.Type[Subcommand]:
            subcommand = T(name, description, help_)
            Subcommand.subcommands.append(subcommand)
            return T
        return decorator

    def __init__(
            self,
            name: str,
            description: str,
            help_: str
    ) -> None:
        self._name = name
        self._description = description
        self._help = help_

        self._parser: tp.Optional[argparse.ArgumentParser] = None

    @property
    def parser(self) -> argparse.ArgumentParser:
        if self._parser is None:
            raise RuntimeError("parser is not set")
        return self._parser

    def setup(self, subparsers: argparse._SubParsersAction) -> None: # pylint: disable=protected-access
        self._parser = subparsers.add_parser(
            self._name, description=self._description, help=self._help
        )
        self.set_arguments()
        self.parser.set_defaults(func=self.run)

    def set_arguments(self) -> None:
        raise NotImplementedError

    def run(self, args: argparse.Namespace) -> None:
        raise NotImplementedError
