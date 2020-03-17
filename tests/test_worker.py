import sys
import importlib
import tempfile
from pathlib import Path

from logexp.experiment import Experiment
from logexp.worker import BaseWorker
from logexp.params import Params
from logexp.storage import Storage


class TestWorker:
    def setup(self):
        sys.path.append("examples/")
        importlib.import_module("hello")
        ex = Experiment.get_experiment("my_experiment")
        self.worker = ex.get_worker("my_worker")

    def test_config(self):
        assert self.worker.message == "hello world"
        assert self.worker.params["message"] == "hello world"

    def test_call(self):
        with tempfile.TemporaryDirectory() as workdir:
            params = Params({"message": "good morning"})
            storage = Storage(Path(workdir))
            self.worker(params=params, storage=storage)
            assert self.worker.message == "good morning"
            assert self.worker.params["message"] == "good morning"
