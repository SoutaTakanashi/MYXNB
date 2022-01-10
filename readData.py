from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image

def loader1(path):
    return Image.open(path).convert('L')

class MyDataset(Dataset):

    # txt here is file path. Will be an incoming value when generating Data loader.
    def __init__(self, txt, transform, target_transform=None, loader=loader1):
        file = open(txt, 'r')
        imgInfo = []
        for line in file:
            line = line.strip('\n')
            line = line.rstrip()  # remove blank space.
            words = line.split()  # path | label

            imgInfo.append((words[0], int(words[1]))) # (address,label)
        self.imgInfo = imgInfo
        self.transform = transform
        self.target_transform = target_transform
        self.loader = loader

    # train_loader里面的
    def __getitem__(self, index):
        pth, label = self.imgInfo[index]   # path and label of a image.
        img = self.loader(pth)  # Use function loader1(path) to read image.

        if self.transform is not None:
            imgTensor = self.transform(img)  # Convert to FloatTensor type.

        return imgTensor, label

    def __len__(self):
        return len(self.imgInfo)


def generate_loader():
    transform = transforms.Compose([

        #Data Augumentation
        transforms.RandomRotation(15),
        # Random rotation: From -15° to 15°
        transforms.ToTensor(),
        transforms.RandomRotation(90)])
    print("Reading train_data...")
    train_data = MyDataset(txt='train.txt', transform=transform)
    # from torch.utils.data import Dataset, DataLoader
    train_loader = DataLoader(dataset=train_data, batch_size=50, shuffle=True)
    print("Reading test_data...")
    test_data = MyDataset(txt='test.txt', transform=transform)
    test_loader = DataLoader(dataset=test_data, batch_size=50, shuffle=False)
    return (train_loader,test_loader)