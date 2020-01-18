from __future__ import annotations
import typing as tp

from logexp.utils.jsondict import JsonDict


class Report(JsonDict):
    """worker report"""

    @classmethod
    def from_json(cls, params_dict: tp.Dict[str, tp.Any]) -> Report:
        # pylint: disable=arguments-differ
        return Report(params_dict)
