from __future__ import annotations
import typing as tp

import json


class JsonDict:
    def __init__(self, init_dict: tp.Dict[str, tp.Any] = None) -> None:
        self._dict: tp.Dict[str, tp.Any] = {}

        if init_dict is not None:
            for key, val in init_dict.items():
                self.__setitem__(key, val)

    def __setitem__(self, key: str, val: tp.Any) -> None:
        if not isinstance(key, str):
            raise TypeError(f"key must be str: {type(key)}")
        _ = json.dumps(val)

        self._dict[key] = val

    def __getitem__(self, key: str) -> tp.Any:
        return self._dict[key]

    def __delitem__(self, key: str):
        del self._dict[key]

    def __iter__(self) -> tp.Iterator[str]:
        return iter(self._dict)

    def __len__(self) -> int:
        return len(self._dict)

    def items(self) -> tp.ItemsView[str, tp.Any]:
        return self._dict.items()

    def to_json(self) -> tp.Dict[str, tp.Any]:
        return self._dict

    @classmethod
    def from_json(cls, jsondict: tp.Dict[str, tp.Any]) -> JsonDict:
        return cls(jsondict)
