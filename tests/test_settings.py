from logexp.settings import Settings

import os
import tempfile
from pathlib import Path


class TestSettings:
    @staticmethod
    def test_settings():
        with tempfile.TemporaryDirectory() as tempdir:
            before_path = os.getcwd()

            path = Path(tempdir)
            os.chdir(path)

            with open(path / "logexp.ini", "w") as f:
                f.write(
                    "[logexp]\n"
                    "module = foo"
                )

            settings = Settings()

            assert settings.logexp_module == "foo"

        os.chdir(before_path)
