import json
import os
import sys
import tempfile

from logexp.executor import Executor
from logexp.experiment import Experiment
from logexp.metadata.status import Status
from logexp.worker import BaseWorker


class TestExecutor:
    @staticmethod
    def test_run():
        with tempfile.TemporaryDirectory() as tempdir:
            executor = Executor(
                base_path=tempdir,
                module="hello",
                experiment_name="my_experiment",
                worker_name="my_worker",
                execution_path="./examples"
            )

            oneuuid = executor.run("test_run", note="some note...")

            entry_filename = getattr(executor, "_ENTRY_FILENAME")
            storage_dirname = getattr(executor, "_STORAGE_DIRNAME")

            with open(os.path.join(tempdir, oneuuid, entry_filename)) as f:
                entry = json.load(f)

            with open(os.path.join(tempdir, oneuuid, storage_dirname, "hello.txt")) as f:
                text = f.read()

            assert entry["status"] == Status.FINISHED.value
            assert text == "hello world"
