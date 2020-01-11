from logexp.experiment import Experiment
from logexp.worker import BaseWorker


class MyWorker(BaseWorker):
    def config(self):
        self.n_iter = 10

    def run(self):
        for i in range(self.n_iter):
            print(i)


class TestExperiment:
    @staticmethod
    def test_set_and_get_experiment():
        ex = Experiment("my_experiment")

        assert ex == Experiment.get_experiment("my_experiment")

    @staticmethod
    def test_set_and_get_worker():
        ex = Experiment("my_experiment")
        ex.worker("my_worker")(MyWorker)

        worker = ex.get_worker("my_worker")

        assert worker.name == "my_worker"
