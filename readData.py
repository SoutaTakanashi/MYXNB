from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image

def default_loader(path):
    return Image.open(path).convert('L')


class MyDataset(Dataset):
    # txt是路径和文件名
    def __init__(self, txt, transform=transforms.ToTensor(), target_transform=None, loader=default_loader):
        fh = open(txt, 'r')  # 只读打开
        imgs = []
        for line in fh:
            line = line.strip('\n')  # 删除 回车
            line = line.rstrip()  # 删除 右侧 空格
            words = line.split()  # 分割：就两列，0列是路径 1列是标号

            imgs.append((words[0], int(words[1]))) # (address,label)
        self.imgs = imgs
        self.transform = transform
        self.target_transform = target_transform
        self.loader = loader  # 是个函数

    # train_loader里面的
    def __getitem__(self, index):
        fn, label = self.imgs[index]   # fn是完整路径 label是标号
        img = self.loader(fn)  # 调用上面的default_loader(path) 按照路径读取图片
        if self.transform is not None:
            img = self.transform(img)  # 将图片转换成FloatTensor类型
        return img, label

    def __len__(self):
        return len(self.imgs)

def generate_loader():
    print("Reading train_data...")
    train_data = MyDataset(txt='train.txt', transform=transforms.ToTensor())
    # from torch.utils.data import Dataset, DataLoader 下面的函数在这里
    train_loader = DataLoader(dataset=train_data, batch_size=50, shuffle=True)
    print("Reading test_data...")
    test_data = MyDataset(txt='test.txt', transform=transforms.ToTensor())
    test_loader = DataLoader(dataset=test_data, batch_size=50, shuffle=False)
    return (train_loader,test_loader)