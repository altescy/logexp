from __future__ import annotations
import typing as tp

import contextlib
import os
import shutil
from pathlib import Path


class Storage:
    def __init__(self, rootdir: Path) -> None:
        if not rootdir.is_dir():
            raise RuntimeError(f"storage directory not found: {rootdir}")
        self._rootdir = rootdir

    @property
    def rootdir(self) -> Path:
        return self._rootdir.absolute()

    def mkdirs(self, path: str, exist_ok: bool = False) -> None:
        _check_path(path)
        os.makedirs(self.rootdir / path, exist_ok=exist_ok)

    def rmtree(self, path: str) -> None:
        _check_path(path)
        shutil.rmtree(self.rootdir / path)

    def remove(self, path: str) -> None:
        _check_path(path)
        os.remove(self.rootdir / path)

    @contextlib.contextmanager
    def open(self, path: str, *args, **kwargs) -> tp.Iterator:
        _check_path(path)
        with open(self.rootdir / path, *args, **kwargs)  as f:
            yield f

    def to_json(self) -> tp.Dict[str, tp.Any]:
        storage_dict = {
            "rootdir": str(self.rootdir),
        }
        return storage_dict

    @classmethod
    def from_json(cls, storage_dict: tp.Dict[str, tp.Any]) -> Storage:
        onestorage = Storage(
            rootdir=Path(storage_dict["rootdir"]),
        )
        return onestorage


def _check_path(path: str) -> None:
    # do not allow absolute path and parent path
    path = os.path.normpath(path)
    if path.startswith("/") or path.startswith("../"):
        raise RuntimeError("invalid path")
