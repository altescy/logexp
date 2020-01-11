import argparse

from logexp.cli.subcommand import Subcommand
from logexp.executor import Executor


@Subcommand.add(
    name="run",
    description="run worker",
    help_="run worker",
)
class RunCommand(Subcommand):
    def set_arguments(self):
        self.parser.add_argument("-o", "--output", required=True,
                                 help="path to output directory")
        self.parser.add_argument("-m", "--module", required=True,
                                 help="module name")
        self.parser.add_argument("-e", "--experiment", required=True,
                                 help="experiment name")
        self.parser.add_argument("-w", "--worker", required=True,
                                 help="worker name")
        self.parser.add_argument("-n", "--name",
                                 help="name this log-entry")
        self.parser.add_argument("--note",
                                 help="add some note about this log-entry")
        self.parser.add_argument("--exec-path",
                                 help="execution path", default=".")


    def run(self, args: argparse.Namespace) -> None:
        executor = Executor(
            base_path=args.output,
            module=args.module,
            experiment_name=args.experiment,
            worker_name=args.worker,
            execution_path=args.exec_path,
        )
        oneuuid = executor.run(args.name, args.note)
        print(f"logid: {oneuuid}")
