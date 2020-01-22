import argparse
import json
from pathlib import Path

from logexp.cli.subcommand import Subcommand
from logexp.executor import Executor
from logexp.metadata.runinfo import RunInfo
from logexp.report import Report
from logexp.settings import Settings


_RUNINFO_SUMMARY_TEMPLATE = """
** SUMMARY **
run_id     : {run_id}
name       : {name}
module     : {module}
experiment : {experiment}
worker     : {worker}
status     : {status}
artifacts  : {artifacts}
start_time : {start_time}
end_time   : {end_time}
"""

_REPORT_TEMPLATE = """
** WORKER REPORT **
{report}
"""


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


def _print_report(report: Report) -> None:
    report_dict = report.to_json()
    report_json = json.dumps(report_dict, indent=2)
    report_str = _REPORT_TEMPLATE.format(report=report_json)
    print(report_str)

@Subcommand.add(
    name="run",
    description="run worker",
    help_="run worker",
)
class RunCommand(Subcommand):
    def set_arguments(self):
        self.parser.add_argument("-e", "--experiment", required=True,
                                 help="experiment id")
        self.parser.add_argument("-w", "--worker", required=True,
                                 help="worker name")
        self.parser.add_argument("-p", "--params", type=Path,
                                 help="path to params file")
        self.parser.add_argument("--name",
                                 help="name this run")
        self.parser.add_argument("--note",
                                 help="add some note about this run")
        self.parser.add_argument("-m", "--module",
                                 help="module name")
        self.parser.add_argument("--exec-path", type=Path,
                                 help="execution path")
        self.parser.add_argument("-s", "--store", type=Path,
                                 help="path to logstore directory")
        self.parser.add_argument("--config-file", type=Path,
                                 help="logexp config file")

    def run(self, args: argparse.Namespace) -> None:
        settings = Settings()
        if args.config_file is not None:
            settings.load(args.config_file)

        module = args.module or settings.logexp_module
        store_path = args.store or settings.logstore_storepath
        exec_path = args.exec_path or settings.logexp_execpath

        if not module:
            raise RuntimeError("module is required")

        executor = Executor(
            rootdir=store_path,
            module=module,
            execution_path=exec_path,
        )
        run_info = executor.run(
            experiment_id=args.experiment,
            worker_name=args.worker,
            params_path=args.params,
            name=args.name,
            note=args.note,
        )

        if run_info.report is not None:
            _print_report(run_info.report)

        _print_summary(run_info)
