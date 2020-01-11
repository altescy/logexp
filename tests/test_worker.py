import sys
import importlib

from logexp.experiment import Experiment
from logexp.worker import BaseWorker
from logexp.params import Params


class TestWorker:
    def setup(self):
        sys.path.append("examples/")
        importlib.import_module("hello")
        ex = Experiment.get_experiment("my_experiment")
        self.worker = ex.get_worker("my_worker")

    def test_config(self):
        assert self.worker.message == "hello world"
        assert self.worker.params["message"] == "hello world"

    def test_setup_params(self):
        params = Params({"message": "good morning"})
        self.worker.setup(params=params)
        assert self.worker.message == "good morning"
        assert self.worker.params["message"] == "good morning"
