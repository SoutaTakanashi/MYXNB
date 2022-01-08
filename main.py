import os
import sys
import dataProcess
import readData
import CNN_Model
import torch

from FileExe import MainWidget
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    print("Please choose your opreation:\n 1:Training 2:Read local picture and predict.")
    mode=input("Enter Number:")
    if mode==1:
        print("Now processing raw dataset...")
        dataProcess.convert()
        print("Generating data loaders...")
        train_loader, test_loader = readData.generate_loader()
        print("Loading Our Model...")
        model, criterion, optimizer = CNN_Model.giveModel()
        print("Model Loaded")

        print("Training Model...")
        for epoch in range(10):
            CNN_Model.train(epoch, model, criterion, optimizer, train_loader)
            CNN_Model.test(model, test_loader)
            if epoch % 2 == 0:
                if not os.path.exists('./model/'):
                    os.makedirs('./model/')
                torch.save(model, './model/net.pkl')
    else:
        app = QApplication(sys.argv)

        mainWidget = MainWidget()  # 新建一个主界面
        mainWidget.show()  # 显示主界面

        exit(app.exec_())  # 进入消息循环



