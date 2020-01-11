from __future__ import annotations

import enum


class Status(enum.Enum):
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"
    INTERRUPTED = "interrupted"
