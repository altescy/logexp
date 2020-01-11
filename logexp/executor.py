from __future__ import annotations
import typing as tp

import datetime
import importlib
import json
import os
import sys
import uuid

from logexp.capture import capture
from logexp import error
from logexp.experiment import Experiment
from logexp.git import GitInfo, get_git_info
from logexp.logentry import LogEntry
from logexp.platform import get_platform_info
from logexp.status import Status
from logexp.storage import Storage
from logexp.worker import BaseWorker


class Executor:
    _ENTRY_FILENAME = "info.json"
    _STORAGE_DIRNAME = "storage"

    def __init__(
            self,
            base_path: str,
            module: str,
            experiment_name: str,
            worker_name: str,
            execution_path: str = ".",
    ) -> None:
        sys.path.append(execution_path)
        importlib.import_module(module)

        self._base_path = base_path
        self._module = module
        self._experiment = Experiment.get_experiment(experiment_name)
        self._worker = self._experiment.get_worker(worker_name)

    @staticmethod
    def _get_default_runname(
            experiment: Experiment,
            worker: BaseWorker
    ) -> str:
        date = datetime.datetime.now().strftime("%Y%m%d")
        name = f"{experiment.name}_{worker.name}_{date}"
        return name

    @staticmethod
    def _get_uuid() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def _save_entry(path: str, entry: LogEntry) -> None:
        with open(path, "w") as f:
            json.dump(entry.to_json(), f)

    def load(self, oneuuid: str) -> None:
        """load specified run and set params"""

    def run(self, name: str = None, note: str = None) -> str:
        if name is None:
            name = self._get_default_runname(self._experiment, self._worker)

        oneuuid = self._get_uuid()
        working_path = os.path.join(self._base_path, oneuuid)
        entry_path = os.path.join(working_path, self._ENTRY_FILENAME)
        storage_path = os.path.join(working_path, self._STORAGE_DIRNAME)

        gitinfo: tp.Optional[GitInfo] = None
        try:
            gitinfo = get_git_info()
        except (error.GitCommandNotFoundError,
                error.GitRepositoryNotFoundError):
            gitinfo = None

        os.mkdir(working_path)
        os.mkdir(storage_path)

        storage = Storage(storage_path)
        self._worker.setup(storage=storage)

        entry = LogEntry(
            uuid=oneuuid,
            name=name,
            module=self._module,
            experiment_name=self._experiment.name,
            worker_name=self._worker.name,
            status=Status.RUNNING,
            params=self._worker.params,
            storage=self._worker.storage,
            platform=get_platform_info(),
            git=gitinfo,
            note=note,
            stdout=None,
            stderr=None,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

        self._save_entry(entry_path, entry)

        try:
            with capture() as captured_out:
                self._worker.run()
        except KeyboardInterrupt:
            entry.status = Status.INTERRUPTED
        except Exception: # pylint: disable=broad-except
            entry.status = Status.FAILED
        else:
            entry.status = Status.FINISHED

        entry.stdout = captured_out["stdout"]
        entry.stderr = captured_out["stderr"]

        self._save_entry(entry_path, entry)

        return oneuuid
