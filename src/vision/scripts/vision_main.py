#!/usr/bin/python3
#coding:utf-8
import rospy
import cv2
import os
from predict_image import detectImage
import json
from vision.srv import *
class VisionNode:
    def __init__(self):
    
        rospy.init_node('vision_node', anonymous = True)          #创建节点
        
        self.rate = rospy.Rate(20)

        self.cap = cv2.VideoCapture(4)  #临时调试用
        
        #self.cap.set(3,480) #调整相机画幅大小，上位机不可用
        #self.cap.set(4,640)
        self.packagePath = rospy.get_param("/pkg_path/vision")
        self.yolov5Module = detectImage(os.path.join(self.packagePath, 'scripts/v5l-last.pt'))  #加载模型
        rospy.Service('/vision_service',VisionDetectService, self.Callback)  #建立服务

        # rospy.wait_for_service('vision_service')

        # self.vision_service = rospy.ServiceProxy('vision_service',VisionService)

    def create_vision_detect_service_response(self):
        tpm = VisionDetectServiceResponse()
        tpm.isFind = 0
        tpm.detect_res = 0
        tpm.conf = 0
        self.vision_detect_service_res = tpm

    def Callback(self, data):
        self.create_vision_detect_service_response()
        _, self.frame = self.cap.read()
        self.vision_detect_service_res = self.yolov5Module.detect(self.frame,self.vision_detect_service_res) #传入图片以及平面图像坐标系下的点击位置，识别
        #data-base
        
        return self.vision_detect_service_res
        
    def MainLoop(self):
        while not rospy.is_shutdown():
            self.rate.sleep()
            
            
if __name__ == '__main__':
    visionNode = VisionNode()
    visionNode.MainLoop()
