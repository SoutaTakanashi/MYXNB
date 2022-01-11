import tkinter as tk
from tkinter import filedialog
from PyQt5.Qt import QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QApplication,QListWidget,QMessageBox
from PyQt5.QtGui import QPixmap,QIcon
import torch
from PIL import Image,ImageOps,ImageEnhance
import CNN_Model
from torchvision import transforms
import matplotlib.pyplot as plt
class MainWidget(QWidget):

    def __init__(self, Parent=None):

        super().__init__(Parent)
        self.filePath=''
        self.img=''
        self.setFixedSize(640, 480)
        self.setWindowTitle("Digit Prediction")
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
        self.lbl.setPixmap(QPixmap(self.filePath))
        sub_layout2.addWidget(self.lbl)

        self.listFile = QListWidget()
        self.listFile.setFixedSize(200, 280)
        sub_layout2.addWidget(self.listFile)

        main_layout.addLayout(sub_layout2)  # 将子布局加入主布局

    def Quit(self):
        self.close()

    def getPhoto(self):
        QApplication.processEvents()
        root = tk.Tk()
        root.withdraw()
        # Return the path of photo.
        file = filedialog.askopenfilename(filetypes=[('jpg','*.jpg'),('png','*.png'),('bmp','*.bmp')])
        if not file=='':
            self.filePath = file
            print("Selected:", self.filePath)
            self.img = Image.open(self.filePath)
            self.lbl.setPixmap(QPixmap(self.filePath))
            self.lbl.setScaledContents(True)
            QApplication.processEvents()
        #Else nothing will happen.(If no file selected.)

    def pred(self):

        path=self.filePath
        if path=='':
            msg_box=QMessageBox(QMessageBox.Information,'Error','Empty file path!')
            msg_box.setWindowIcon(QIcon('dark souls.png'))
            msg_box.exec_()
        else:
            self.listFile.addItem("Loading...")
            QApplication.processEvents()
            img = Image.open(path).convert('L')

            #Image Enhance:Brightness & Sharpness
            enh_bri = ImageEnhance.Brightness(img)
            img = enh_bri.enhance(factor=2)
            enh_sha = ImageEnhance.Sharpness(img)
            img = enh_sha.enhance(factor=1.5)
            width, height = img.size

            # Data Augumentation: Binarization
            #Pixel > threshold -> White(255) else Black(0)
            threshold = 115
            for w in range(width):
                for h in range(height):
                    if img.getpixel((w, h)) > threshold:
                        img.putpixel((w, h), 255)
                    else:
                        img.putpixel((w, h), 0)

            # plt.imshow(img)
            # plt.show()

            def blackOrWhiteBased(image, wid, hei):
                countWhite = 0
                countBlack = 0
                #Calculate the number of white(255) and black(0) pixels.
                #If white is more than black then it is a white based paper.
                #Vise versa.
                for w in range(wid):
                    for h in range(hei):
                        if image.getpixel((w, h)) == 255:
                            countWhite += 1
                        else:
                            countBlack += 1
                if countWhite > countBlack:
                    return 0
                else:
                    return 1

            if blackOrWhiteBased(img, width, height) == 0:
                # If the picture is considered a white based with words in black.
                #Reverse the color.
                img = ImageOps.invert(img).convert('L')

            def enlargeDigit(image, wid, hei):

                horizontal = []
                vertical = []
                #Get the range of character on picture.
                for w in range(wid):
                    for h in range(hei):
                        if image.getpixel((w, h)) == 255:
                            horizontal.append(w)
                            vertical.append(h)

                north = min(vertical)
                south = max(vertical)
                west = min(horizontal)
                east = max(horizontal)
                #Crop the picture to enlarge the picture in order to better recognize the character.
                return image.crop((int(west / 2), int(north / 2), int((wid + east) / 2), int((height + south) / 2)))

            if width > 100:
                img = enlargeDigit(img, width, height)
                width, height = img.size
            if width > 100:
                img = enlargeDigit(img, width, height)

            resize = transforms.Resize([28, 28])
            testData = resize(img)

            transform = transforms.ToTensor()
            testData = transform(testData)

            # print(testData[0])
            #Load the model. Then send the data to model for prediction.
            model = torch.load('model/net.pkl')
            testData = testData.unsqueeze(0).unsqueeze(0)
            result = CNN_Model.testSingle(model, testData)
            outline = 'the prediction is '
            self.listFile.addItem(outline + str(result))
