Train scikit-learn SVC model with logexp
===


### 1. init experiment

```
$ logexp init -e sklearn-iris
experiment id: 0
```


### 2. edit params

```
$ logexp params -e sklearn-iris -w train-svc > params.json
$ cat params.json  # edit params.json if you need
{
  "svc_params": {
    "C": 1.0,
    "kernel": "rbf"
  },
  "test_size": 0.3
}
```

### 3. run worker

```
$ logexp run -e 0 -w train-svc -p params.json
INFO - 01/18/20 15:34:21 - 0:00:00 - load iris dataset
INFO - 01/18/20 15:34:21 - 0:00:00 - dataset size: train=105, valid=45
INFO - 01/18/20 15:34:21 - 0:00:00 - start training
INFO - 01/18/20 15:34:21 - 0:00:00 - end training

** WORKER REPORT **
{
  "train_size": 105,
  "valid_size": 45,
  "train_accuracy": 0.9714285714285714,
  "valid_accuracy": 0.9777777777777777
}

** SUMMARY **
  run_id     : 82cb27bd78384498b683375f5c7f41ef
  name       :
  module     : iris
  experiment : sklearn-iris
  worker     : train-svc
  status     : finished
  artifacts  : {'rootdir': '/work/examples/scikit-learn/.logexp/0/train-svc/82cb27bd78384498b683375f5c7f41ef/artifacts'}
  start_time : 2020-01-18 15:34:21.925937
  end_time   : 2020-01-18 15:34:21.941321
```

### 4. try other params

Do your experiment.


### 5. list up your runs

```
$ logexp list -e 0 --sort end_time --desc
run_id                           name exp_id exp_name     worker    status   start_time          end_time            note
================================ ==== ====== ============ ========= ======== =================== =================== ====
82cb27bd78384498b683375f5c7f41ef      0      sklearn-iris train-svc finished 2020-01-18 15:34:21 2020-01-18 15:34:21
f5e4ad901a344e289e510f111c4d131c      0      sklearn-iris train-svc finished 2020-01-18 15:17:07 2020-01-18 15:17:07
a8d98715d4c44ed09039175e8ba05286      0      sklearn-iris train-svc finished 2020-01-18 15:10:50 2020-01-18 15:10:50
cee07b00e0334279ac0277b5aac772be      0      sklearn-iris train-svc finished 2020-01-18 15:02:47 2020-01-18 15:02:47
```

### 6. search the best run with [`jq`](https://stedolan.github.io/jq/)

`logexp logs` command exports all runs with JSON format.
You can search the output by using `jq`.

```
$ logexp logs -e 0 | jq '
  map(select(.status == "finished"))
    | sort_by(.report.valid_accuracy)
    | reverse
    | .[]
    | {run_id: .uuid, valid_accuracy: .report.valid_accuracy}'
{
  "run_id": "f5e4ad901a344e289e510f111c4d131c",
  "valid_accuracy": 1
}
{
  "run_id": "82cb27bd78384498b683375f5c7f41ef",
  "valid_accuracy": 0.9777777777777777
}
{
  "run_id": "cee07b00e0334279ac0277b5aac772be",
  "valid_accuracy": 0.9333333333333333
}
{
  "run_id": "a8d98715d4c44ed09039175e8ba05286",
  "valid_accuracy": 0.9111111111111111
}
```
