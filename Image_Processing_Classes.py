#import libraries
import numpy as np
import cv2
import Image_Processing_Classes as ip
from matplotlib import pyplot as plt
import mediapipe as mp
import math
import os
import imutils
from IPython.display import Image


class BST_Image_Proc:
    #this class will serve as a way to incorporate multiple image processing libraries
    def __init__(self):
        self.vid = cv2.VideoCapture(0)

    #creating mediapipe objects for finding body position
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils 
        self.mp_styles = mp.solutions.drawing_styles
        self.yolo = None

        #getting deep neural network data for processing
        self.yolo, self.layer_names = self.initialise_yolo()
    
    
    def initialize_yolo(self):
        """
        Function to initialise the weights, architecture, and labels for the yolo model

        :return: yolo model, yolo model output layer names, model labels (ball, person, etc.)
        """
        yolo_dir = os.path.abspath("./yolo")

        # load the labels, weights, and config for the yolo model
        weights_path = os.path.sep.join([yolo_dir, "yolov3.weights"])
        config_path = os.path.sep.join([yolo_dir, "yolov3.cfg"])

        # load the labels (as list), and model
        self.yolo = cv2.dnn.readNetFromDarknet(config_path, weights_path)

        # get the output layers
        self.layer_names = self.yolo.getLayerNames()
        self.layer_names = [self.layer_names[i - 1] for i in self.yolo.getUnconnectedOutLayers()]
        
        
        
    def find_ball(self, confidence_threshold = 0.3):
        #method for detecting ball on image
        #frame = imutils.resize(frame, width=500)
        blob = cv2.dnn.blobFromImage(self.frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.yolo_model.setInput(blob)
        layerOutputs = self.yolo_model.forward(self.layer_names)
        boxes = []
        confidences = []
        classIDs = []
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # get the class id and confidence for the object
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if confidence > confidence_threshold and classID == 32:
                    # get the bounding box for the object
                    (H, W) = self.frame.shape[:2]
                    box = detection[0:4] * np.array([W, H, W, H])
                    (x, y, width, height) = box.astype("int")
                    # update our list of bounding box coordinates, confidences, and class IDs
                    boxes.append([x, y, width, height])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        if len(confidences) > 0:
            (x, y, w, h) = boxes[np.argmax(confidences)]
            ball = {
                'x':x,
                'y':y,
                'w':W,
                'h':h
            }
        else:
            ball = {
                'x':0,
                'y':0,
                'w':0,
                'h':0
            }
        return ball
    
    def get_body_vectors(self):
        with self.mp_pose.Pose(
            static_image_mode=True, min_detection_confidence=0.5, model_complexity=2) as pose:
            # Convert the BGR image to RGB and process it with MediaPipe Pose.
            results = pose.process(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))

            # Draw pose landmarks.
            #print(f'Pose landmarks of {name}:')
            #annotated_image = frame.copy()
            self.mp_drawing.draw_landmarks(
                self.frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_styles.get_default_pose_landmarks_style())
            #annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
            
            
    def draw_on_image(self):
        cv2.circle(self.frame, 
                   center = (self.ball['x'], self.ball['y']), 
                   radius=int(self.ball['w']/2), color=(0,255,0), 
                   thickness=3)
        #annotated_image = image.copy()
        self.mp_drawing.draw_landmarks(
            self.frame,
            self.ball.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_styles.get_default_pose_landmarks_style())
            #annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)