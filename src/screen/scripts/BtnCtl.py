from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QHBoxLayout, QVBoxLayout,QGridLayout
from PyQt5.Qt import QSize,QPixmap
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import *


class BtnCtl(QWidget):
    def __init__(self, btn_CH_name,btn_EN_name,Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)

        self.__InitData(btn_CH_name,btn_EN_name) #先初始化数据，再初始化界面
        self.__InitView()
        
    def __InitData(self,btn_CH_name,btn_EN_name):
        
        self.__size = QSize(650,300)
        self.btn_CH_name = btn_CH_name
        self.btn_EN_name = btn_EN_name

     
    def __InitView(self):
        #设置界面的尺寸为__size
        self.setFixedSize(self.__size)

        self.btn_grid=QGridLayout(self)

        self.btn_position = [(i,j) for i in range(4) for j in range(3)]
        self.btn_list = []

        for position,name in zip(self.btn_position,self.btn_CH_name):
            btn = QPushButton(name)
            btn.setMinimumHeight(90)
            btn.setStyleSheet("font-size:30px")
            self.btn_list.append(btn)

            self.btn_grid.addWidget(btn,position[0],position[1])

        self.btn_dict = dict(zip(self.btn_EN_name,self.btn_list))


    def change_btn_text(self,btn_name,text):
        self.btn_dict[btn_name].setText(text)


        
        
