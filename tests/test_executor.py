import json
import os
import tempfile
from pathlib import Path

from logexp.executor import Executor


class TestExecutor:
    @staticmethod
    def test_run():
        with tempfile.TemporaryDirectory() as tempdir:
            rootdir = Path(tempdir)

            executor = Executor(
                rootdir=rootdir,
                module="hello",
                execution_path="./examples",
            )

            experiment_id = executor.init("my_experiment")
            runinfo = executor.run(experiment_id, "my_worker")
