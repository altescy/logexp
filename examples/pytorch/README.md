PyTorch: MNIST and TensorboardX
===


### Dependencies

- logexp
- torch
- torchvision
- tensorboardX



### Commands

```
$ logexp init -e pytorch-mnist
$ logexp run -e 0 -w train-mnist
$ tensorboard --logdir=`logexp show -r [ RUN_ID ] | jq .storage.rootdir -r`
```

![Screenshot from 2020-02-08 23-06-59](https://user-images.githubusercontent.com/16734471/74086613-cd356f80-4ac7-11ea-8c53-696eeaff4426.png)
