from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QHBoxLayout, QVBoxLayout,QTextEdit
from PyQt5.Qt import QSize,QPixmap
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import *
import time
import rospy
from tello_driver.msg import TelloStatus
import numpy as np
class MsgCtl(QWidget):
    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)

        self.__InitData() #先初始化数据，再初始化界面
        self.__InitView()
        self.timer.start(50)
        
    def __InitData(self):
        
        self.__size = QSize(650,600)
        self.Msg = ""
        self.filter_target = ""
        self.Msg_list = []
        self.new_Msg = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_msg)

        self.tello_battery = np.zeros(4)
        rospy.Subscriber("/tello0/status", TelloStatus, self.cb_tello0_status)
        rospy.Subscriber("/tello1/status", TelloStatus, self.cb_tello1_status)
        rospy.Subscriber("/tello2/status", TelloStatus, self.cb_tello2_status)
        rospy.Subscriber("/tello3/status", TelloStatus, self.cb_tello3_status)

    def show_battery(self):
        string = "tello0：%d<br>"%self.tello_battery[0]
        string += "tello1：%d<br>"%self.tello_battery[1]
        string += "tello2：%d<br>"%self.tello_battery[2]
        string += "tello3：%d<br>"%self.tello_battery[3]
        self.AddMsg(string)
     
    def cb_tello0_status(self, msg):
        self.tello_battery[0] = msg.battery_percentage
        print("tello0:",msg.battery_percentage)
    def cb_tello1_status(self, msg):
        self.tello_battery[1] = msg.battery_percentage
        print("tello1:",msg.battery_percentage)
    def cb_tello2_status(self, msg):
        self.tello_battery[2] = msg.battery_percentage
        print("tello2:",msg.battery_percentage)
    def cb_tello3_status(self, msg):
        self.tello_battery[3] = msg.battery_percentage
        print("tello3:",msg.battery_percentage)

    def update_msg(self):
        filter_res = []
        if self.filter_target != "":
            for each_msg in self.Msg_list:
                if self.filter_target in each_msg:
                    filter_res.append(each_msg)
            if len(filter_res)<=0:
                filter_res.append("未找到信息")
        else:
            filter_res = self.Msg_list
        self.Msg = '<br>'.join(filter_res)
        self.Msg_show.setText(self.Msg)

    def __InitView(self):
        #设置界面的尺寸为__size
        self.setFixedSize(self.__size)

        self.Msg_show = QTextEdit(self)
        self.Msg_show.setFixedSize(self.__size)
        self.Msg_show.setStyleSheet("font:30px")
        self.Msg_show.setVerticalScrollBarPolicy(2)
        self.Msg_show.setFocusPolicy(Qt.NoFocus)
        self.Msg_show.setText(self.Msg)
        self.Msg_show.textChanged.connect(self.onAutoScroll)
    
    def AddMsg(self,text):
        time_str = "<font color=grey >[%s]</font> %s " % (self.get_time(),text)
        self.Msg_list.append(time_str)

        # if self.Msg!="":
        #     self.Msg+="\n"
        # self.Msg+="[%s]" % self.get_time()
        # self.Msg += text
        # self.new_Msg = 1
        # Msg = self.Msg
        # self.Msg_show.setText(Msg)
    def FilterMsg(self,target):
        self.filter_target = target
    
    def ClearAllMsg(self):
        self.Msg = ""
        self.Msg_list = []
        self.Msg_show.setText("")

    def onAutoScroll(self):
        self.Msg_show.ensureCursorVisible()  # 游标可用
        cursor = self.Msg_show.textCursor()  # 设置游标
        pos = len(self.Msg_show.toPlainText())  # 获取文本尾部的位置
        cursor.setPosition(pos)  # 游标位置设置为尾部
        self.Msg_show.setTextCursor(cursor)  # 滚动到游标位置
        # self.Msg_show.verticalScrollBar.
        # self.Msg_show.verticalScrollBar.setValue(self.Msg_show.verticalScrollBar.maximum)

    def get_time(self):
        time_stamp = time.time() #获取当前时间戳
        time_array = time.localtime(time_stamp) #时间戳转时间数组
        time_str = time.strftime("%H:%M:%S",time_array) # 时间数组转时间字符串
        return time_str
        
        
