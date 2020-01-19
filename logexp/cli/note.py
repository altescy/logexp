import argparse
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.logstore import LogStore
from logexp.settings import Settings
from logexp.utils.editor import edit


@Subcommand.add(
    name="note",
    description="edit run note",
    help_="edit run note",
)
class NoteCommand(Subcommand):
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

        if args.store is None:
            store_path = settings.logstore_storepath
        else:
            store_path = Path(args.store)

        store = LogStore(store_path)
        runinfo = store.load_run(args.run)

        note = edit(
            editor=settings.logexp_editor,
            filename="note.txt",
            text=runinfo.note,
        )

        runinfo.note = note

        store.save_run(runinfo)
