import argparse
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.logstore import LogStore
from logexp.settings import Settings


@Subcommand.add(
    name="delete",
    description="delete specified run",
    help_="delete specified run",
)
class DeleteCommand(Subcommand):
    def set_arguments(self):
        self.parser.add_argument("-r", "--run", required=True,
                                 help="run id")
        self.parser.add_argument("-f", "--force", action="store_true",
                                 help="force to remove run")
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

        if args.force:
            choise = "y"
        else:
            choise = input(f"Do you delete this run: {runinfo.uuid} ? [y/N] ")

        if choise.strip().lower() == "y":
            store.delete_run(runinfo.uuid)
