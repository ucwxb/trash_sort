#!/usr/bin/python3
#coding:utf-8
import rospy
from trashsql.srv import data_manage,data_manageResponse,data_manageRequest
import cv2
import os
import numpy as np
np.set_printoptions(threshold=np.inf)
class VisionNode:
    def __init__(self):
        rospy.wait_for_service('/sql_service')
        rospy.init_node('test_sql_node', anonymous = True)          #创建节点
        self.rate = rospy.Rate(10)       #20Hz     
        self.service_testVis = rospy.ServiceProxy('/sql_service', data_manage)
        
    def get_img(self):
        cap = cv2.VideoCapture(14)
        _,frame = cap.read()
        encoded_image = cv2.imencode(".jpg", frame)[1]
        encoded_image = np.array(encoded_image)
        self.image = encoded_image.flatten()
        

    def handle_rev_image(self,img):
        print(len(img))
        img = np.array(img,dtype=np.uint8)
        img = img.reshape(len(img),1)
        img = cv2.imdecode(img,cv2.IMREAD_COLOR)
        return img

    def MainLoop(self):
            
        self.get_img()
        new_data_manage_req = data_manageRequest()
        new_data_manage_req.cmd = "add"
        new_data_manage_req.src_img = self.image
        new_data_manage_req.detect_img = self.image
        new_data_manage_req.detect_res = 12
        new_data_manage_req.detect_res_string = "12123"
        res = self.service_testVis(new_data_manage_req)
        
        new_data_manage_req = data_manageRequest()
        new_data_manage_req.cmd = "get"
        testreses = self.service_testVis(new_data_manage_req)
        reses = testreses.res
        for res in reses:
            src_img = self.handle_rev_image(res.src_img)
            save_path = os.path.join(rospy.get_param("/pkg_path/trashsql"),str(res.id)+".jpg")
            cv2.imwrite(save_path,src_img)
            
            
            
if __name__ == '__main__':
    visionNode = VisionNode()
    visionNode.MainLoop()
