#!/usr/bin/python3
#coding:utf-8
import rospy
from vision.srv import VisionService,VisionServiceResponse
import json

class VisionNode:
    def __init__(self):
        rospy.wait_for_service('/vision_service')
        rospy.init_node('test_vision_node', anonymous = True)          #创建节点
        
        self.rate = rospy.Rate(1)       #20Hz     
        self.service_testVis = rospy.ServiceProxy('/vision_service', VisionService)
    def MainLoop(self):
        while not rospy.is_shutdown():
            self.rate.sleep()
            res = self.service_testVis(0,0,0)
            if(len(res.res)>1):
                print("red_x:{},red_y:{},blue_x:{},blue_y:{}".format(res.res[0],res.res[1],res.res[2],res.res[3]))
            else:
                print(res.type)
            
            
if __name__ == '__main__':
    visionNode = VisionNode()
    visionNode.MainLoop()
