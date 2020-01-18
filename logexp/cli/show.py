import argparse
import json
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.logstore import LogStore
from logexp.settings import Settings


@Subcommand.add(
    name="show",
    description="All of run details will print to the stdout as JSON format.",
    help_="All of run details will print to the stdout as JSON format.",
)
class ShowCommand(Subcommand):
    def set_arguments(self):
        self.parser.add_argument("-r", "--run", required=True,
                                 help="run id")
        self.parser.add_argument("-s", "--store", type=Path,
                                 help="path to logstore directory")
        self.parser.add_argument("--config-file", type=Path,
                                 help="logexp config file")

    def run(self, args: argparse.Namespace) -> None:
        settings = Settings()
        if args.config_file is not None:
            settings.load(args.config_file)

        store_path = args.store or settings.logstore_storepath

        store = LogStore(store_path)
        runinfo = store.load_run(args.run)
        print(json.dumps(runinfo.to_json(), indent=2))
