from __future__ import annotations
import typing as tp


class Params:
    def __init__(self, params: tp.Dict[str, tp.Any] = None) -> None:
        self._params: tp.Dict[str, tp.Any] = params or {}

    def __setitem__(self, key: str, val: tp.Any) -> None:
        if not isinstance(key, str):
            raise TypeError(f"key must be str: {type(key)}")

        self._params[key] = val

    def __getitem__(self, key: str) -> tp.Any:
        return self._params[key]

    def __delitem__(self, key: str):
        del self._params[key]

    def __iter__(self) -> tp.Iterator[str]:
        return iter(self._params)

    def __len__(self) -> int:
        return len(self._params)

    def items(self) -> tp.ItemsView[str, tp.Any]:
        return self._params.items()

    def to_json(self) -> tp.Dict[str, tp.Any]:
        return self._params

    @classmethod
    def from_json(cls, params_dict: tp.Dict[str, tp.Any]):
        return Params(params_dict)
