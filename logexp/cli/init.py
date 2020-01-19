import argparse
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.executor import Executor
from logexp.settings import Settings


@Subcommand.add(
    name="init",
    description="initialize experiment",
    help_="initialize experiment",
)
class InitCommand(Subcommand):
    def set_arguments(self):

        self.parser.add_argument("-e", "--experiment", required=True,
                                 help="experiment id")
        self.parser.add_argument("--exec-path", type=Path,
                                 help="execution path")
        self.parser.add_argument("-m", "--module",
                                 help="module name")
        self.parser.add_argument("-s", "--store", type=Path,
                                 help="path to logstore directory")
        self.parser.add_argument("--config-file", type=Path,
                                 help="logexp config file")

    def run(self, args: argparse.Namespace) -> None:
        settings = Settings()
        if args.config_file is not None:
            settings.load(args.config_file)

        store_path = args.store or settings.logstore_storepath
        module = args.module or settings.logexp_module
        exec_path = args.exec_path or settings.logexp_execpath

        if not module:
            raise RuntimeError("module is required")

        executor = Executor(
            rootdir=store_path,
            module=module,
            execution_path=exec_path,
        )
        experiment_id = executor.init(args.experiment)
        print(f"experiment id: {experiment_id}")
