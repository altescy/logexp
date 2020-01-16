from __future__ import annotations
import typing as tp

import dataclasses
import platform


@dataclasses.dataclass
class PlatformInfo:
    system: str
    node: str
    release: str
    version: str
    machine: str
    processor: str
    python_version: str

    def to_json(self) -> tp.Dict[str, tp.Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_json(cls, platform_dict: tp.Dict[str, tp.Any]) -> PlatformInfo:
        return PlatformInfo(**platform_dict)


def get_platform_info() -> PlatformInfo:
    info = PlatformInfo(system=platform.system(),
                        node=platform.node(),
                        release=platform.release(),
                        version=platform.version(),
                        machine=platform.machine(),
                        processor=platform.processor(),
                        python_version=platform.python_version())
    return info
