import typing as tp

import argparse
import json
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.logstore import LogStore
from logexp.metadata.runinfo import RunInfo
from logexp.settings import DEFAULT_LOGSTORE_DIR
from logexp.utils.table import Table


@Subcommand.add(
    name="logs",
    description="dump logs in json format",
    help_="dump logs in json format",
)
class ListCommand(Subcommand):
    def set_arguments(self):
        self.parser.add_argument("-e", "--experiment", type=int,
                                 help="experiment id")
        self.parser.add_argument("-w", "--worker",
                                 help="worker name")
        self.parser.add_argument("-s", "--store", default=DEFAULT_LOGSTORE_DIR,
                                 help="path to logstore directory")

    def run(self, args: argparse.Namespace) -> None:
        store = LogStore(Path(args.store))
        runinfos = store.get_runs(args.experiment, args.worker)
        runinfo_dicts = [x.to_json() for x in runinfos]
        print(json.dumps(runinfo_dicts))
