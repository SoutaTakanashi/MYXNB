import torch.nn
import torch.optim as optim
import torch
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Sequential(  # (1,28,28)
            # conv2d(in_channels,out_channels,kernelsize,stride,padding)
            torch.nn.Conv2d(1, 16, 5, 1, 2),  # (16,28,28)
            # To make the size of conv2d's output  unchanged: padding=(kernel_size-1)/2
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)  # (16,14,14)
        )
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv2d(16, 64, 3),  # (64,12,12)
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)  # (64,6,6)
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv2d(64, 64, 3),  # (64,4,4)
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)  # (64,2,2)
        )
        self.fc = torch.nn.Linear(256, 10)
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = x.view(x.size(0), -1)  # Flat（batch，64,2,2）to（batch，256）
        x = self.fc(x)
        return x

def giveModel():
    model = Net()
    # construct loss and optimizer
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)
    return (model,criterion,optimizer)

def train(epoch,model,criterion,optimizer,train_loader):
    running_loss = 0.0
    for batch_idx, data in enumerate(train_loader, 0):
        #batch_idx:batch number
        #data:(x,y)
        inputs, target = data
        optimizer.zero_grad()#Zeroing out the gradient
        pred_outputs = model(inputs)#Possibility of
        loss = criterion(pred_outputs, target)#Calculate cross entropy.(Loss function)
        loss.backward()#Back propagation to calculate the gradient value of each parameter
        optimizer.step()#Performing parameter updates via gradient descent
        running_loss += loss.item()
        if batch_idx % 300 == 299:
            # Print the loss every 300 batches in a single epoch.
            print('[%d, %5d] loss: %.3f' % (epoch+1, batch_idx+1, running_loss/300))
            running_loss = 0.0


def test(model,test_loader):
    sum = 0
    total = 0
    with torch.no_grad():
        for data in test_loader:
            images, labels = data
            outputs = model(images)
            _, predicted = torch.max(outputs.data, dim=1)
            total += labels.size(0)
            sum += (predicted == labels).sum().item()
    print('accuracy on test set: %d %% ' % (100*sum/total))

def testSingle(model,data_loader):
    with torch.no_grad():
        for data in data_loader:
            outputs = model(data)
            _, predicted = torch.max(outputs.data, dim=1)
            #print(outputs)
    return predicted.item()
