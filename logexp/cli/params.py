import argparse
import importlib
import pprint
import sys
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.experiment import Experiment
from logexp.logstore import LogStore


@Subcommand.add(
    name="params",
    description="initialize experiment",
    help_="initialize experiment",
)
class RunCommand(Subcommand):
    def set_arguments(self):
        module_group = self.parser.add_argument_group("params from module")
        module_group.add_argument("-m", "--module",
                                  help="module name")
        module_group.add_argument("-e", "--experiment", required=True,
                                  help="experiment name")
        module_group.add_argument("-w", "--worker",
                                  help="worker name")
        module_group.add_argument("--exec-path",
                                  help="execution path", default=".")

        run_group = self.parser.add_argument_group("params from run")
        run_group.add_argument("-s", "--store",
                               help="path to logstore directory")
        run_group.add_argument("-r", "--run",
                               help="run id")

    @staticmethod
    def _check_args(args: argparse.Namespace) -> None:
        is_module = all(
            x is not None
            for x in [args.module, args.experiment, args.worker]
        )
        is_run = all(
            x is not None
            for x in [args.store, args.run]
        )
        if not (is_module or is_run):
            raise RuntimeError("some arguments are missing")

    def run(self, args: argparse.Namespace) -> None:
        self._check_args(args)

        if args.module is not None:
            sys.path.append(args.exec_path)
            importlib.import_module(args.module)

            experiment = Experiment.get_experiment(args.experiment)
            worker = experiment.get_worker(args.worker)
            params = worker.params
        else:
            store = LogStore(Path(args.store))
            runinfo = store.load_run(args.run)
            params = runinfo.params

        pprint.pprint(params.to_json())
