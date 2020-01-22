import argparse
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.logstore import LogStore
from logexp.metadata.status import Status
from logexp.settings import Settings


@Subcommand.add(
    name="prune",
    description="delete all failed and interrupted runs",
    help_="delete all failed and interrupted runs",
)
class PruneCommand(Subcommand):
    def set_arguments(self):
        self.parser.add_argument("-e", "--experiment", type=int,
                                 help="experiment id")
        self.parser.add_argument("-w", "--worker",
                                 help="worker name")
        self.parser.add_argument("-s", "--store", type=Path,
                                 help="path to logstore directory")
        self.parser.add_argument("-f", "--force", action="store_true",
                                 help="force to remove runs")
        self.parser.add_argument("--config-file", type=Path,
                                 help="logexp config file")

    def run(self, args: argparse.Namespace) -> None:
        settings = Settings()
        if args.config_file is not None:
            settings.load(args.config_file)

        store_path = args.store or settings.logstore_storepath

        store = LogStore(store_path)
        runinfos = [
            x for x in store.get_runs(args.experiment, args.worker)
            if x.status == Status.FAILED or x.status == Status.INTERRUPTED
        ]

        if args.force:
            choise = "y"
        else:
            print("Following runs will be removed:")
            for runinfo in runinfos:
                print(f"  {runinfo.uuid}")
            choise = input("Are you sure you want to continue? [y/N] ")

        if choise.strip().lower() == "y":
            for runinfo in runinfos:
                store.delete_run(runinfo.uuid)
