#!/usr/bin/python3
#coding:utf-8
import numpy as np
import os
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.Qt import QSize
from PyQt5.QtCore import Qt,QTimer,QThread
import rospy
from nlink_parser.msg import LinktrackAnchorframe0
from geometry_msgs.msg import Twist
import time
import os
import random
class CurvePaint(FigureCanvasQTAgg):
    def __init__(self,__package_path,parent = None):
        self.fig = Figure()
        super(CurvePaint,self).__init__(self.fig)

        self.logs_path = os.path.join(__package_path,"logs")
        self.tello0_pos_log = open(os.path.join(self.logs_path,"%s-tello0-pos"%(self.get_time())),"w+")
        self.tello1_pos_log = open(os.path.join(self.logs_path,"%s-tello1-pos"%(self.get_time())),"w+")
        self.tello2_pos_log = open(os.path.join(self.logs_path,"%s-tello2-pos"%(self.get_time())),"w+")
        self.tello3_pos_log = open(os.path.join(self.logs_path,"%s-tello3-pos"%(self.get_time())),"w+")
        self.human4_pos_log = open(os.path.join(self.logs_path,"%s-human4-pos"%(self.get_time())),"w+")
        self.car5_pos_log = open(os.path.join(self.logs_path,"%s-car5-pos"%(self.get_time())),"w+")
        self.car6_pos_log = open(os.path.join(self.logs_path,"%s-car6-pos"%(self.get_time())),"w+")
        self.car7_pos_log = open(os.path.join(self.logs_path,"%s-car7-pos"%(self.get_time())),"w+")

        self.pos_log_list = []
        self.pos_log_list.append(self.tello0_pos_log)
        self.pos_log_list.append(self.tello1_pos_log)
        self.pos_log_list.append(self.tello2_pos_log)
        self.pos_log_list.append(self.tello3_pos_log)
        self.pos_log_list.append(self.human4_pos_log)
        self.pos_log_list.append(self.car5_pos_log)
        self.pos_log_list.append(self.car6_pos_log)
        self.pos_log_list.append(self.car7_pos_log)

        self.tello0_vel_log = open(os.path.join(self.logs_path,"%s-tello0-vel"%(self.get_time())),"w+")
        self.tello1_vel_log = open(os.path.join(self.logs_path,"%s-tello1-vel"%(self.get_time())),"w+")
        self.tello2_vel_log = open(os.path.join(self.logs_path,"%s-tello2-vel"%(self.get_time())),"w+")
        self.tello3_vel_log = open(os.path.join(self.logs_path,"%s-tello3-vel"%(self.get_time())),"w+")
        self.human4_vel_log = open(os.path.join(self.logs_path,"%s-human4-vel"%(self.get_time())),"w+")
        self.car5_vel_log = open(os.path.join(self.logs_path,"%s-car5-vel"%(self.get_time())),"w+")
        self.car6_vel_log = open(os.path.join(self.logs_path,"%s-car6-vel"%(self.get_time())),"w+")
        self.car7_vel_log = open(os.path.join(self.logs_path,"%s-car7-vel"%(self.get_time())),"w+")

        self.vel_log_list = []
        self.vel_log_list.append(self.tello0_vel_log)
        self.vel_log_list.append(self.tello1_vel_log)
        self.vel_log_list.append(self.tello2_vel_log)
        self.vel_log_list.append(self.tello3_vel_log)
        self.vel_log_list.append(self.human4_vel_log)
        self.vel_log_list.append(self.car5_vel_log)
        self.vel_log_list.append(self.car6_vel_log)
        self.vel_log_list.append(self.car7_vel_log)
       
        self.setFixedSize(QSize(250,900))
        self.ax_1 = self.fig.add_subplot(411)
        self.ax_2 = self.fig.add_subplot(412)
        self.ax_3 = self.fig.add_subplot(413)
        self.ax_4= self.fig.add_subplot(414)
        self.ax = [self.ax_1,self.ax_2,self.ax_3,self.ax_4]
        self.fig.subplots_adjust(hspace = 1.0)

        self.tello_pos=[[[] for _ in range(3)] for k in range(8)]
        self.tello_cmd_vel=[[[] for _ in range(3)] for k in range(8)]
        self.curve_paint_timer = QTimer(self)
        self.curve_paint_timer.timeout.connect(self.update_curve_paint)
        self.curve_paint_timer.start(500)
        self.curve_paint_mode = 0
        self.curve_paint_mode_list = ["标签位置","0号机速度","1号机速度","2号机速度","3号机速度"]
        self.topic_init()

        self.pos_x = np.arange(self.x_len_min,self.x_len_max,1)
        self.pos_y = np.arange(self.y_len_min,self.y_len_max,1)
        self.vel_y = np.arange(1.4,1.8,0.2)

        if self.curve_paint_mode == 0:
            for i in range(4):
                self.ax[i].cla()
                self.ax[i].set_xlim(self.x_len_min,self.x_len_max)
                self.ax[i].set_ylim(self.y_len_min,self.y_len_max)
                self.ax[i].set_xticks(self.pos_x)
                self.ax[i].set_yticks(self.pos_y)

    def get_time(self):
        time_stamp = time.time() #获取当前时间戳
        time_array = time.localtime(time_stamp) #时间戳转时间数组
        time_str = time.strftime("%m:%d:%H:%M:%S",time_array) # 时间数组转时间字符串
        return time_str

    def switch_mode(self):
        self.curve_paint_mode += 1
        self.curve_paint_mode %= len(self.curve_paint_mode_list)
        if self.curve_paint_mode == 0:
            for i in range(4):
                self.ax[i].cla()
                self.ax[i].set_xlim(0,6)
                self.ax[i].set_ylim(0,6)
                self.ax[i].set_xticks(self.pos_x)
                self.ax[i].set_yticks(self.pos_y)
        else:
            for i in range(3):
                self.ax[i].cla()
                self.ax[i].set_xlim(0,10)
                self.ax[i].set_ylim(-0.8,0.8)
                self.ax[i].set_yticks(self.vel_y)

    
    def get_current_mode(self):
        return self.curve_paint_mode_list[self.curve_paint_mode]

    def topic_init(self):
        self.x_len_min = rospy.get_param("/x_len_min")
        self.x_len_max = rospy.get_param("/x_len_max")
        self.y_len_min = rospy.get_param("/y_len_min")
        self.y_len_max = rospy.get_param("/y_len_max")
        rospy.Subscriber("/nlink_linktrack_anchorframe0",LinktrackAnchorframe0,self.cb_readPos)
        rospy.Subscriber("/tello0/cmd_vel",Twist,self.cb_tello0_vel)
        rospy.Subscriber("/tello1/cmd_vel",Twist,self.cb_tello1_vel)
        rospy.Subscriber("/tello2/cmd_vel",Twist,self.cb_tello2_vel)
        rospy.Subscriber("/tello3/cmd_vel",Twist,self.cb_tello3_vel)


    def update_curve_paint(self):
        if self.curve_paint_mode == 0:
            self.handle_paint_pos(self.tello_pos)
        else:
            self.handle_paint_vel(self.tello_cmd_vel[self.curve_paint_mode-1])
    
    def handle_paint_pos(self,tello_pos):
        for i in range(4):
            self.ax[i].plot(tello_pos[i][0],tello_pos[i][1])
            try:
                self.ax[i].set_xlabel("(%.2f,%.2f)"%(tello_pos[i][0][-1],tello_pos[i][1][-1]))
            except:
                self.ax[i].set_xlabel("None")
        self.fig.canvas.draw_idle()
    
    def handle_paint_vel(self,tello_vel):
        for i in range(3):
            self.ax[i].cla()
            self.ax[i].set_xlim(0,10)
            self.ax[i].set_ylim(1.4,1.8)
            self.ax[i].set_yticks(self.vel_y)
            self.ax[i].plot(tello_vel[i])
            try:
                self.ax[i].set_xlabel("(%.3f)"%(tello_vel[i][-1]))
            except:
                self.ax[i].set_xlabel("None")
        self.fig.canvas.draw_idle()

    def cb_readPos(self,msg):
        msg = msg.nodes
        for each_msg in msg:
            try:
                self.tello_pos[each_msg.id][0].append(each_msg.pos_3d[0])
                self.tello_pos[each_msg.id][1].append(each_msg.pos_3d[1])
                self.pos_log_list[each_msg.id].write("%.4f %.4f\n"%(each_msg.pos_3d[0],each_msg.pos_3d[1]))
                if len(self.tello_pos[each_msg.id][0]) >=50:
                    self.tello_pos[each_msg.id][0].pop(0)
                if len(self.tello_pos[each_msg.id][1]) >= 50:
                    self.tello_pos[each_msg.id][1].pop(0)
            except:
                continue

    def cb_tello0_vel(self,msg):
        self.tello_cmd_vel[0][0].append(msg.linear.x)
        self.tello_cmd_vel[0][1].append(msg.linear.y)
        self.tello_cmd_vel[0][2].append(msg.linear.z)
        self.vel_log_list[0].write("%.2f %.2f %.2f\n"%(msg.linear.x,msg.linear.y,msg.linear.z))
        for i in range(3):
            if len(self.tello_cmd_vel[0][i]) >=100:
                self.tello_cmd_vel[0][i].pop(0)

    def cb_tello1_vel(self,msg):
        self.tello_cmd_vel[1][0].append(msg.linear.x)
        self.tello_cmd_vel[1][1].append(msg.linear.y)
        self.tello_cmd_vel[1][2].append(msg.linear.z)
        self.vel_log_list[1].write("%.2f %.2f %.2f\n"%(msg.linear.x,msg.linear.y,msg.linear.z))
        for i in range(3):
            if len(self.tello_cmd_vel[1][i]) >=100:
                self.tello_cmd_vel[1][i].pop(0)

    def cb_tello2_vel(self,msg):
        self.tello_cmd_vel[2][0].append(msg.linear.x)
        self.tello_cmd_vel[2][1].append(msg.linear.y)
        self.tello_cmd_vel[2][2].append(msg.linear.z)
        self.vel_log_list[2].write("%.2f %.2f %.2f\n"%(msg.linear.x,msg.linear.y,msg.linear.z))
        for i in range(3):
            if len(self.tello_cmd_vel[2][i]) >=100:
                self.tello_cmd_vel[2][i].pop(0)

    def cb_tello3_vel(self,msg):
        self.tello_cmd_vel[3][0].append(msg.linear.x)
        self.tello_cmd_vel[3][1].append(msg.linear.y)
        self.tello_cmd_vel[3][2].append(msg.linear.z)
        self.vel_log_list[3].write("%.2f %.2f %.2f\n"%(msg.linear.x,msg.linear.y,msg.linear.z))
        for i in range(3):
            if len(self.tello_cmd_vel[3][i]) >=100:
                self.tello_cmd_vel[3][i].pop(0)