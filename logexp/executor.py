from __future__ import annotations
import typing as tp

import datetime
import importlib
import json
import sys
from pathlib import Path

from logexp.utils.capture import capture
from logexp import error
from logexp.experiment import Experiment
from logexp.logstore import LogStore
from logexp.metadata.git import GitInfo, get_git_info
from logexp.metadata.runinfo import RunInfo
from logexp.metadata.platform import get_platform_info
from logexp.metadata.status import Status
from logexp.params import Params
from logexp.report import Report
from logexp.version import VERSION
from logexp.worker import BaseWorker


class Executor:
    def __init__(
            self,
            rootdir: tp.Union[Path, str],
            module: str,
            execution_path: tp.Union[Path, str],
    ) -> None:
        self._store = LogStore(Path(rootdir))
        self._module = module
        self._execution_path = Path(execution_path).absolute()

        if execution_path is not None:
            sys.path.append(str(execution_path))
        importlib.import_module(module)

    @staticmethod
    def _load_params(path: Path):
        with open(path, "r") as f:
            params_dict = json.load(f)
        return Params.from_json(params_dict)

    def _build_runinfo(
            self,
            experiment_id: int,
            experiment: Experiment,
            worker: BaseWorker,
            run_id: str,
            name: str,
            status: Status,
            params: Params,
            report: Report = None,
            note: str = None,
            stdout: str = None,
            stderr: str = None,
    ) -> RunInfo:
        storage = self._store.get_storage(experiment_id, run_id)

        gitinfo: tp.Optional[GitInfo] = None
        try:
            gitinfo = get_git_info()
        except (error.GitCommandNotFoundError,
                error.GitRepositoryNotFoundError):
            gitinfo = None

        runinfo = RunInfo(
            version=VERSION,
            uuid=run_id,
            name=name,
            module=self._module,
            execution_path=self._execution_path,
            experiment_id=experiment_id,
            experiment_name=experiment.name,
            worker_name=worker.name,
            status=status,
            params=params,
            report=report,
            storage=storage,
            platform=get_platform_info(),
            git=gitinfo,
            note=note,
            stdout=stdout,
            stderr=stderr,
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now(),
        )

        return runinfo

    def init(
            self,
            experiment_name: str,
    ) -> int:
        experiment = Experiment.get_experiment(experiment_name)
        experiment_id = self._store.create_experiment(experiment)
        return experiment_id

    def run(
            self,
            experiment_id: int,
            worker_name: str,
            params_path: Path = None,
            name: str = None,
            note: str = None,
    ) -> RunInfo:
        name = name or ""

        experiment = self._store.get_experiment(experiment_id)
        worker = experiment.get_worker(worker_name)

        params = (
            self._load_params(params_path)
            if params_path else worker.params
        )

        # make sure that worker_name exists before create_run
        run_id = self._store.create_run(experiment_id, worker_name)

        runinfo = self._build_runinfo(
            experiment_id=experiment_id,
            experiment=experiment,
            worker=worker,
            run_id=run_id,
            name=name,
            status=Status.RUNNING,
            params=params,
            note=note,
        )

        self._store.save_run(runinfo)

        worker.setup(
            storage=runinfo.storage,
            params=params,
        )

        report: tp.Optional[Report] = None

        try:
            with capture() as captured_out:
                report = worker.run()
        except KeyboardInterrupt:
            runinfo.status = Status.INTERRUPTED
        except Exception as e: # pylint: disable=broad-except
            runinfo.status = Status.FAILED
            raise e
        else:
            runinfo.status = Status.FINISHED
        finally:
            runinfo.report = report
            runinfo.stdout = captured_out["stdout"]
            runinfo.stderr = captured_out["stderr"]

            runinfo.end_time = datetime.datetime.now()

            self._store.save_run(runinfo)

        return runinfo
