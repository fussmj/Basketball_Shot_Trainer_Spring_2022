import os
import argparse
import cv2
import tflite_runtime as tf
import tflite_runtime.interpreter as Interpreter
from tflite_runtime.interpreter import load_delegate
#import tensorflow as tf
import numpy as np
import importlib.util
from threading import Thread
import time
import sys
import pathlib
from copy import copy

import sys
print(sys.path.append('/root/.local/'))




# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(640,480),framerate=30):
        # Initialize the PiCamera and the camera image stream
        #breakpoint()
        
        self.stream = cv2.VideoCapture(0)
        cv2.waitKey(1000)
        print("Camera initiated.")
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()
        #cv2.imshow('window',self.frame)
        #cv2.waitKey(1000)

    # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
    # Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
    # Return the most recent frame
        return self.frame

    def stop(self):
    # Indicate that the camera and thread should be stopped
        self.stopped = True


MODEL_NAME = 'models/lite-model_movenet_singlepose_lightning_tflite_float16_4.tflite'
#GRAPH_NAME = args.graph
#LABELMAP_NAME = args.labels
min_conf_threshold = 0.5
resW, resH = 1280, 720
imW, imH = int(resW), int(resH)
use_TPU = False

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME)

#load in the model
interpreter = Interpreter.Interpreter(model_path=PATH_TO_CKPT)
print('model loaded successfully')

#determine intput shape
interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']
print('input image shape (', width, ',', height, ')')





# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

frame_rate_calc = 1
freq = cv2.getTickFrequency()
videostream = VideoStream(resolution=(imW,imH),framerate=30).start()
time.sleep(1)


while True:
    #print('running loop')
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()
    
    # Grab frame from video stream
    frame = videostream.read()
    try:
        cv2.imshow('frame', frame)
        cv2.waitKey(33)
    except:
        print(frame)