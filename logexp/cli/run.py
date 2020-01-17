import argparse
import pprint

from logexp.cli.subcommand import Subcommand
from logexp.executor import Executor
from logexp.metadata.runinfo import RunInfo
from logexp.settings import DEFAULT_LOGSTORE_DIR


_RUNINFO_SUMMARY_TEMPLATE = """** SUMMARY **
  run_id     : {run_id}
  name       : {name}
  module     : {module}
  experiment : {experiment}
  worker     : {worker}
  status     : {status}
  artifacts  : {artifacts}
  start_time : {start_time}
  end_time   : {end_time}"""


def _print_summary(runinfo: RunInfo) -> None:
    summary = _RUNINFO_SUMMARY_TEMPLATE.format(
        run_id=runinfo.uuid,
        name=runinfo.name,
        module=runinfo.module,
        experiment=runinfo.experiment_name,
        worker=runinfo.worker_name,
        status=runinfo.status.value,
        artifacts=runinfo.storage.to_json(),
        start_time=runinfo.start_time,
        end_time=runinfo.end_time,
    )
    print(summary)


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
        _print_summary(run_info)
