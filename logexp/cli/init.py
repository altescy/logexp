import argparse

from logexp.cli.subcommand import Subcommand
from logexp.executor import Executor


@Subcommand.add(
    name="init",
    description="initialize experiment",
    help_="initialize experiment",
)
class RunCommand(Subcommand):
    def set_arguments(self):
        self.parser.add_argument("-s", "--store", required=True,
                                 help="path to logstore directory")
        self.parser.add_argument("-m", "--module", required=True,
                                 help="module name")
        self.parser.add_argument("-e", "--experiment", required=True,
                                 help="experiment id")
        self.parser.add_argument("--exec-path",
                                 help="execution path", default=".")


    def run(self, args: argparse.Namespace) -> None:
        executor = Executor(
            rootdir=args.store,
            module=args.module,
            execution_path=args.exec_path,
        )
        experiment_id = executor.init(args.experiment)
        print(f"experiment id: {experiment_id}")
