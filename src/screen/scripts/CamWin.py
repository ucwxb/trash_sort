from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.Qt import QSize,QPixmap
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import *
import cv2
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
class CamWin(QWidget):
    def __init__(self,Parent=None):
        super().__init__(Parent)

        self.__InitData() #先初始化数据，再初始化界面
        self.__InitView()
        
    def __InitData(self):
        
        self.__size = QSize(600,450)
        self.isEnable_Cam = False
        self.before_Cam_status = False
        self.bridge = CvBridge()
        rospy.Subscriber("/gesture_image", Image,self.cb_gesture_image)
        self.frame = None
        self.lock = False
        
        self.curve_paint_timer = QTimer(self)
        self.curve_paint_timer.timeout.connect(self.update_pic)
        self.curve_paint_timer.start(0.1)
     
    def __InitView(self):
        #设置界面的尺寸为__size
        self.setFixedSize(self.__size)
        self.show_label =  QLabel(self)
        self.show_label.setFixedSize(self.__size)
        
        self.show_label.setAlignment(Qt.AlignCenter)

    def CamControl(self):
        self.isEnable_Cam = 1-self.isEnable_Cam
        return self.isEnable_Cam

    def cb_gesture_image(self,img_msg):
        if self.lock == False:
            self.frame = self.bridge.imgmsg_to_cv2(img_msg, 'bgr8')
            self.lock = True

    def update_pic(self):
        if self.isEnable_Cam:
            try:
                img_rows,img_cols,channels = self.frame.shape
                bytesPerLine = channels * img_cols
                # cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB,self.frame)
                QImg = QImage(self.frame.data,img_cols,img_rows,bytesPerLine,QImage.Format_RGB888)
                self.show_label.setStyleSheet('background-color: rgb(0, 0, 0)')
                self.show_label.setPixmap(QPixmap.fromImage(QImg).scaled(
                    self.show_label.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation
                ))
            except:
                self.isEnable_Cam = 0
            self.lock = False
        else:
            self.show_label.setStyleSheet('background-color: rgb(128,128, 128)')
            self.show_label.setText("未打开摄像头")
            self.show_label.setStyleSheet("font:30px")