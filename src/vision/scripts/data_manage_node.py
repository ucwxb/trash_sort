#!/usr/bin/python3
#coding:utf-8
import rospy
import time
import os
import numpy as np
class DataManage:
    def __init__(self):
        self.pkg_path = rospy.get_param("/pkg_path/vision")
        self.data_path = os.path.join(self.pkg_path,"data")
        self.data_path = os.path.join(self.data_path,"data.json")
    
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
