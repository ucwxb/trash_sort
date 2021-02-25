import sys
import os
# sys.path.append(rospy.get_param('/pkg_path/vision'))
import torch
from models.experimental import attempt_load
import numpy as np
from numpy import random
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords,
    xyxy2xywh, plot_one_box, strip_optimizer, set_logging)
from utils.datasets import LoadStreams, LoadImages,letterbox
import cv2

class detectImage:
    def __init__(self,modulePath,imgsz = 640,classes = 0,device=''):
        self.selectDevice(device)  #选择gpu或cpu
        self.modulePath = modulePath  #模型路径
        self.model = attempt_load(modulePath, map_location=self.device) # 加载模型
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names # 获取类别
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(self.names))] # 为不同类别分配颜色
        self.classes  = classes
        self.imgsz = imgsz  #图片大小
        self.update = 0  #是否更新的标志

    def selectDevice(self,device):
        cpu_request = device.lower() == 'cpu'
        cuda = False if cpu_request else torch.cuda.is_available()
        self.device = torch.device('cuda:0' if cuda else 'cpu')

    def loadPic(self,frame): #图像预处理
        self.src_img = frame.copy()
        self.detect_img = frame
        img = letterbox(self.detect_img, new_shape=self.imgsz)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.float()
        img /= 255.0  # 归一化
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        return img

    def detect(self,frame,vision_detect_service_res):
        img = self.loadPic(frame) #加载数据集
        pred = self.model(img, augment=False)[0] #检测
        pred = non_max_suppression(pred, 0.4, 0.5, classes=None, agnostic=False)[0] #NMS
        
        if pred is not None and len(pred):
            pred[:, :4] = scale_coords(img.shape[2:], pred[:, :4], self.detect_img.shape).round()
            pred = pred.cuda().data.cpu().numpy()
            max_indexs = np.argmax(pred, axis=0)
            max_index = max_indexs[-2]
            pred = pred[max_index]
            *xyxy, conf, cls = pred
            label = '%s %.2f' % (self.names[int(cls)], conf)
            plot_one_box(xyxy, self.detect_img, label=label, color=self.colors[int(cls)])
                #     res_xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4))).view(-1).tolist()
                #     res_xyxy = torch.tensor(xyxy).view(-1).tolist()

                #     self.res_xywh.append(res_xywh)
                #     self.res_xyxy.append(res_xyxy)
                    
                    # diag_co = torch.tensor(xyxy).view(1, 4).detach().numpy().tolist() #对角坐标
                    # xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    # center_co = (torch.tensor(xywh) * gn).detach().numpy().tolist() #中心坐标与长宽
                    # label = '%s' % (self.names[int(cls)])

                    # put_str = 'location:'
                    # for rect in diag_co: #画框与文字
                    #     # rect = [int(i) for i in rect]
                    #     # cv2.rectangle(self.im0, (rect[0],rect[1],rect[2],rect[3]), (0, 0, 255),6)
                    #     cv2.rectangle(self.im0, (int(rect[0]),int(rect[1]),int(rect[2]),int(rect[3])), (0, 0, 255),6)
                    #     # cv2.putText(self.im0, label, (rect[0],rect[1]), cv2.FONT_ITALIC, 4, (0, 255, 0), 6)
                    #     cv2.putText(self.im0, label, (int(rect[0]),int(rect[1])), cv2.FONT_ITALIC, 4, (0, 255, 0), 6)
                    #     put_str += str(rect)
                    # cv2.putText(self.im0, put_str, (10, 100), cv2.FONT_ITALIC, 3, (255, 0, 0), 6)
        # self.diag_co = diag_co
        # self.center_co = center_co
        # self.label = label
        # self.conf = conf
        
if __name__ == '__main__':
    testM = detectImage('v5l-last.pt')
    frame = cv2.imread('2.png')
    testM.detect(frame)
