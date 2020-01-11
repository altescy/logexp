import logexp


ex = logexp.Experiment("my_experiment")

@ex.worker("my_worker")
class MyWorker(logexp.BaseWorker):
    def config(self):
        self.n_iter = 10

    def run(self):
        with self.storage.open("hello.txt", "w") as f:
            f.write("hello world")
