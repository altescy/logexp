import logexp


ex = logexp.Experiment("my_experiment")

@ex.worker("my_worker")
class MyWorker(logexp.BaseWorker):
    def config(self):
        self.message = "hello world"

    def run(self):
        with self.storage.open("hello.txt", "w") as f:
            f.write(self.message)

        report = logexp.Report()
        report["foo"] = "bar"
        return report
