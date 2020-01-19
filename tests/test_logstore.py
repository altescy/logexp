import datetime
import importlib
import sys
import tempfile
import uuid
from pathlib import Path

from logexp.experiment import Experiment
from logexp.metadata.git import get_git_info
from logexp.logstore import LogStore
from logexp.params import Params
from logexp.report import Report
from logexp.metadata.platform import get_platform_info
from logexp.metadata.status import Status
from logexp.metadata.runinfo import RunInfo
from logexp.version import VERSION


class TestLogStore:
    def setup(self):
        sys.path.append("examples/")
        importlib.import_module("hello")

        self.experiment_name = "my_experiment"
        self.worker_name = "my_worker"
        self.experiment = Experiment.get_experiment(self.experiment_name)

    def test_create_and_get_experiment(self):
        with tempfile.TemporaryDirectory() as tempdir:
            rootdir = Path(tempdir)

            store = LogStore(rootdir)

            experiment_id = store.create_experiment(self.experiment)
            experiment = store.get_experiment(experiment_id)

            assert experiment.name == self.experiment_name

    def test_save_and_load_run(self):
        with tempfile.TemporaryDirectory() as tempdir:
            rootdir = Path(tempdir)

            store = LogStore(rootdir)

            experiment_id = store.create_experiment(self.experiment)
            run_id = store.create_run(experiment_id, self.worker_name)

            run_info = RunInfo(
                version=VERSION,
                uuid=run_id,
                name="test run",
                module="test_module",
                execution_path=Path("test/path"),
                experiment_id=experiment_id,
                experiment_name=self.experiment_name,
                worker_name=self.worker_name,
                status=Status.FINISHED,
                params=Params({"test": "params"}),
                report=Report({"test": "report"}),
                storage=store.get_storage(experiment_id, run_id),
                platform=get_platform_info(),
                git=get_git_info(),
                note="test note",
                stdout="test stdout",
                stderr="test stderr",
                start_time=datetime.datetime.now(),
                end_time=datetime.datetime.now(),
            )

            store.save_run(run_info)

            run_info_ = store.load_run(run_id)

            assert run_info_.uuid == run_id
            assert run_info_.stdout == "test stdout"

    def test_get_runs(self):
        with tempfile.TemporaryDirectory() as tempdir:
            rootdir = Path(tempdir)

            store = LogStore(rootdir)

            experiment_id = store.create_experiment(self.experiment)
            run_id = store.create_run(experiment_id, self.worker_name)

            run_info = RunInfo(
                version=VERSION,
                uuid=run_id,
                name="test run",
                module="test_module",
                execution_path=Path("test/path"),
                experiment_id=experiment_id,
                experiment_name=self.experiment_name,
                worker_name=self.worker_name,
                status=Status.FINISHED,
                params=Params({"test": "params"}),
                report=Report({"test": "report"}),
                storage=store.get_storage(experiment_id, run_id),
                platform=get_platform_info(),
                git=get_git_info(),
                note="test note",
                stdout="test stdout",
                stderr="test stderr",
                start_time=datetime.datetime.now(),
                end_time=datetime.datetime.now(),
            )

            store.save_run(run_info)

            runinfos = store.get_runs(
                experiment_id=experiment_id,
                worker_name=self.worker_name
            )

            assert runinfos[0].uuid == run_id

    def test_delete_run(self):
        with tempfile.TemporaryDirectory() as tempdir:
            rootdir = Path(tempdir)

            store = LogStore(rootdir)

            experiment_id = store.create_experiment(self.experiment)
            run_id = store.create_run(experiment_id, self.worker_name)

            run_info = RunInfo(
                version=VERSION,
                uuid=run_id,
                name="test run",
                module="test_module",
                execution_path=Path("test/path"),
                experiment_id=experiment_id,
                experiment_name=self.experiment_name,
                worker_name=self.worker_name,
                status=Status.FINISHED,
                params=Params({"test": "params"}),
                report=Report({"test": "report"}),
                storage=store.get_storage(experiment_id, run_id),
                platform=get_platform_info(),
                git=get_git_info(),
                note="test note",
                stdout="test stdout",
                stderr="test stderr",
                start_time=datetime.datetime.now(),
                end_time=datetime.datetime.now(),
            )

            store.save_run(run_info)

            assert (rootdir / str(experiment_id) / self.worker_name / run_id).exists()

            runinfos = store.delete_run(run_id)

            assert not (rootdir / str(experiment_id) / self.worker_name / run_id).exists()


