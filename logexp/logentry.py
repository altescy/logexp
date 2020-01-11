from __future__ import annotations
import typing as tp

import dataclasses
import datetime

from logexp.git import GitInfo
from logexp.params import Params
from logexp.platform import PlatformInfo
from logexp.status import Status
from logexp.storage import Storage


_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def _datetime_to_str(onetime: datetime.datetime) -> str:
    return onetime.strftime(_DATETIME_FORMAT)


def _str_to_datetime(timestr: str) -> datetime.datetime:
    return datetime.datetime.strptime(timestr, _DATETIME_FORMAT)


@dataclasses.dataclass
class LogEntry:
    uuid: str
    name: str
    module: str
    experiment_name: str
    worker_name: str
    status: Status
    params: Params
    storage: Storage
    platform: PlatformInfo
    git: tp.Optional[GitInfo]
    note: tp.Optional[str]
    stdout: tp.Optional[str]
    stderr: tp.Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_json(self) -> tp.Dict[str, tp.Any]:
        entry = {
            "uuid": self.uuid,
            "name": self.name,
            "module": self.module,
            "experiment_name": self.experiment_name,
            "worker_name": self.worker_name,
            "status": self.status.value,
            "params": self.params.to_json(),
            "storage": self.storage.to_json(),
            "note": self.note,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "platform": self.platform.to_json(),
            "git": self.git.to_json() if self.git else None,
            "created_at": _datetime_to_str(self.created_at),
            "updated_at": _datetime_to_str(self.updated_at),
        }
        return entry
