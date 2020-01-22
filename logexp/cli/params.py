import argparse
import importlib
import json
import sys
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.experiment import Experiment
from logexp.logstore import LogStore
from logexp.settings import Settings


@Subcommand.add(
    name="params",
    description="export params with JSON format",
    help_="export params with JSON format",
)
class ParamsCommand(Subcommand):
    def set_arguments(self):
        module_group = self.parser.add_argument_group("params from module")
        module_group.add_argument("-m", "--module",
                                  help="module name")
        module_group.add_argument("-e", "--experiment",
                                  help="experiment name")
        module_group.add_argument("-w", "--worker",
                                  help="worker name")
        module_group.add_argument("--exec-path", type=Path,
                                  help="execution path")

        run_group = self.parser.add_argument_group("params from run")
        run_group.add_argument("-r", "--run",
                               help="run id")
        run_group.add_argument("-s", "--store", type=Path,
                               help="path to logstore directory")
        self.parser.add_argument("--config-file", type=Path,
                                 help="logexp config file")

    def run(self, args: argparse.Namespace) -> None:
        settings = Settings()
        if args.config_file is not None:
            settings.load(args.config_file)

        module = args.module or settings.logexp_module

        # check arguments
        is_module = all([args.experiment is not None, args.worker, module])
        is_run = args.run is not None
        if not (is_module or is_run):
            raise RuntimeError("some arguments are missing")

        if is_run:
            if args.store is None:
                store_path = settings.logstore_storepath
            else:
                store_path = Path(args.store)

            store = LogStore(store_path)
            runinfo = store.load_run(args.run)
            params = runinfo.params
        else:
            sys.path.append(args.exec_path or str(settings.logexp_execpath))
            importlib.import_module(module)

            experiment = Experiment.get_experiment(args.experiment)
            worker = experiment.get_worker(args.worker)
            params = worker.params

        print(json.dumps(params.to_json(), indent=2))
