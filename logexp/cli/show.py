import argparse
import json
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.logstore import LogStore
from logexp.settings import DEFAULT_LOGSTORE_DIR


@Subcommand.add(
    name="show",
    description="All of run details will print to the stdout as JSON format.",
    help_="All of run details will print to the stdout as JSON format.",
)
class ShowCommand(Subcommand):
    def set_arguments(self):
        self.parser.add_argument("-r", "--run", required=True,
                                 help="run id")
        self.parser.add_argument("-s", "--store", default=DEFAULT_LOGSTORE_DIR,
                                 help="path to logstore directory")

    def run(self, args: argparse.Namespace) -> None:
        store = LogStore(Path(args.store))
        runinfo = store.load_run(args.run)
        print(json.dumps(runinfo.to_json(), indent=2))
