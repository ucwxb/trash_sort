#!/usr/bin/python3
#coding:utf-8
import rospy
import time
import os
from sql_manage import sql_manage
from data_manage.srv import *
class DataManage:
    def __init__(self):
        rospy.init_node('data_manage_node', anonymous = True)          #创建节点
        self.rate = rospy.Rate(50)       #50H
        self.pkg_path = rospy.get_param("/pkg_path/data_manage")

        self.host = rospy.get_param("/data_manage/host")
        self.user = rospy.get_param("/data_manage/user")
        self.password = rospy.get_param("/data_manage/password")
        self.db_name = rospy.get_param("/data_manage/db_name")
        self.port = rospy.get_param("/data_manage/port")
        self.charset = rospy.get_param("/data_manage/charset")
        self.my_sql_manage = sql_manage(
            self.host,
            self.user,
            self.password,
            self.db_name,
            self.port,
            self..charset
        )

        rospy.Service('/sql_service',yaml_srv, self.sql_srv_func)
        
    def sql_srv_func(self,srv_data):
        cmd = srv_data.cmd
        pkg_name = srv_data.pkg_name
        class_name = srv_data.class_name
        res = yaml_srvResponse()
        if cmd == "add":
            src_img = srv_data.src_img
            detect_img = srv_data.detect_img
            detect_res = srv_data.detect_res
            detect_res_string = srv_data.detect_res_string
            res.code = self.my_yaml_manage.add_data(src_img,detect_img,detect_res,detect_res_string)
        elif cmd == "get":
            res.code = self.my_yaml_manage.get_data(pkg_name,class_name)
        return res
        
    def MainLoop(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

if __name__ == '__main__':
    node1 = DataManage()
    node1.MainLoop()
