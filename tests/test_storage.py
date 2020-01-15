import os
import tempfile
from pathlib import Path

from logexp.storage import Storage


class TestStorage:
    @staticmethod
    def test_mkdirs():
        with tempfile.TemporaryDirectory() as tempdir:
            rootdir = Path(tempdir)
            storage = Storage(rootdir)
            storage.mkdirs("foo")

            assert os.path.isdir(os.path.join(tempdir, "foo"))

    @staticmethod
    def test_rmtree():
        with tempfile.TemporaryDirectory() as tempdir:
            rootdir = Path(tempdir)
            storage = Storage(rootdir)
            storage.mkdirs("foo/bar")

            assert (rootdir / "foo").is_dir()
            assert (rootdir / "foo/bar").is_dir()

            storage.rmtree("foo")

            assert not (rootdir / "foo").exists()

    @staticmethod
    def test_open():
        with tempfile.TemporaryDirectory() as tempdir:
            rootdir = Path(tempdir)
            storage = Storage(rootdir)

            with storage.open("foo.txt", "w") as f:
                f.write("hello")

            assert (rootdir / "foo.txt").exists()

            with storage.open("foo.txt", "r") as f:
                text = f.read()

            assert text == "hello"
