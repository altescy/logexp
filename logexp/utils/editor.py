from __future__ import annotations

import tempfile
import subprocess
from pathlib import Path


def edit(editor: str, filename: str = None, text: str = None) -> str:
    filename = filename or "tmp"

    with tempfile.TemporaryDirectory() as tempdir:
        filepath = Path(tempdir) / filename

        if text:
            with open(filepath, "w") as f:
                f.write(text)

        subprocess.call([editor, str(filepath)])

        with open(filepath, "r") as f:
            edited_text = f.read()

    return edited_text
