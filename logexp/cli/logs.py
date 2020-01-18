import argparse
import json
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.logstore import LogStore
from logexp.settings import Settings


@Subcommand.add(
    name="logs",
    description="dump logs in json format",
    help_="dump logs in json format",
)
class LogsCommand(Subcommand):
    def set_arguments(self):
        self.parser.add_argument("-e", "--experiment", type=int,
                                 help="experiment id")
        self.parser.add_argument("-w", "--worker",
                                 help="worker name")
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
        runinfos = store.get_runs(args.experiment, args.worker)
        runinfo_dicts = [x.to_json() for x in runinfos]
        print(json.dumps(runinfo_dicts))
