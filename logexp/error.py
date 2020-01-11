from __future__ import annotations

class ExperimentConflictError(Exception):
    """experiment conflict error"""


class ExperimentNotFoundError(Exception):
    """experiment not found error"""


class WorkerNotFoundError(Exception):
    """worker not found error"""



class GitError(Exception):
    """git error"""


class GitCommandNotFoundError(GitError):
    """git command not found error"""


class GitRepositoryNotFoundError(GitError):
    """git repository not found error"""
