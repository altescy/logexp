import sys
import importlib

from logexp.experiment import Experiment
from logexp.worker import BaseWorker


class TestExperiment:
    @staticmethod
    def setup():
        sys.path.append("examples/")
        importlib.import_module("hello")

    @staticmethod
    def test_set_and_get_experiment():
        ex =  Experiment.get_experiment("my_experiment")

        assert ex.name == "my_experiment"

    @staticmethod
    def test_set_and_get_worker():
        ex = Experiment.get_experiment("my_experiment")
        worker = ex.get_worker("my_worker")

        assert worker.name == "my_worker"
