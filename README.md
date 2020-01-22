# logexp
[![Actions Status](https://github.com/altescy/logexp/workflows/logexp/badge.svg)](https://github.com/altescy/logexp)
[![Python version](https://img.shields.io/pypi/pyversions/logexp)](https://github.com/altescy/logexp)
[![pypi version](https://img.shields.io/pypi/v/logexp)](https://pypi.org/project/logexp/)
[![license](https://img.shields.io/github/license/altescy/logexp)](https://github.com/altescy/logexp/blob/master/LICENSE)

## Quick Links

- [Installation](#Installation)
- [Tutorial](#Tutorial)
- [scikit-learn example](https://github.com/altescy/logexp/tree/master/examples/scikit-learn)


## Introduction

`logexp` is a simple experiment manager for machine learning.
You can manage your experiments and executions from command line interface.

- Features
  - **track experiments**: `logexp` tracks experiments and environment.
  - **manage parameters**: Import / export worker parameters with JSON format.
  - **capture stdout / stderr**: Capture stdout / stderr during execution automatically.
  - **search logs**: You can search your runs with [`jq`](https://stedolan.github.io/jq/) command.
  - **written in pure Python**: `logexp` has no external dependencies.


## Installation

Installing the library is simple using `pip`.
```
pip install logexp
```

## Tutorial

In this tutorial we'll implement a simple worker for machine learning with [`scikit-learn`](https://scikit-learn.org/).
And then, let me introduce some operations to manage experiments and executions.

### 1. Create worker

This worker trains `RandomForestClassifier` and saves a trained model.

Worker needs to inherit `logexp.BaseWorker`.
In `config` method, you can define worker parameters, that are logged automatically.
Write your task in `run` method, and return `logexp.Report` which describes quick result if you need.

`BaseWorker.storage` is an artifact storage.
You can save any files by using this storage.

```
$ cat << EOF > iris.py
import logexp
import numpy as np
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

ex = logexp.Experiment("sklearn-iris")

@ex.worker("train-rfc")
class TrainRandomForest(logexp.BaseWorker):
    def config(self):
        self.rfc_params = {
            "n_estimators": 100,
            "min_samples_leaf": 1,
            "random_state": 0,
        }
        self.test_size = 0.3
        self.random_seed = 0

    def run(self):
        np.random.seed(self.random_seed)

        iris = load_iris()
        X, y = iris.data, iris.target

        X_train, X_valid, y_train, y_valid = \
            train_test_split(X, y, test_size=self.test_size)

        model = RandomForestClassifier(**self.rfc_params)
        model.fit(X_train, y_train)

        with self.storage.open("rfc.pkl", "wb") as f:
            pickle.dump(model, f)

        train_accuracy = model.score(X_train, y_train)
        valid_accuracy = model.score(X_valid, y_valid)

        report = logexp.Report()
        report["train_size"] = len(X_train)
        report["valid_size"] = len(X_valid)
        report["train_accuracy"] = train_accuracy
        report["valid_accuracy"] = valid_accuracy

        return report
EOF
```


### 2. Initialize experiment

Following command creates log-store directory (`./.logexp` by default) and returns `experiment_id`.

```
$ logexp init -m iris -e sklearn-iris
experiment id: 0
```


### 3. Edit parameters

Export default parameters with JSON format via:
```
$ logexp params -m iris -e sklearn-iris -w train-rfc > params.json
$ cat params.json
{
  "rfc_params": {
    "n_estimators": 100,
    "min_samples_leaf": 1,
    "random_state": 0
  },
  "test_size": 0.3,
  "random_seed": 0
}
```

You can also export params from specified run:

```
$ logexp params -r [ RUN_ID ]
```

Edit `params.json` file if you need.


### 4. Run worker

Run worker via `$ logexp run` command and see quick result like bellow:

```
$ logexp run -m iris -e 0 -w train-rfc -p params.json
** WORKER REPORT **
{
  "train_size": 105,
  "valid_size": 45,
  "train_accuracy": 1.0,
  "valid_accuracy": 0.9777777777777777
}

** SUMMARY **
run_id     : 7fcd37ef38104715ad60bd55b7e1023d
name       :
module     : iris
experiment : sklearn-iris
worker     : train-rfc
status     : finished
artifacts  : {'rootdir': '/src/.logexp/0/train-rfc/7fcd37ef38104715ad60bd55b7e1023d/artifacts'}
start_time : 2020-01-19 05:14:05.246681
end_time   : 2020-01-19 05:14:05.430199
```

### 5. View logs

Following command lists up executions:

```
$ logexp list -e 0 --sort start_time
run_id                           name exp_id exp_name     worker    status   start_time          end_time            note
================================ ==== ====== ============ ========= ======== =================== =================== ====
7fcd37ef38104715ad60bd55b7e1023d      0      sklearn-iris train-rfc finished 2020-01-19 05:14:05 2020-01-19 05:14:05
5300f7fc32b949bba6775c5899e09ae9      0      sklearn-iris train-rfc finished 2020-01-19 05:44:04 2020-01-19 05:44:04
```

`$ logexp logs` command exports all logs with JSON format.
Using [`jq`](https://stedolan.github.io/jq/) command, you can do more complex search.

```
$ logexp logs -e 0 | jq '
  map(select(.status == "finished"))
    | sort_by(.report.valid_accuracy)
    | reverse
    | .[]
    | {run_id: .uuid, valid_accuracy: .report.valid_accuracy}'
{
  "run_id": "7fcd37ef38104715ad60bd55b7e1023d",
  "valid_accuracy": 0.9777777777777777
}
{
  "run_id": "5300f7fc32b949bba6775c5899e09ae9",
  "valid_accuracy": 0.9555555555555556
}
```
