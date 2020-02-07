Train a scikit-learn model with logexp
===

### Dependencies

- [logexp](https://github.com/altescy/logexp)
- [sklearn](https://scikit-learn.org/)
- [colt](https://github.com/altescy/colt)


### `logexp` Configuration File

You can define your `logexp` settings in `logexp.ini`.

```
[logexp]
module=iris
```

In this case, a default module will be set as `iris`,
so you don't need to specify the module when execute commands:

```
$ logexp init -e sklearn-iris   # not need `-m iris`
```
