#!/usr/bin/python3
#coding:utf-8
import rospy
from vision.srv import VisionDetectService,VisionDetectServiceResponse,VisionDetectServiceRequest
import json

class VisionNode:
    def __init__(self):
        rospy.wait_for_service('/vision_service')
        rospy.init_node('test_vision_node', anonymous = True)          #创建节点
        
        self.rate = rospy.Rate(2000)       #20Hz     
        self.service_testVis = rospy.ServiceProxy('/vision_service', VisionDetectService)
    def MainLoop(self):
        while not rospy.is_shutdown():
            self.rate.sleep()
            res = self.service_testVis()
            print(res.isFind,res.detect_res,res.conf)
            
            
if __name__ == '__main__':
    visionNode = VisionNode()
    visionNode.MainLoop()
