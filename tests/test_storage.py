import os
import tempfile

from logexp.storage import Storage


class TestStorage:
    @staticmethod
    def test_mkdirs():
        with tempfile.TemporaryDirectory() as tempdir:
            storage = Storage(tempdir)
            storage.mkdirs("foo")

            assert os.path.isdir(os.path.join(tempdir, "foo"))

    @staticmethod
    def test_rmtree():
        with tempfile.TemporaryDirectory() as tempdir:
            storage = Storage(tempdir)
            storage.mkdirs("foo/bar")

            assert os.path.isdir(os.path.join(tempdir, "foo"))
            assert os.path.isdir(os.path.join(tempdir, "foo/bar"))

            storage.rmtree("foo")

            assert not os.path.exists(os.path.join(tempdir, "foo"))

    @staticmethod
    def test_open():
        with tempfile.TemporaryDirectory() as tempdir:
            storage = Storage(tempdir)

            with storage.open("foo.txt", "w") as f:
                f.write("hello")

            assert os.path.exists(os.path.join(tempdir, "foo.txt"))

            with storage.open("foo.txt", "r") as f:
                text = f.read()

            assert text == "hello"
