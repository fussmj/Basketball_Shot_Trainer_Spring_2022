'''
@author: Matthew Fuss
'''
import numpy as np
import cv2

import Image_Processing_Classes as ip
from matplotlib import pyplot as plt

video = cv2.VideoCapture('clip.mp4')

if not video.isOpened():
    print("Video clips not opened successfully")
else:
    frame_rate = int(video.get(5))
    print(frame_rate)
    
    frame_count = video.get(7)
    print(frame_count)

classNames = []
classFile = 'coco.names'

configPath = ('ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
weightsPath = ('frozen_inference_graph.pb')

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


while(video.isOpened()):
    ret, frame = video.read()
    if ret:
        
        
        classIds, confs, bbox = net.detect(frame, confThreshold = 0.3)
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                if classId == 34:
                    cv2.rectangle(frame, box, color = (0, 255, 0), thickness = 2)
        cv2.imshow("Output", frame)
        
        #20 ms between frames. Replace this with a more accurate number when it matters
        k = cv2.waitKey(20)
        
        #pressing q ends the video
        if k == 113:
            break
    else:
        break        
    
 