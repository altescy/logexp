from __future__ import annotations
import typing as tp

import dataclasses
import datetime
from pathlib import Path

from logexp.metadata.git import GitInfo
from logexp.params import Params
from logexp.report import Report
from logexp.metadata.platform import PlatformInfo
from logexp.metadata.status import Status
from logexp.storage import Storage


_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def _datetime_to_str(onetime: datetime.datetime) -> str:
    return onetime.strftime(_DATETIME_FORMAT)


def _str_to_datetime(timestr: str) -> datetime.datetime:
    return datetime.datetime.strptime(timestr, _DATETIME_FORMAT)


@dataclasses.dataclass
class RunInfo:
    version: str
    uuid: str
    name: str
    module: str
    execution_path: Path
    experiment_id: int
    experiment_name: str
    worker_name: str
    status: Status
    params: Params
    storage: Storage
    report: tp.Optional[Report]
    platform: PlatformInfo
    git: tp.Optional[GitInfo]
    note: tp.Optional[str]
    stdout: tp.Optional[str]
    stderr: tp.Optional[str]
    start_time: datetime.datetime
    end_time: datetime.datetime

    def to_json(self) -> tp.Dict[str, tp.Any]:
        info = {
            "version": self.version,
            "uuid": self.uuid,
            "name": self.name,
            "module": self.module,
            "execution_path": str(self.execution_path),
            "experiment_id": self.experiment_id,
            "experiment_name": self.experiment_name,
            "worker_name": self.worker_name,
            "status": self.status.value,
            "params": self.params.to_json(),
            "storage": self.storage.to_json(),
            "report": self.report.to_json() if self.report else None,
            "note": self.note,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "platform": self.platform.to_json(),
            "git": self.git.to_json() if self.git else None,
            "start_time": _datetime_to_str(self.start_time),
            "end_time": _datetime_to_str(self.end_time),
        }
        return info

    @classmethod
    def from_json(cls, info_dict: tp.Dict[str, tp.Any]) -> RunInfo:
        git_info: tp.Optional[GitInfo] = None
        if info_dict["git"] is not None:
            git_info = GitInfo.from_json(info_dict["git"])

        report: tp.Optional[Report] = None
        if info_dict["report"] is not None:
            report = Report.from_json(info_dict["report"])

        runinfo = RunInfo(
            version=info_dict["version"],
            uuid=info_dict["uuid"],
            name=info_dict["name"],
            module=info_dict["module"],
            execution_path=Path(info_dict["execution_path"]),
            experiment_id=int(info_dict["experiment_id"]),
            experiment_name=info_dict["experiment_name"],
            worker_name=info_dict["worker_name"],
            status=Status(info_dict["status"]),
            params=Params.from_json(info_dict["params"]),
            storage=Storage.from_json(info_dict["storage"]),
            report=report,
            note=info_dict["note"],
            stdout=info_dict["stdout"],
            stderr=info_dict["stderr"],
            platform=PlatformInfo.from_json(info_dict["platform"]),
            git=git_info,
            start_time=_str_to_datetime(info_dict["start_time"]),
            end_time=_str_to_datetime(info_dict["end_time"]),
        )
        return runinfo
