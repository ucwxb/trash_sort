#!/usr/bin/python3
#coding:utf-8
import rospy
import time
import os
import numpy as np
np.set_printoptions(threshold=np.inf)
from sql_manage import sql_manage
from trashsql.srv import data_manage,data_manageResponse
class DataManage:
    def __init__(self):
        rospy.init_node('data_manage_node', anonymous = True)          #创建节点
        self.rate = rospy.Rate(10)       #50H
        self.pkg_path = rospy.get_param("/pkg_path/trashsql")

        self.host = rospy.get_param("/trashsql/host")
        self.user = rospy.get_param("/trashsql/user")
        self.password = rospy.get_param("/trashsql/password")
        self.db_name = rospy.get_param("/trashsql/db_name")
        self.port = rospy.get_param("/trashsql/port")
        self.charset = rospy.get_param("/trashsql/charset")
        self.my_sql_manage = sql_manage(
            self.host,
            self.user,
            self.password,
            self.db_name,
            self.port,
            self.charset
        )
        rospy.Service('/sql_service',data_manage, self.sql_srv_func)
    
    def handle_rev_image(self,img):
        # print("handle_rev_image")
        img = np.array(list(img),dtype=np.uint8)
        img = img.reshape(img.shape[0],1)
        # print(img.dtype)
        img = img.tostring()
        # print(len(img))
        return img

    def sql_srv_func(self,srv_data):
        new_data_manage = data_manageResponse()
        new_data_manage.status = 0
        cmd = srv_data.cmd
        if cmd == "add":
            src_img = self.handle_rev_image(srv_data.src_img)
            detect_img = self.handle_rev_image(srv_data.detect_img)
            detect_res = srv_data.detect_res
            detect_res_string = srv_data.detect_res_string
            new_data_manage.status = self.my_sql_manage.add_data(src_img,detect_img,detect_res,detect_res_string)
        elif cmd == "get":
           new_data_manage = self.my_sql_manage.get_data(new_data_manage)
        return new_data_manage
        
    def MainLoop(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

if __name__ == '__main__':
    node1 = DataManage()
    node1.MainLoop()
