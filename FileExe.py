import tkinter as tk
from tkinter import filedialog
from PyQt5.Qt import QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QApplication,QListWidget
from PyQt5.QtGui import QPixmap,QIcon
import torch
from PIL import Image,ImageOps,ImageFilter,ImageEnhance
import CNN_Model,dataProcess
from torchvision import transforms
import matplotlib.pyplot as plt
class MainWidget(QWidget):

    def __init__(self, Parent=None):

        super().__init__(Parent)
        self.filePath=''
        self.img=''
        self.setFixedSize(640, 480)
        self.setWindowTitle("Dark Souls III")
        self.setWindowIcon(QIcon('dark souls.png'))
        # Main layout.
        main_layout = QVBoxLayout(self)
        #Set distance between different widget to 10px
        main_layout.setSpacing(10)
        #New sub layout to place widgets.
        sub_layout1 = QHBoxLayout()

        sub_layout1.setContentsMargins(10, 10, 10, 10)

        self.btn_Quit = QPushButton("Quit")
        self.btn_Quit.clicked.connect(self.Quit)
        
        sub_layout1.addWidget(self.btn_Quit)

        self.btn_GetPic= QPushButton("Get picture")
        self.btn_GetPic.clicked.connect(self.getPhoto)
        sub_layout1.addWidget(self.btn_GetPic)

        self.btn_Pred= QPushButton("Predict")
        self.btn_Pred.clicked.connect(self.pred)
        sub_layout1.addWidget(self.btn_Pred)




        main_layout.addLayout(sub_layout1)

        sub_layout2 = QHBoxLayout()

        self.lbl = QLabel(self.filePath)
        self.lbl.setMaximumSize(280,280)
        # lbl.setParent(self)
        self.lbl.setPixmap(QPixmap(self.filePath))
        sub_layout2.addWidget(self.lbl)

        self.listFile = QListWidget()
        # self.listFile.move(410,30)
        self.listFile.setFixedSize(200, 280)
        sub_layout2.addWidget(self.listFile)


        main_layout.addLayout(sub_layout2)  # 将子布局加入主布局

    def Quit(self):
        self.close()

    def getPhoto(self):
        QApplication.processEvents()
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename(filetypes=[('jpg','*.jpg'),('png','*.png'),('bmp','*.bmp')])
        if not file=='':
            self.filePath = file
        else:
            exit()
        print("Selected:", self.filePath)
        self.img=Image.open(self.filePath)
        self.lbl.setPixmap(QPixmap(self.filePath))
        self.lbl.setScaledContents(True)
        QApplication.processEvents()
        # Return the path of photo.

    def pred(self):
        self.listFile.addItem("Loading...")
        QApplication.processEvents()
        path=self.filePath
        img = Image.open(path).convert('L')


        enh_bri = ImageEnhance.Brightness(img)
        img = enh_bri.enhance(factor=2)
        enh_sha = ImageEnhance.Sharpness(img)
        img = enh_sha.enhance(factor=1.5)
        width, height = img.size

        threshold = 115
        for w in range(width):#二值化
            for h in range(height):
                if img.getpixel((w, h)) > threshold:
                    img.putpixel((w, h), 255)
                else:
                    img.putpixel((w, h), 0)
        #plt.imshow(img)
        #plt.show()

        def blackOrWhiteBased(image,wid,hei):
            countWhite = 0
            countBlack = 0
            for w in range(wid):
                for h in range(hei):
                    if image.getpixel((w,h))==255:
                        countWhite+=1
                    else:
                        countBlack+=1
            if countWhite>countBlack:
                return 0
            else:
                return 1
        if blackOrWhiteBased(img,width,height)==0:#如果是白纸黑字
            img=ImageOps.invert(img).convert('L')

        def enlargeDigit(image,wid,hei):

            yoko=[]
            nao=[]
            for w in range(wid):
                for h in range(hei):
                    if image.getpixel((w,h))==255:
                        yoko.append(w)
                        nao.append(h)

            north=min(nao)
            south=max(nao)
            west=min(yoko)
            east=max(yoko)

            return image.crop((int(west / 2), int(north / 2), int((wid + east) / 2), int((height + south) / 2)))

        if width >100:
            img=enlargeDigit(img,width,height)
            width, height = img.size
        if width > 100:
            img=enlargeDigit(img,width,height)



        resize = transforms.Resize([28, 28])
        testData = resize(img)
        """
        
        
        width, height = testData.size
        
        threshold = 0.4
        for w in range(width):  # 二值化
            for h in range(height):
                if testData.getpixel((w, h)) > threshold:
                    testData.putpixel((w, h), 1)
                else:
                    testData.putpixel((w, h), 0)

        print("MYXNB!!!")
        plt.imshow(testData)
        plt.show()
        """
        transform = transforms.ToTensor()
        testData = transform(testData)

        #print(testData[0])
        model = torch.load('model/net.pkl')
        testData = testData.unsqueeze(0).unsqueeze(0)
        result = CNN_Model.testSingle(model, testData)
        outline = 'the prediction is '
        self.listFile.addItem(outline + str(result))
