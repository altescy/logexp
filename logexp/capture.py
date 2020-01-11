from __future__ import annotations

import contextlib
import os
import subprocess
import sys
import tempfile
import traceback


@contextlib.contextmanager
def capture():
    with tempfile.TemporaryDirectory() as temppath:
        stdout_path = os.path.join(temppath, "stdout.txt")
        stderr_path = os.path.join(temppath, "stderr.txt")

        original_stdout_fd = 1
        original_stderr_fd = 2
        saved_stdout_fd = os.dup(original_stdout_fd)
        saved_stderr_fd = os.dup(original_stderr_fd)

        tee_out = subprocess.Popen(
            ["tee", "-a", stdout_path],
            start_new_session=True,
            stdin=subprocess.PIPE,
            stdout=1
        )
        tee_err = subprocess.Popen(
            ["tee", "-a", stderr_path],
            start_new_session=True,
            stdin=subprocess.PIPE,
            stdout=2
        )

        os.dup2(tee_out.stdin.fileno(), original_stdout_fd)
        os.dup2(tee_err.stdin.fileno(), original_stderr_fd)

        capture_result = {
            "stdout": "",
            "stderr": "",
        }

        try:
            yield capture_result
        except Exception as e:
            sys.stderr.write(traceback.format_exc())
            raise e
        finally:
            sys.stdout.flush()
            sys.stderr.flush()

            tee_out.stdin.close()
            tee_err.stdin.close()

            os.dup2(saved_stdout_fd, original_stdout_fd)
            os.dup2(saved_stderr_fd, original_stderr_fd)

            tee_out.wait(timeout=1)
            tee_err.wait(timeout=1)

            os.close(saved_stdout_fd)
            os.close(saved_stderr_fd)

            with open(stdout_path) as f:
                capture_result["stdout"] = f.read()

            with open(stderr_path) as f:
                capture_result["stderr"] = f.read()
