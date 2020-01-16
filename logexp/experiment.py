from __future__ import annotations
import typing as tp

from collections import defaultdict

from logexp import error
from logexp.worker import BaseWorker


class Experiment:
    _experiments: tp.Dict[tp.Type, tp.Dict[str, "Experiment"]] = defaultdict(dict)

    @classmethod
    def set_experiment(cls, experiment: Experiment) -> None:
        Experiment._experiments[cls][experiment.name] = experiment

    @classmethod
    def get_experiment(cls, name: str) -> Experiment:
        experiment = Experiment._experiments[cls].get(name)

        if experiment is None:
            raise error.ExperimentNotFoundError

        return experiment

    def __init__(self, name: str) -> None:
        self._name = name
        self._workers: tp.Dict[str, tp.Type[BaseWorker]] = {}

        Experiment.set_experiment(self)

    def worker(self, name: str) -> tp.Callable:
        workers = self._workers

        def decorator(worker: tp.Type[BaseWorker]):
            if name in workers:
                message = (
                    "Cannot register {} as {}; "
                    "name already in use for {}"
                ).format(
                    worker.__name__, name, workers[name].__name__
                )
                raise ValueError(message)
            workers[name] = worker
            return worker

        return decorator

    def get_worker(self, name: str) -> BaseWorker:
        if name not in self._workers:
            raise error.WorkerNotFoundError
        return self._workers[name](name)

    @property
    def name(self) -> str:
        return self._name

    def to_json(self) -> tp.Dict[str, tp.Any]:
        expeirment_dict = {
            "name": self.name
        }
        return expeirment_dict

    @classmethod
    def from_json(cls, experiment_dict: tp.Dict[str, tp.Any]) -> Experiment:
        name = experiment_dict["name"]
        return Experiment.get_experiment(name)
