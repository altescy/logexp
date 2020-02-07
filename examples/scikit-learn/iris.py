import typing as tp
import importlib

import colt
import logexp
import sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from logger import create_logger


logger = create_logger(__name__)
ex = logexp.Experiment("sklearn-iris")


@colt.register("sklearn-model")
class SklearnModelBuilder:
    def __init__(self, **kwargs) -> None:
        model_path = kwargs.pop("@model")
        self._model = self._get_model_from_sklearn(model_path)
        self._params = kwargs

    def get_model(self):
        return self._model(**self._params)

    @staticmethod
    def _get_model_from_sklearn(model_path: str) -> tp.Any:
        model_path = "sklearn." + model_path
        module_path, model_name = model_path.rsplit(".", 1)

        module = importlib.import_module(module_path)
        model = getattr(module, model_name)

        if isinstance(model, sklearn.base.BaseEstimator):
            raise ValueError(f"{model_path} is not an estimator.")

        return model


@ex.worker("sklearn-trainer")
class TrainSklearnModel(logexp.BaseWorker):
    def config(self):
        self.model = {
            "@type": "sklearn-model",
            "@model": "svm.SVC",
            "C": 1.0,
            "kernel": "rbf",
        }
        self.test_size = 0.3

    def run(self):
        logger.info("load iris dataset")

        iris = load_iris()
        X, y = iris.data, iris.target

        X_train, X_valid, y_train, y_valid = \
            train_test_split(X, y, test_size=self.test_size)

        logger.info(f"dataset size: train={len(X_train)}, valid={len(X_valid)}")

        model = colt.build(self.model).get_model()

        logger.info("start training")

        model.fit(X_train, y_train)

        logger.info("end training")

        train_accuracy = model.score(X_train, y_train)
        valid_accuracy = model.score(X_valid, y_valid)

        report = logexp.Report()
        report["train_size"] = len(X_train)
        report["valid_size"] = len(X_valid)
        report["train_accuracy"] = train_accuracy
        report["valid_accuracy"] = valid_accuracy

        return report
