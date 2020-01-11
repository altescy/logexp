from logexp.worker import BaseWorker
from logexp.params import Params


class SampleWorker(BaseWorker):
    def config(self):
        self.n_iter = 10

    def run(self):
        for i in range(self.n_iter):
            print(i)


class TestWorker:
    def setup(self):
        self.worker = SampleWorker("sample_worker")

    def test_config(self):
        assert self.worker.n_iter == 10
        assert self.worker.params["n_iter"] == 10

    def test_setup_params(self):
        params = Params({"n_iter": 20})
        self.worker.setup(params=params)
        assert self.worker.n_iter == 20
        assert self.worker.params["n_iter"] == 20
