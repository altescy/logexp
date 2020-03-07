from __future__ import annotations
import typing as tp

import contextlib
import io
import sys

class TeeingStreamProxy:
    def __init__(self, stream: tp.IO, out: tp.IO):
        self._stream = stream
        self._out = out

    def __getattr__(self, name: str):
        return getattr(self._stream, name)

    def write(self, data):
        self._stream.write(data)
        self._out.write(data)

    def flush(self):
        self._stream.flush()
        self._out.flush()


@contextlib.contextmanager
def capture():
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    orig_stdout, orig_stderr = sys.stdout, sys.stderr

    sys.stdout.flush()
    sys.stderr.flush()

    sys.stdout = TeeingStreamProxy(sys.stdout, stdout_buffer)
    sys.stderr = TeeingStreamProxy(sys.stderr, stderr_buffer)

    out = {
        "stdout": "",
        "stderr": "",
    }

    try:
        yield out
    finally:
        sys.stdout.flush()
        sys.stderr.flush()

        out["stdout"] = stdout_buffer.getvalue()
        out["stderr"] = stderr_buffer.getvalue()

        stdout_buffer.close()
        stderr_buffer.close()

        sys.stdout, sys.stderr = orig_stdout, orig_stderr
