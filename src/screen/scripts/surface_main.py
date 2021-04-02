#!/usr/bin/python3
#coding:utf-8
from PyQt5.Qt import QWidget, QColor, QPixmap, QIcon, QSize, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSplitter,\
    QComboBox, QLabel, QSpinBox, QFileDialog,QMessageBox,QInputDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt,QTimer
import sys
from PaintBoard import PaintBoard
from CamWin import CamWin
from MsgCtl import MsgCtl
from BtnCtl import BtnCtl
from CurvePaint import CurvePaint
import time
import os
import cv2
import random
import rospy
from surface.msg import *
from screen.msg import *
from gesture.msg import *
from voice.msg import *
from std_msgs.msg import Int32,Empty

class MainWidget(QWidget):
    
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.__InitData()
        self.__InitBtn()
        self.__InitView()
        self.__InitRos()
    
    def __InitRos(self):
        
        rospy.init_node('surface_node')
        self.rospy_rate = rospy.get_param("rospy_rate")
        self.rate = rospy.Rate(self.rospy_rate)
        

        rospy.Subscriber('/screen_detect_topic', screen_msg, self.Callback_screen)
        rospy.Subscriber('/gesture_detect_topic', gesture_msg, self.Callback_gesture)
        rospy.Subscriber('/voice_detect_topic', voice_msg, self.Callback_voice)
        rospy.Subscriber('/command_total', main_msg, self.Callback_main)

        self.stop_at_once_topic = rospy.Publisher("/stop_at_once_topic",Empty,queue_size=1)
        self.points_trans_topic = rospy.Publisher("/points_trans",points_trans,queue_size=1)
        self.lan_change_topic = rospy.Publisher("/lan_change_topic",Int32,queue_size=1)
        
    def __InitData(self):
        #初始化数据
        #变量名前有两个下划线代表类的私有变量
        #获取QT中的颜色列表(字符串的List)
        self.__paintBoard = PaintBoard(self)
        self.__CamWin = CamWin(self)
        self.__MsgCtl = MsgCtl(self)
        
        self.__colorList = QColor.colorNames()
        self.__package_path = rospy.get_param('/pkg_path/surface')

        self.__CurvePaint = CurvePaint(self.__package_path,self)

        # self.voice_record_status = -1 #start
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_btn_status)
        self.timer.start(50)
        
        self.language_CN_list = ["普通话","英语","粤语"," 四川话"]
        self.language_index = 0

        self.painter_timer = QTimer(self)
        self.painter_timer.timeout.connect(self.update_painter)
        self.painter_timer.start(1)

        self.filter_name_list = ["全部","主","手势","语音","笔画"]
        self.filter_index = 0
        

    def __InitBtn(self):
        self.btn_CH_name = [
            "打开摄像头","笔画识别","标签位置",
            "切换语言（普通话）","只看主节点相关","清空信息",
            "编码查询","紧急着地","显示电量"
        ]
        self.btn_EN_name = [
            "CamControl","RecTour","PaintClear",
            "LanChange","FilterMain","MsgClear",
            "CodeSearch","StopAtOnce","ShowBattery"
        ]
        self.__BtnCtl = BtnCtl(self.btn_CH_name,self.btn_EN_name,self)
        self.__BtnCtl.btn_dict["CamControl"].clicked.connect(self.CamControl)
        self.__BtnCtl.btn_dict["RecTour"].clicked.connect(self.RecTour_UP)
        self.__BtnCtl.btn_dict["PaintClear"].clicked.connect(self.PaintClear_HOLD)

        self.__BtnCtl.btn_dict["LanChange"].clicked.connect(self.LanChange)
        self.__BtnCtl.btn_dict["FilterMain"].clicked.connect(self.FilterMain)
        self.__BtnCtl.btn_dict["MsgClear"].clicked.connect(self.MsgClear)
        self.__BtnCtl.btn_dict["ShowBattery"].clicked.connect(self.ShowBattery)
        self.__BtnCtl.btn_dict["StopAtOnce"].clicked.connect(self.StopAtOnce)
        self.__BtnCtl.btn_dict["CodeSearch"].clicked.connect(self.CodeSearch)

    def __InitView(self):
        '''
                  初始化界面
        '''
        self.setFixedSize(1500,900)
        self.setWindowTitle("人-机器人集群系统交互平台")
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        # main_layout.setSpacing(10)

        #新建一个水平布局作为本窗体的主布局
        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0,0,0,0)
        # second_layout.setSpacing(10)
        top_layout.addWidget(self.__CamWin)
        top_layout.addWidget(self.__paintBoard)
        main_layout.addLayout(top_layout)

        bottom_layout = QVBoxLayout()
        bottom_layout.setContentsMargins(0,0,0,0)
        bottom_layout.addWidget(self.__MsgCtl)
        bottom_layout.addWidget(self.__BtnCtl)
        main_layout.addLayout(bottom_layout)
        

        curvepaint_layout = QVBoxLayout()
        curvepaint_layout.addWidget(self.__CurvePaint)
        main_layout.addLayout(curvepaint_layout)

    def CamControl(self):
        if self.__CamWin.CamControl():
            self.__BtnCtl.change_btn_text("CamControl","关闭摄像头")
            self.__MsgCtl.AddMsg("已开启摄像头")
        else:
            self.__BtnCtl.change_btn_text("CamControl","开启摄像头")
            self.__MsgCtl.AddMsg("已关闭摄像头")
        
    def RecTour(self):
        _DrawPos = self.__paintBoard.GetDrawPos()
        if len(_DrawPos) > 0 :
            self.new_points_trans = points_trans()
            self.__paintBoard.Clear()
            self.__paintBoard.update()
            for each_pos in _DrawPos:
                new_point = point()
                new_point.x = each_pos.X
                new_point.y = each_pos.Y
                self.new_points_trans.points.append(new_point)
            self.points_trans_topic.publish(self.new_points_trans)
        else:
            self.__MsgCtl.AddMsg("画板为空")
    
    def PaintClear(self):
        self.__paintBoard.Clear()

    def LanChange(self):
        self.language_index += 1
        self.language_index %= len(self.language_CN_list)
        self.lan_change_topic.publish(self.language_index)

    def update_btn_status(self):

        # if self.voice_record_status:
        #     self.__BtnCtl.btn_dict["LanChange"].setStyleSheet('background-color: rgb(255, 0, 0)')
        #     # self.__BtnCtl.btn_dict["RecordStatus"].setText("正在录音")
        # elif self.voice_record_status == 0:
        #     self.__BtnCtl.btn_dict["LanChange"].setStyleSheet('background-color: rgb(0, 255, 0)')
        #     # self.__BtnCtl.btn_dict["RecordStatus"].setText("结束录音")
        # # elif self.voice_record_status == -1:
        # #     self.__BtnCtl.btn_dict["RecordStatus"].setText("等待识别服务")
        self.__BtnCtl.btn_dict["LanChange"].setText("切换语言（%s）" % self.language_CN_list[self.language_index])
        
        self.__BtnCtl.btn_dict["FilterMain"].setText(self.filter_name_list[self.filter_index]+"节点")

        self.__BtnCtl.btn_dict["PaintClear"].setText(self.__CurvePaint.get_current_mode())
        
    
    def update_painter(self):
        if self.__paintBoard.isRelease:
            self.__paintBoard.isRelease = False
            self.RecTour()

    def FilterMain(self):
        self.filter_index += 1
        self.filter_index %= len(self.filter_name_list)
        if self.filter_index !=0 :
            self.__MsgCtl.filter_target = self.filter_name_list[self.filter_index]
        else:
            self.__MsgCtl.filter_target = ""
    
    def MsgClear(self):
        self.__MsgCtl.ClearAllMsg()

    def ShowBattery(self):
        self.__MsgCtl.show_battery()

    def RecTour_UP(self):
        send_cmd_count = 2
        while(send_cmd_count>0):
            self.stop_at_once_topic.publish(stop_at_once_topic(1))
            send_cmd_count-=1

    def PaintClear_HOLD(self):
        self.__CurvePaint.switch_mode()

    def StopAtOnce(self):
        send_cmd_count = 2
        self.__MsgCtl.AddMsg("<font color=red><b>发起紧急着地</b></font>")
        while(send_cmd_count>0):
            self.stop_at_once_topic.publish()
            send_cmd_count-=1

    def CodeSearch(self):
        CodeMsg = "UP: 1                             #起飞 <br>"\
                                "STOP: 3                        #悬停 <br>"\
                                "DOWN: 9                      #降落 <br>"\
                                "LEFT: 13                       #向左 <br>"\
                                "RIGHT: 14                    #向右 <br>"\
                                "FORWARD: 15            #前进 <br>"\
                                "BACKWARD: 16         #后退 <br>"\
                                "LINE: 18                       #一字形 <br>"\
                                "TRIANGLE: 19            #三角形 <br>"\
                                "RECTANGLE: 20        #长方形"
        self.__MsgCtl.AddMsg(CodeMsg)


    def Callback_screen(self,msg):
        string = msg.command
        self.__MsgCtl.AddMsg("<b>[笔画识别]</b> "+string)

    def Callback_gesture(self,msg):
        string = msg.command
        self.__MsgCtl.AddMsg("<b>[手势识别]</b> "+string)

    def Callback_voice(self,msg):
        string = msg.command
        self.__MsgCtl.AddMsg("<b>[语音识别]</b> "+string)

    def Callback_main(self,msg):
        string = str(msg.data)
        self.__MsgCtl.AddMsg("<b>[主节点发出指令]</b> "+string)
    

def main():
    app = QApplication(sys.argv) # sys.argv即命令行参数
    mainWidget = MainWidget() #新建一个主界面
    mainWidget.show()	#显示主界面
    exit(app.exec_()) #进入消息循环

if __name__ == '__main__':
    main()
