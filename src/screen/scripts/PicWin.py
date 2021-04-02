from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.Qt import QSize,QPixmap
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import *
import cv2
import rospy
import os
class PicWin(QWidget):
    def __init__(self,Parent=None):
        super().__init__(Parent)

        self.__InitData()
        self.__InitView()
        
    def __InitData(self):
        
        self.__size = QSize(600,450)
        self.pkg_path = rospy.get_param("/pkg_path/screen")
        self.pic_path = os.path.join(self.pkg_path,"pic")

        self.create_pic_list()
        self.lock = False
        
        self.curve_paint_timer = QTimer(self)
        self.curve_paint_timer.timeout.connect(self.update_pic)
        self.curve_paint_timer.start(2000)
     
    def __InitView(self):
        #设置界面的尺寸为__size
        self.setFixedSize(self.__size)
        self.show_label =  QLabel(self)
        self.show_label.setFixedSize(self.__size)
        
        self.show_label.setAlignment(Qt.AlignCenter)

    def create_pic_list(self):
        self.pic_list = []
        self.pic_index = 0
        for pic in os.listdir(self.pic_path):
            frame = cv2.imread(os.path.join(self.pic_path,pic))
            cv2.cvtColor(frame,cv2.COLOR_BGR2RGB,frame)
            self.pic_list.append(frame)


    def update_pic(self):
        if self.lock == False:
            self.lock = True
            self.frame = self.pic_list[self.pic_index]
            self.pic_index += 1
            self.pic_index %= len(self.pic_list)
            img_rows,img_cols,channels = self.frame.shape
            bytesPerLine = channels * img_cols
            QImg = QImage(self.frame.data,img_cols,img_rows,bytesPerLine,QImage.Format_RGB888)
            self.show_label.setStyleSheet('background-color: rgb(0, 0, 0)')
            self.show_label.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.show_label.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation
            ))
            self.lock = False