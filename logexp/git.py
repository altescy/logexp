from __future__ import annotations
import typing as tp

import dataclasses
import hashlib
import subprocess

from logexp import error


@dataclasses.dataclass
class GitInfo:
    version: str
    state: str
    head: str
    diff: tp.Optional[str]

    def to_json(self) -> tp.Dict[str, tp.Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_json(cls, git_dict: tp.Dict[str, tp.Any]) -> GitInfo:
        return GitInfo(**git_dict)


def _check_git_command() -> None:
    try:
        subprocess.check_call(["git", "--help"],
                              stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        raise error.GitCommandNotFoundError


def _check_git_repository() -> None:
    try:
        subprocess.check_call(["git", "status"],
                              stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise error.GitRepositoryNotFoundError


def _git_version() -> str:
    version: str = subprocess.check_output(["git", "--version"]).decode().strip()
    return version


def _git_head() -> str:
    head: str = subprocess.check_output(
        ["git", "log", "-n", "1", "--format=%H"]).decode().strip()
    return head


def _git_diff() -> str:
    diff: str = subprocess.check_output(["git", "diff"]).decode().strip()
    return diff


def get_git_info() -> GitInfo:
    _check_git_command()
    _check_git_repository()

    version = _git_version()
    head = _git_head()
    diff = _git_diff()
    state = hashlib.md5(f"{head}:{diff}".encode()).hexdigest()

    info = GitInfo(
        version=version,
        state=state,
        head=_git_head(),
        diff=diff if diff else None
    )
    return info
