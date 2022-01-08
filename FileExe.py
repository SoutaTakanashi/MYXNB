import tkinter as tk
from tkinter import filedialog
from PyQt5.Qt import QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout,QPushButton,QLabel
from PyQt5.QtGui import QPixmap
from PIL import Image,ImageQt
class MainWidget(QWidget):

    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)
        self.filePath=''

        self.setFixedSize(800, 800)
        self.setWindowTitle("MYXNB")

        # 新建一个水平布局作为本窗体的主布局
        main_layout = QHBoxLayout(self)
        # 设置主布局内边距以及控件间距为10px
        main_layout.setSpacing(10)

        # 新建垂直子布局用于放置按键
        sub_layout1 = QVBoxLayout()

        sub_layout1.setContentsMargins(10, 10, 10, 10)
        self.__btn_Quit = QPushButton("Quit")
        self.__btn_Quit.setParent(self)  # 设置父对象为本界面
        self.__btn_Quit.clicked.connect(self.Quit)
        sub_layout1.addWidget(self.__btn_Quit)

        self.__btn_GetPic = QPushButton("Get picture")
        self.__btn_GetPic.setParent(self)
        self.__btn_GetPic.clicked.connect(self.getPhoto)
        sub_layout1.addWidget(self.__btn_GetPic)

        lbl = QLabel()
        lbl.setParent(self)
        lbl.setPixmap(QPixmap(self.filePath))
        sub_layout1.addWidget(lbl)

        main_layout.addLayout(sub_layout1)  # 将子布局加入主布局
        """
         sub_layout2 = QVBoxLayout()
        self.__picLbl=QLabel("MAMMA MIA")
        self.__picLbl.setParent(self)
        self.__picLbl.show()
        self.pixmap=QPixmap(self.filePath)
        print(self.filePath)
        self.__picLbl.setPixmap(self.pixmap)
        self.__picLbl.setScaledContents(True)
        sub_layout2.addWidget(self.__picLbl)
        main_layout.addLayout(sub_layout2)
        """
    def Quit(self):
        self.close()

    def getPhoto(self):
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename(filetypes=[('jpg','*.jpg'),('png','*.png'),('bmp','*.bmp')])
        self.filePath = file
        print("Selected:", self.filePath)

        # Return the path of photo.


