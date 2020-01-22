import typing as tp

import argparse
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.logstore import LogStore
from logexp.metadata.runinfo import RunInfo
from logexp.settings import Settings
from logexp.utils.table import Table


def _get_runinfo_table(runinfos: tp.List[RunInfo], max_column_width: int) -> Table:
    columns = ["run_id", "name", "exp_id", "exp_name", "worker",
               "status", "start_time", "end_time", "note"]
    runinfo_dicts = [
        {"run_id": x.uuid, "name": x.name,
         "exp_id": x.experiment_id, "exp_name": x.experiment_name,
         "worker": x.worker_name, "status": x.status.value,
         "start_time": x.start_time.strftime("%Y-%m-%d %H:%M:%S"),
         "end_time": x.end_time.strftime("%Y-%m-%d %H:%M:%S"),
         "note": x.note or ""}
        for x in runinfos
    ]

    table = Table(columns=columns, max_column_width=max_column_width)
    for item in runinfo_dicts:
        table.add(item)

    table.sort("start_time")

    return table


@Subcommand.add(
    name="list",
    description="list up items",
    help_="list up items",
)
class ListCommand(Subcommand):
    def set_arguments(self):
        self.parser.add_argument("-e", "--experiment", type=int,
                                 help="experiment id")
        self.parser.add_argument("-w", "--worker",
                                 help="worker name")
        self.parser.add_argument("-s", "--store", type=Path,
                                 help="path to logstore directory")
        self.parser.add_argument("-c", "--columns",
                                 help="show specified columns (comma separated string)")
        self.parser.add_argument("--max-column-width", type=int, default=40,
                                 help="maximum column width (>=3)")
        sort_group = self.parser.add_argument_group("sort options")
        sort_group.add_argument("--sort",
                                help="sort by specified column")
        sort_group.add_argument("--desc", action="store_true",
                                help="sort by descending order")
        self.parser.add_argument("--config-file", type=Path,
                                 help="logexp config file")

    def run(self, args: argparse.Namespace) -> None:
        settings = Settings()
        if args.config_file is not None:
            settings.load(args.config_file)

        store_path = args.store or settings.logstore_storepath

        store = LogStore(store_path)
        runinfos = store.get_runs(args.experiment, args.worker)

        table = _get_runinfo_table(runinfos, args.max_column_width)

        if args.sort is not None:
            table.sort(args.sort, args.desc)

        if args.columns is not None:
            columns = args.columns.split(",")
            table = table[columns]

        table.print()
