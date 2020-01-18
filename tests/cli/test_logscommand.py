import argparse
import tempfile
from pathlib import Path

from logexp.cli import Subcommand
from logexp.executor import Executor


class TestLogsCommand:
    def setup(self):
        self.parser = argparse.ArgumentParser("test parser")
        self.subparsers = self.parser.add_subparsers()

        for subcommand in Subcommand.subcommands:
            subcommand.setup(self.subparsers)

    def test_runcommand(self):
        module = "hello"
        execution_path = "./example"
        experiment_name = "my_experiment"
        worker_name = "my_worker"

        with tempfile.TemporaryDirectory() as tempdir:
            rootdir = Path(tempdir)

            executor = Executor(
                rootdir=rootdir,
                module=module,
                execution_path=execution_path,
            )

            experiment_id = executor.init(experiment_name)
            runinfo = executor.run(experiment_id, worker_name)

            args = self.parser.parse_args([
                "logs",
                "-s", tempdir,
                "-e", experiment_id,
                "-w", worker_name
            ])

            args.func(args)
