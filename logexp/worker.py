from __future__ import annotations
import typing as tp

import contextlib

from logexp.params import Params
from logexp.report import Report
from logexp.storage import Storage


class BaseWorker:
    def __init__(self, name: str) -> None:
        self._name = name

        self._within_config_scope = False
        self.__init_done = True

        self._storage: tp.Optional[Storage] = None

        self._params = Params()

        with self.config_scope():
            self.config()

    def __setattr__(self, name: str, value: tp.Any):
        if self.within_config_scope and name != "_within_config_scope":
            self._params[name] = value
        super().__setattr__(name, value)

    def _check_init_done(self) -> None:
        if not self.__init_done:
            raise RuntimeError("BaseWorker.__init__() has not been called.")

    @property
    def within_config_scope(self) -> bool:
        return getattr(self, "_within_config_scope", False) # type:ignore

    @contextlib.contextmanager
    def config_scope(self) -> tp.Iterator[tp.Any]:
        self._check_init_done()
        old_flag = self.within_config_scope
        self._within_config_scope = True
        try:
            yield
        finally:
            self._within_config_scope = old_flag

    def setup(
            self,
            storage: Storage = None,
            params: Params = None,
    ) -> None:
        if storage is not None:
            self._storage = storage

        if params is not None:
            with self.config_scope():
                for key, value in params.items():
                    setattr(self, key, value)

    @property
    def params(self) -> Params:
        return self._params

    @property
    def name(self) -> str:
        return self._name

    @property
    def storage(self) -> Storage:
        if self._storage is None:
            raise RuntimeError("storage is not set")
        return self._storage

    def config(self):
        """define worker parameters"""

    def run(self) -> tp.Optional[Report]:
        raise NotImplementedError
