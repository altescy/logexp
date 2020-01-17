import argparse
import pprint

from logexp.cli.subcommand import Subcommand
from logexp.executor import Executor
from logexp.settings import DEFAULT_LOGSTORE_DIR


@Subcommand.add(
    name="run",
    description="run worker",
    help_="run worker",
)
class RunCommand(Subcommand):
    def set_arguments(self):

        self.parser.add_argument("-m", "--module", required=True,
                                 help="module name")
        self.parser.add_argument("-e", "--experiment", required=True,
                                 help="experiment id")
        self.parser.add_argument("-w", "--worker", required=True,
                                 help="worker name")
        self.parser.add_argument("-p", "--params",
                                 help="path to params file")
        self.parser.add_argument("--name",
                                 help="name this run")
        self.parser.add_argument("--note",
                                 help="add some note about this run")
        self.parser.add_argument("--exec-path",
                                 help="execution path", default=".")
        self.parser.add_argument("-s", "--store", default=DEFAULT_LOGSTORE_DIR,
                                 help="path to logstore directory")


    def run(self, args: argparse.Namespace) -> None:
        executor = Executor(
            rootdir=args.store,
            module=args.module,
            execution_path=args.exec_path,
        )
        run_info = executor.run(
            experiment_id=args.experiment,
            worker_name=args.worker,
            params_path=args.params,
            name=args.name,
            note=args.note,
        )
        pprint.pprint(run_info.to_json())
