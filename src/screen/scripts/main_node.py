#!/usr/bin/python3
#coding:utf-8
import rospy
import time
import numpy as np
from threading import Timer
import os
from watchdog import WatchDog
from screen.msg import *
from gesture.msg import *
from voice.msg import *
from surface.msg import *
from std_msgs.msg import Int32,Empty
class MainController:
    def __init__(self):
        rospy.init_node('main_node', anonymous = True)          #创建节点
        self.rospy_rate = rospy.get_param("rospy_rate")
        self.rate = rospy.Rate(self.rospy_rate)       #50H
        self.sub_topic()
        self.topic_send_cmd = rospy.Publisher("/command_total", main_msg,queue_size=1)
        self.topic_main_info = rospy.Publisher("/main_info_topic", main_info,queue_size=1)
        self.lock_queue = False
        self.cmd_queue = []
        self.cmd_queue_max_len = int(rospy.get_param("/main/cmd_queue_max_len"))
        self.cmd_stop_interval_s = int(rospy.get_param("/main/cmd_stop_interval_s"))
        self.cmd_timer_s = int(rospy.get_param("/main/cmd_timer_s"))
        self.cmd_timer_hz = int(rospy.get_param("/main/cmd_timer_hz"))
        self.time_out_s = int(rospy.get_param("/main/time_out_s"))
        self.command_list = rospy.get_param("/command_list")
        self.my_dog = WatchDog(self.check_cmd_queue)
        
        self.tello_return = np.zeros(4)
        self.current_cmd = -1
        self.before_cmd = -1
        self.same_cmd_lock = False
        self.finish_send = time.time()
        
    def sub_topic(self):
        rospy.Subscriber('/screen_detect_topic', screen_msg, self.Callback_Command)
        rospy.Subscriber('/gesture_detect_topic', gesture_msg, self.Callback_Command)
        rospy.Subscriber('/voice_detect_topic', voice_msg, self.Callback_Command)

        rospy.Subscriber('/stop_at_once_topic', Empty, self.Callback_stop_at_once_topic)

        rospy.Subscriber("/tello0/return", Empty,self.Callback_tello0_return)
        rospy.Subscriber("/tello1/return", Empty,self.Callback_tello1_return)
        rospy.Subscriber("/tello2/return", Empty,self.Callback_tello2_return)
        rospy.Subscriber("/tello3/return", Empty,self.Callback_tello3_return)

    def handle_watchdog(self,cmd_code):
        if self.my_dog.watching == False:
            self.my_dog.AutoCheck(self.cmd_timer_s,self.cmd_timer_hz,self.cmd_queue_max_len)
            if self.my_dog.Feed():
                self.cmd_queue.append(cmd_code)
        else:
            if self.my_dog.Feed():
                self.cmd_queue.append(cmd_code)

    def check_cmd_queue(self):
        cmd_num_list = np.zeros(30)
        for i in self.cmd_queue:
            cmd_num_list[i] += 1
        self.current_cmd = np.argmax(cmd_num_list)
        self.cmd_queue =[]
        self.my_dog.Kill()

    def send_cmd_func(self):
        if self.current_cmd != -1:
            if not (self.current_cmd == self.before_cmd and self.same_cmd_lock is True):
                self.topic_main_info.publish(main_info("send_cmd"))
                self.topic_send_cmd.publish(main_msg(self.current_cmd))
                self.same_cmd_lock = True
                self.before_cmd = self.current_cmd
                self.finish_send = time.time()
            self.current_cmd = -1
        else:
            if (np.sum(self.tello_return) == 4 or time.time()-self.finish_send >= self.time_out_s):
                if self.same_cmd_lock:
                    if np.sum(self.tello_return) == 4:
                        self.topic_main_info.publish(main_info("return_all_return"))
                    else:
                        self.topic_main_info.publish(main_info("time_out"))
                    self.same_cmd_lock = False
                    self.tello_return = np.zeros(4)
        
    
    def Callback_stop_at_once_topic(self,data):
        self.topic_send_cmd.publish(main_msg(9))
    

    def Callback_Command(self,msg):
        command = msg.command
        info = msg.info
        cmd_code = self.command_list.index(command)
        self.handle_watchdog(cmd_code)

    def Callback_tello0_return(self):
        self.tello_return[0] = 1
    
    def Callback_tello1_return(self):
        self.tello_return[1] = 1
    
    def Callback_tello2_return(self):
        self.tello_return[2] = 1
    
    def Callback_tello3_return(self):
        self.tello_return[3] = 1

    def MainLoop(self):
        while not rospy.is_shutdown():
            self.rate.sleep()
            self.send_cmd_func()
            

if __name__ == '__main__':
    node1 = MainController()
    node1.MainLoop()
