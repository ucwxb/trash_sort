#!/usr/bin/python3
#coding:utf-8
import rospy
import cv2
import os
from predict_image import detectImage
import json
from vision.srv import VisionDetectService,VisionDetectServiceResponse,VisionDetectServicesRequest
class VisionNode:
    def __init__(self):
    
        rospy.init_node('vision_node', anonymous = True)          #创建节点
        
        self.rate = rospy.Rate(20)

        self.cap = cv2.VideoCapture(0)  #临时调试用
        
        #self.cap.set(3,480) #调整相机画幅大小，上位机不可用
        #self.cap.set(4,640)
        self.packagePath = rospy.get_param("/pkg_path/vision")
        self.yolov5Module = detectImage(os.path.join(self.packagePath, 'scripts/yolov5/v5l-last.pt'))  #加载模型
        rospy.Service('/vision_service',VisionDetectService, self.Callback)  #建立服务

        # rospy.wait_for_service('vision_service')

        # self.vision_service = rospy.ServiceProxy('vision_service',VisionService)

    def create_vision_detect_service_response(self):
        tpm = VisionDetectServiceResponse()
        tpm.isFind = 0
        tpm.detect_res = 0
        tpm.detect_res_string = ""
        self.vision_detect_service_res = tpm

    def Callback(self, data):
        self.create_vision_detect_service_response()

        self.yolov5Module.detect(self.frame,self.vision_detect_service_res) #传入图片以及平面图像坐标系下的点击位置，识别
        
        
        if(self.yolov5Module.update == 1): #检测结果是否更新
            self.yolov5Module.update = 0
            vision_src_res.isFind = 1 #标记找到

            redPot_robot  = self.cameraInfo.Tr_img2global(self.yolov5Module.res_red_xywh[0],self.yolov5Module.res_red_xywh[1])  #相机的global是机器人坐标系！！！！！
            bluePot_robot = self.cameraInfo.Tr_img2global(self.yolov5Module.res_blue_xywh[0],self.yolov5Module.res_blue_xywh[1])  #相机的global是机器人坐标系！！！！！

            srv_res.append(redPot_robot[0])
            srv_res.append(redPot_robot[1])
            srv_res.append(bluePot_robot[0])
            srv_res.append(bluePot_robot[1])

            vision_src_res.res = srv_res
            return vision_src_res#计算鼠标点击位置的对应坐标(图像上的x, 图像上的y, 目标物已知高度z坐标)
        vision_src_res.isFind = 0
        vision_src_res.res = srv_res
        return vision_src_res
        
    def MainLoop(self):
        while not rospy.is_shutdown():
            _, self.frame = self.cap.read()
            self.rate.sleep()
            
            
if __name__ == '__main__':
    visionNode = VisionNode()
    visionNode.MainLoop()
