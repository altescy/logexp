import logexp
import torch
import torch.nn.functional as F
from torchvision import datasets, transforms
from tensorboardX import SummaryWriter


ex = logexp.Experiment("pytorch-mnist")


class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = torch.nn.Dropout2d()
        self.fc1 = torch.nn.Linear(320, 50)
        self.fc2 = torch.nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=0)


@ex.worker("train-mnist")
class TranMnist(logexp.BaseWorker):
    def config(self):
        self.data_directory = "./data"

        self.batch_size = 64
        self.test_batch_size = 1000
        self.sgd_optimizer = {
            "lr": 0.01,
            "momentum": 0.5,
        }
        self.epochs = 10
        self.cuda = False

        self.log_interval = 100

    def run(self):
        self.writer = SummaryWriter(self.storage.rootdir)

        self._prepare_dataset()

        self.model = Net()
        if self.cuda:
            self.model.cuda()

        self.optimizer = torch.optim.SGD(self.model.parameters(), **self.sgd_optimizer)

        for epoch in range(1, self.epochs + 1):
            self._train(epoch)
            self._test(epoch)

    def _prepare_dataset(self):
        kwargs = {'num_workers': 1, 'pin_memory': True} if self.cuda else {}
        self.train_loader = torch.utils.data.DataLoader(
            datasets.MNIST(self.data_directory, train=True, download=True,
                           transform=transforms.Compose([
                               transforms.ToTensor(),
                               transforms.Normalize((0.1307,), (0.3081,))
                           ])),
            batch_size=self.batch_size, shuffle=True, **kwargs)
        self.test_loader = torch.utils.data.DataLoader(
            datasets.MNIST(self.data_directory, train=False,
                           transform=transforms.Compose([
                               transforms.ToTensor(),
                               transforms.Normalize((0.1307,), (0.3081,))
                           ])),
            batch_size=self.test_batch_size, shuffle=True, **kwargs)

    def _log_weights(self, step):
        self.writer.add_histogram('weights/conv1/weight', self.model.conv1.weight.data, step)
        self.writer.add_histogram('weights/conv1/bias', self.model.conv1.bias.data, step)
        self.writer.add_histogram('weights/conv2/weight', self.model.conv2.weight.data, step)
        self.writer.add_histogram('weights/conv2/bias', self.model.conv2.bias.data, step)
        self.writer.add_histogram('weights/fc1/weight', self.model.fc1.weight.data, step)
        self.writer.add_histogram('weights/fc1/bias', self.model.fc1.bias.data, step)
        self.writer.add_histogram('weights/fc2/weight', self.model.fc2.weight.data, step)
        self.writer.add_histogram('weights/fc2/bias', self.model.fc2.bias.data, step)

    def _train(self, epoch):
        self.model.train()
        for batch_idx, (data, target) in enumerate(self.train_loader):
            if self.cuda:
                data, target = data.cuda(), target.cuda()
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            self.optimizer.step()
            if batch_idx % self.log_interval == 0:
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(self.train_loader.dataset),
                    100. * batch_idx / len(self.train_loader), loss.data.item()))
                step = epoch * len(self.train_loader) + batch_idx
                self.writer.add_scalar('train_loss', loss.data.item(), step)
                self._log_weights(step)

    def _test(self, epoch):
        self.model.eval()
        test_loss = 0
        correct = 0
        with torch.no_grad():
            for data, target in self.test_loader:
                if self.cuda:
                    data, target = data.cuda(), target.cuda()
                output = self.model(data)
                test_loss += F.nll_loss(output, target, reduction='sum').data.item() # sum up batch loss
                pred = output.data.max(1)[1] # get the index of the max log-probability
                correct += pred.eq(target.data).cpu().sum().item()

        test_loss /= len(self.test_loader.dataset)
        test_accuracy = 100.0 * correct / len(self.test_loader.dataset)
        print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
            test_loss, correct, len(self.test_loader.dataset), test_accuracy))
        step = (epoch + 1) * len(self.train_loader)
        self.writer.add_scalar('test_loss', test_loss, step)
        self.writer.add_scalar('test_accuracy', test_accuracy, step)
