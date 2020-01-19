import argparse
import tempfile
from pathlib import Path

from logexp.cli import Subcommand
from logexp.executor import Executor


class TestParamsCommand:
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
            args = self.parser.parse_args([
                "params", "-m", module,
                "-e", experiment_name, "-w", worker_name,
            ])

            args.func(args)
