import os
from skimage import io
import torchvision.datasets.mnist as mnist
import torch

def flip(x, dim):
    indices = [slice(None)] * x.dim()
    indices[dim] = torch.arange(x.size(dim) - 1, -1, -1,
                                dtype=torch.long, device=x.device)
    return x[tuple(indices)]
# read the emnist dataset
train_set = (
mnist.read_image_file('./dataset/emnist-mnist-train-images-idx3-ubyte/emnist-mnist-train-images-idx3-ubyte'),
mnist.read_label_file('./dataset/emnist-mnist-train-labels-idx1-ubyte/emnist-mnist-train-labels-idx1-ubyte')
)
test_set = (
mnist.read_image_file('./dataset/emnist-mnist-train-images-idx3-ubyte/emnist-mnist-train-images-idx3-ubyte'),
mnist.read_label_file('./dataset/emnist-mnist-train-labels-idx1-ubyte/emnist-mnist-train-labels-idx1-ubyte')
)
#They are in 'tensor' type.

#print(train_set[0][1].shape)
def save_as_images(mode=1):  # mode 1:Train, else: Test.

    if mode == 1:  # 如果是训练数据
        f = open('train.txt', 'w')
        data_path = 'train/'  # 好像可以删去左边的/
        # Create if does not exist.
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        for i, (img, label) in enumerate(zip(train_set[0], train_set[1])):
            img_path = data_path + str(i) + '.jpg'
            # Save the images to local directory.
            io.imsave(img_path, (flip(img, -2)))
            # 保存标号文件路径和标号
            f.write(img_path + ' ' + str(label.item()) + '\n')

        f.close()
    else:
        f = open('test.txt', 'w')
        data_path = 'test/'
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        for i, (img, label) in enumerate(zip(test_set[0], test_set[1])):
            img_path = data_path + str(i) + '.jpg'
            io.imsave(img_path, (flip(img, -2)))
            f.write(img_path + ' ' + str(label.item()) + '\n')
        f.close()

def convert():
    if os.path.exists('train'):  # 如果目录不存在就返回False
        print("Pictures(train) already converted.")

    else:

        print("Building training set...")
        save_as_images(1)
        print("Image conversion accomplished! Long may the sunshine!")

    if os.path.exists('test'):  # 如果目录不存在就返回False
        print("Pictures(test) already converted.")
    else:
        print("Building test set...")
        save_as_images(2)
        print("Image conversion accomplished! Long may the sunshine!")

