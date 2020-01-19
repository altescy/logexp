from __future__ import annotations
import typing as tp

import configparser
import os
from pathlib import Path


DEFAULT_LOGSTORE_DIR = f"{os.getcwd()}/.logexp"


class Settings:
    @classmethod
    def _get_default_dict(cls) -> tp.Dict:
        default_dict = {
            "logexp": {
                "module": "",
                "execution_path": os.getcwd(),
                "editor": "vi",
            },
            "logstore": {
                "store_dir": f"{os.getcwd()}/.logexp",
            },
        }
        return default_dict

    def __init__(self) -> None:
        self._config = configparser.ConfigParser()
        self._config.read_dict(Settings._get_default_dict())
        self._config.read([
            f"{os.getcwd()}/logexp.ini",
            os.path.expanduser("~/.logexp.ini")
        ])

    def load(self, filename: Path) -> None:
        self._config.read(filename)

    @property
    def logexp_module(self) -> str:
        module = self._config["logexp"]["module"]
        return module

    @property
    def logexp_execpath(self) -> Path:
        return Path(self._config["logexp"]["execution_path"])

    @property
    def logexp_editor(self) -> str:
        return self._config["logexp"]["editor"]

    @property
    def logstore_storepath(self) -> Path:
        return Path(self._config["logstore"]["store_dir"])
