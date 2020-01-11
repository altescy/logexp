from __future__ import annotations
import typing as tp

import dataclasses
import numbers
from collections import defaultdict


@dataclasses.dataclass
class Metric:
    value: numbers.Number
    step: int


class Metrics:
    def __init__(self) -> None:
        self._metrics: tp.Dict[str, tp.List[Metric]] = defaultdict(list)

    def add(self, key: str, value: tp.Any, step: int) -> None:
        metric = Metric(value, step)
        self._metrics[key].append(metric)

    def __getitem__(self, key: str) -> tp.List[Metric]:
        metrics = self._metrics[key]
        return sorted(metrics, key=lambda x: x.step)

    def to_json(self):
        return {
            key: [dataclasses.asdict(x) for x in metrics]
            for key, metrics in self._metrics
        }
