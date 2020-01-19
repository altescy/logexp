from __future__ import annotations
import typing as tp

import json
import re
import shutil
import uuid
from pathlib import Path

from logexp.experiment import Experiment
from logexp.metadata.runinfo import RunInfo
from logexp.storage import Storage


class LogStore:
    _META_FILE = "meta.json"
    _PARAMS_FILE = "params.json"
    _REPORT_FILE = "report.json"
    _STDOUT_FILE = "stdout.txt"
    _STDERR_FILE = "stderr.txt"
    _NOTE_FILE = "note.txt"
    _PLATFORM_FILE = "platform.json"
    _GIT_VERSION_FILE = "version.txt"
    _GIT_STATE_FILE = "state.txt"
    _GIT_HEAD_FILE = "head.txt"
    _GIT_DIFF_FILE = "diff.txt"
    _GIT_DIR = "git"
    _ARTIFACTS_DIR = "artifacts"
    _EXPERIEMT_DIR_PATTERN = re.compile(r"^[0-9]+$")

    def __init__(self, rootdir: Path) -> None:
        if rootdir.exists() and not  rootdir.is_dir():
            raise RuntimeError(f"root_dir is not a directory: {rootdir}")

        self._rootdir = rootdir

        rootdir.mkdir(exist_ok=True)

    def _check_experiment_exists(self, experiment_id: int) -> None:
        experiment_path = self._rootdir / str(experiment_id)
        if not experiment_path.exists():
            raise FileNotFoundError(f"experiment not found: {experiment_path}")

    def _get_experiment_ids(self) -> tp.List[int]:
        experiment_ids = [
            int(x.name) for x in _get_paths_with_pattern(
                self._rootdir, self._EXPERIEMT_DIR_PATTERN
            )
        ]
        return experiment_ids

    def _get_worker_names(self, experiment_id: int) -> tp.List[str]:
        self._check_experiment_exists(experiment_id)

        experiment_path = self._get_experiment_path(experiment_id)
        worker_names = [
            x.name for x in experiment_path.iterdir()
        ]
        return worker_names

    def _get_experiment_path(self, experiment_id: int) -> Path:
        return self._rootdir / str(experiment_id)

    def create_experiment(self, experiment: Experiment) -> int:
        experiment_ids = sorted(self._get_experiment_ids())

        experiment_id = experiment_ids[-1] + 1 if experiment_ids else 0
        experiment_path = self._get_experiment_path(experiment_id)

        experiment_path.mkdir()
        experiment_dict = experiment.to_json()
        with open(experiment_path / self._META_FILE, "w") as f:
            json.dump(experiment_dict, f)

        return experiment_id

    def _search_run_path(self, run_id: str) -> Path:
        run_paths = list(self._rootdir.glob(f"*/*/{run_id}"))
        if not run_paths:
            raise FileNotFoundError(f"run not found: {run_id}")
        if len(run_paths) > 1:
            raise RuntimeError("duplicate run_id")

        run_path = run_paths[0]
        return run_path

    def create_run(self, experiment_id: int, worker_name: str) -> str:
        self._check_experiment_exists(experiment_id)

        experiment_path = self._get_experiment_path(experiment_id)
        worker_path = experiment_path / worker_name

        worker_path.mkdir(exist_ok=True)

        run_id = uuid.uuid4().hex

        run_path = worker_path / run_id
        run_path.mkdir()

        return run_id

    def get_experiment(self, experiment_id: int) -> Experiment:
        self._check_experiment_exists(experiment_id)

        experiment_path = self._get_experiment_path(experiment_id)
        with open(experiment_path / self._META_FILE) as f:
            experiment_dict = json.load(f)

        experiment = Experiment.from_json(experiment_dict)
        return experiment

    def get_storage(self, experiment_id: int, run_id: str) -> Storage:
        self._check_experiment_exists(experiment_id)

        experiment_path = self._get_experiment_path(experiment_id)

        run_paths = list(experiment_path.glob(f"*/{run_id}"))
        if not run_paths:
            raise FileNotFoundError(f"run not found: {run_id}")

        run_path = run_paths[0]
        storage_path = run_path / self._ARTIFACTS_DIR

        storage_path.mkdir(exist_ok=True)

        return Storage(storage_path)

    def save_run(self, runinfo: RunInfo) -> None:
        self._check_experiment_exists(runinfo.experiment_id)

        experiment_path = self._get_experiment_path(runinfo.experiment_id)

        worker_path = experiment_path / runinfo.worker_name

        run_path = worker_path / runinfo.uuid

        if not run_path.exists():
            raise FileNotFoundError(f"run not found: {run_path}")

        runinfo_dict = runinfo.to_json()

        meta_dict = {
            key: runinfo_dict[key]
            for key in [
                "version", "uuid", "name", "module", "execution_path",
                "experiment_id", "experiment_name", "worker_name", "status",
                "storage", "start_time", "end_time",
            ]
        }
        with open(run_path / self._META_FILE, "w") as f:
            json.dump(meta_dict, f)

        params_path = run_path / self._PARAMS_FILE
        if not params_path.exists():
            params_dict = runinfo_dict["params"]
            with open(params_path, "w") as f:
                json.dump(params_dict, f)

        report = runinfo_dict["report"]
        if report is not None:
            with open(run_path / self._REPORT_FILE, "w") as f:
                json.dump(report, f)

        stdout = runinfo_dict["stdout"]
        if stdout is not None:
            with open(run_path / self._STDOUT_FILE, "w") as f:
                f.write(stdout)

        stderr = runinfo_dict["stderr"]
        if stderr is not None:
            with open(run_path / self._STDERR_FILE, "w") as f:
                f.write(stderr)

        note = runinfo_dict["note"]
        if note is not None:
            with open(run_path / self._NOTE_FILE, "w") as f:
                f.write(note)

        platform_path = run_path / self._PLATFORM_FILE
        if not platform_path.exists():
            platform_dict = runinfo_dict["platform"]
            with open(platform_path, "w") as f:
                json.dump(platform_dict, f)

        git_path = run_path / self._GIT_DIR
        if runinfo.git is not None and not git_path.exists():
            git_path.mkdir()
            git_dict = runinfo_dict["git"]

            git_version = git_dict["version"]
            with open(git_path / self._GIT_VERSION_FILE, "w") as f:
                f.write(git_version)

            git_head = git_dict["head"]
            with open(git_path / self._GIT_HEAD_FILE, "w") as f:
                f.write(git_head)

            git_state = git_dict["state"]
            with open(git_path / self._GIT_STATE_FILE, "w") as f:
                f.write(git_state)

            git_diff = git_dict["diff"]
            if git_diff:
                with open(git_path / self._GIT_DIFF_FILE, "w") as f:
                    f.write(git_diff)

    def load_run(self, run_id: str) -> RunInfo:
        run_path = self._search_run_path(run_id)

        with open(run_path / self._META_FILE, "r") as f:
            meta_dict = json.load(f)

        with open(run_path / self._PARAMS_FILE, "r") as f:
            params_dict = json.load(f)

        report_dict: tp.Optional[tp.Dict[str, tp.Any]] = None
        report_path = run_path / self._REPORT_FILE
        if report_path.exists():
            with open(report_path, "r") as f:
                report_dict = json.load(f)

        stdout: tp.Optional[str] = None
        stdout_path = run_path / self._STDOUT_FILE
        if stdout_path.exists():
            with open(stdout_path, "r") as f:
                stdout = f.read()

        stderr: tp.Optional[str] = None
        stderr_path = run_path / self._STDERR_FILE
        if stderr_path.exists():
            with open(stderr_path, "r") as f:
                stderr = f.read()

        note: tp.Optional[str] = None
        note_path = run_path / self._NOTE_FILE
        if note_path.exists():
            with open(note_path, "r") as f:
                note = f.read()

        with open(run_path / self._PLATFORM_FILE, "r") as f:
            platform_dict = json.load(f)

        git_path = run_path / self._GIT_DIR
        git_dict: tp.Optional[tp.Dict[str, tp.Any]] = None

        if git_path.exists():
            git_dict = {}

            with open(git_path / self._GIT_VERSION_FILE, "r") as f:
                git_dict["version"] = f.read()

            with open(git_path / self._GIT_HEAD_FILE, "r") as f:
                git_dict["head"] = f.read()

            with open(git_path / self._GIT_STATE_FILE, "r") as f:
                git_dict["state"] = f.read()

            git_diff_path = git_path / self._GIT_DIFF_FILE
            if git_diff_path.exists():
                with open(git_diff_path, "r") as f:
                    git_dict["diff"] = f.read()
            else:
                git_dict["diff"] = None

        runinfo_dict = {
            "version": meta_dict["version"],
            "uuid": meta_dict["uuid"],
            "name": meta_dict["name"],
            "module": meta_dict["module"],
            "execution_path": meta_dict["execution_path"],
            "experiment_id": meta_dict["experiment_id"],
            "experiment_name": meta_dict["experiment_name"],
            "worker_name": meta_dict["worker_name"],
            "status": meta_dict["status"],
            "storage": meta_dict["storage"],
            "start_time": meta_dict["start_time"],
            "end_time": meta_dict["end_time"],
            "params": params_dict,
            "report": report_dict,
            "note": note,
            "stdout": stdout,
            "stderr": stderr,
            "platform": platform_dict,
            "git": git_dict,
        }
        return RunInfo.from_json(runinfo_dict)

    def delete_run(self, run_id: str) -> None:
        run_path = self._search_run_path(run_id)
        shutil.rmtree(run_path)

    def _get_run_ids(self, experiment_id: int, worker_name: str) -> tp.List[str]:
        experiment_path = self._get_experiment_path(experiment_id)
        worker_path = experiment_path / worker_name
        run_ids = [x.name for x in worker_path.glob("*")]
        return run_ids

    def get_runs(
            self,
            experiment_id: int = None,
            worker_name: str = None
    ) -> tp.List[RunInfo]:
        if experiment_id is not None:
            self._check_experiment_exists(experiment_id)

        experiment_id_str = str(experiment_id or "*")
        worker_name = worker_name or "*"

        runs: tp.List[RunInfo] = []
        run_paths = self._rootdir.glob(f"{experiment_id_str}/{worker_name}/*")
        for run_path in run_paths:
            run_id_ = run_path.parts[-1]
            run_info = self.load_run(run_id_)
            runs.append(run_info)

        return runs


def _get_paths_with_pattern(rootdir: Path, pattern: tp.Pattern) -> tp.List[Path]:
    return [x for x in rootdir.glob("*") if re.match(pattern, x.name)]
