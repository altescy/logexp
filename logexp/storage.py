from __future__ import annotations
import typing as tp

import contextlib
import os
import shutil


class Storage:
    def __init__(self, path: str) -> None:
        if not os.path.isdir(path):
            raise RuntimeError(f"storage directory not found: {path}")
        self._path = path

    @property
    def path(self) -> str:
        return os.path.abspath(self._path)

    def _get_abspath(self, path: str) -> str:
        return os.path.join(self.path, path)

    def mkdirs(self, path: str, exist_ok: bool = False) -> None:
        _check_path(path)
        os.makedirs(self._get_abspath(path), exist_ok=exist_ok)

    def rmtree(self, path: str) -> None:
        _check_path(path)
        shutil.rmtree(self._get_abspath(path))

    def remove(self, path: str) -> None:
        _check_path(path)
        os.remove(self._get_abspath(path))

    @contextlib.contextmanager
    def open(self, path: str, *args, **kwargs) -> tp.Iterator:
        _check_path(path)
        with open(self._get_abspath(path), *args, **kwargs)  as f:
            yield f

    def to_json(self) -> tp.Dict[str, tp.Any]:
        storage_dict = {
            "path": self.path,
        }
        return storage_dict


def _check_path(path: str) -> None:
    # do not allow absolute path and parent path
    path = os.path.normpath(path)
    if path.startswith("/") or path.startswith("../"):
        raise RuntimeError("invalid path")
