import argparse
import datetime
import importlib
import sys
import tempfile
from pathlib import Path

from logexp.cli import Subcommand
from logexp.executor import Executor
from logexp.experiment import Experiment
from logexp.logstore import LogStore
from logexp.metadata.git import get_git_info
from logexp.metadata.platform import get_platform_info
from logexp.metadata.runinfo import RunInfo
from logexp.metadata.status import Status
from logexp.params import Params
from logexp.report import Report
from logexp.version import VERSION


class TestPruneCommand:
    def setup(self):
        self.parser = argparse.ArgumentParser("test parser")
        self.subparsers = self.parser.add_subparsers()

        for subcommand in Subcommand.subcommands:
            subcommand.setup(self.subparsers)

        sys.path.append("examples/")
        importlib.import_module("hello")

        self.experiment_name = "my_experiment"
        self.worker_name = "my_worker"
        self.experiment = Experiment.get_experiment(self.experiment_name)

    def test_runcommand(self):
        with tempfile.TemporaryDirectory() as tempdir:
            rootdir = Path(tempdir)

            store = LogStore(rootdir)

            experiment_id = store.create_experiment(self.experiment)
            run_id = store.create_run(experiment_id, self.worker_name)

            runinfo_interrupted = RunInfo(
                version=VERSION,
                uuid=run_id,
                name="interrupted run",
                module="test_module",
                execution_path=Path("test/path"),
                experiment_id=experiment_id,
                experiment_name=self.experiment_name,
                worker_name=self.worker_name,
                status=Status.INTERRUPTED,
                params=Params({"test": "params"}),
                report=Report({"test": "report"}),
                storage=store.get_storage(experiment_id, run_id),
                platform=get_platform_info(),
                git=get_git_info(),
                note="interrupted",
                stdout="test stdout",
                stderr="test stderr",
                start_time=datetime.datetime.now(),
                end_time=datetime.datetime.now(),
            )

            runinfo_failed = RunInfo(
                version=VERSION,
                uuid=run_id,
                name="failed run",
                module="test_module",
                execution_path=Path("test/path"),
                experiment_id=experiment_id,
                experiment_name=self.experiment_name,
                worker_name=self.worker_name,
                status=Status.FAILED,
                params=Params({"test": "params"}),
                report=Report({"test": "report"}),
                storage=store.get_storage(experiment_id, run_id),
                platform=get_platform_info(),
                git=get_git_info(),
                note="failed",
                stdout="test stdout",
                stderr="test stderr",
                start_time=datetime.datetime.now(),
                end_time=datetime.datetime.now(),
            )

            store.save_run(runinfo_interrupted)
            store.save_run(runinfo_failed)

            interrupted_run_path = rootdir / str(experiment_id) / self.worker_name / runinfo_interrupted.uuid
            failed_run_path = rootdir / str(experiment_id) / self.worker_name / runinfo_failed.uuid
            assert interrupted_run_path.exists()
            assert failed_run_path.exists()

            args = self.parser.parse_args([
                "prune", "-s", tempdir, "-f",
            ])

            args.func(args)

            assert not interrupted_run_path.exists()
            assert not failed_run_path.exists()
