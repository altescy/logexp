import argparse
import glob
import tempfile

from logexp.cli import Subcommand


class TestRunCommand:
    def setup(self):
        self.parser = argparse.ArgumentParser("test parser")
        self.subparsers = self.parser.add_subparsers()

        for subcommand in Subcommand.subcommands:
            subcommand.setup(self.subparsers)

    def test_runcommand(self):
        with tempfile.TemporaryDirectory() as tempdir:
            args = self.parser.parse_args([
                "run", "-o", tempdir, "-m" , "hello",
                "-e", "my_experiment", "-w", "my_worker",
                "--exec-path", "examples/"
            ])

            args.func(args)

            print(glob.glob(f"{tempdir}/**"))
            logdir = glob.glob(f"{tempdir}/*")[0]

            with open(f"{logdir}/storage/hello.txt") as f:
                text = f.read()

            assert text == "hello world"
