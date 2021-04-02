#!/usr/bin/python3
#coding:utf-8
from PyQt5.Qt import QWidget, QColor, QPixmap, QIcon, QSize, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSplitter,\
    QComboBox, QLabel, QSpinBox, QFileDialog,QMessageBox,QInputDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt,QTimer
import sys
from CamWin import CamWin
from PicWin import PicWin
import time
import os
import cv2
import rospy

class MainWidget(QWidget):
    
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.__InitData()
        self.__InitView()
        self.__InitRos()
    
    def __InitRos(self):
        
        rospy.init_node('screen_node')
        self.rospy_rate = 20
        self.rate = rospy.Rate(self.rospy_rate)
        
    def __InitData(self):
        self.__CamWin = CamWin(self)
        self.__PicWin = PicWin(self)
        
        self.__package_path = rospy.get_param('/pkg_path/screen')
        


    def __InitView(self):
        '''
                  初始化界面
        '''
        self.setFixedSize(1500,900)
        self.setWindowTitle("垃圾自动分类装置")
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)

        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0,0,0,0)
        top_layout.addWidget(self.__CamWin)
        top_layout.addWidget(self.__PicWin)
        main_layout.addLayout(top_layout)

def main():
    app = QApplication(sys.argv) # sys.argv即命令行参数
    mainWidget = MainWidget() #新建一个主界面
    mainWidget.show()	#显示主界面
    exit(app.exec_()) #进入消息循环

if __name__ == '__main__':
    main()
