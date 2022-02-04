'''
Created on Sep 23, 2021

@author: Matthew
'''
import numpy as np
import cv2
import User_Classes as uc
import Image_Processing_Classes as ip
from matplotlib import pyplot as plt

img = cv2.imread("image4.jpg")
#cap = cv2.VideoCapture(0)

classNames = []
classFile = 'coco.names'

configPath = ('ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
weightsPath = ('frozen_inference_graph.pb')

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

classIds, confs, bbox = net.detect(img, confThreshold = 0.2)
if len(classIds) != 0:
    for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
        if classId == 34:
            cv2.rectangle(img, box, color = (0, 255, 0), thickness = 2)
cv2.imshow("Output", img)
cv2.waitKey(0)