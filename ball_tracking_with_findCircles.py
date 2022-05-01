'''
@author: Matthew Fuss

The purpose of this script is to take video input from camera and
allow for real time adjustment of various types of filtering/processing 
thresholds. Multiple windows will appear with adjustable sliders and
will also show the input image. The goal is to adjust the values until 
the desired object(in this case a basketball) is being identified. Those
values can then be recorded and used


'''
import cv2
import numpy as np

kernel = np.ones((5,5),np.uint8)

# Take input from webcam
cap = cv2.VideoCapture(0)

# Reduce the size of video to 320x240 so rpi can process faster
cap.set(3,320)
cap.set(4,240)

cv2.namedWindow('HueComp')
cv2.namedWindow('SatComp')
cv2.namedWindow('ValComp')
cv2.namedWindow('closing')
cv2.namedWindow('tracking')


# Creating track bar for min and max for hue, saturation and value
# You can adjust the defaults as you like

#define blank method because one is required for trackbar method
def nothing(input):
    pass

cv2.createTrackbar('hmin', 'HueComp', 174, 255, nothing)
cv2.createTrackbar('hmax', 'HueComp', 247, 255, nothing)

cv2.createTrackbar('smin', 'SatComp', 74, 255, nothing)
cv2.createTrackbar('smax', 'SatComp', 144, 255, nothing)

cv2.createTrackbar('vmin', 'ValComp', 38, 255, nothing)
cv2.createTrackbar('vmax', 'ValComp', 191, 255, nothing) 

# My experimental values
# hmn = 12
# hmx = 37
# smn = 145
# smx = 255
# vmn = 186
# vmx = 255

try:
    while(1):
        buzz = 0
        _, frame = cap.read()

        #converting to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #looking for the color orange and bright parts of image
        #hsv_orange = cv2.inRange(hsv, (7,180,180), (11, 255, 255))
        
        hue,sat,val = cv2.split(hsv)

        # get info from track bar and appy to result
        hmn = cv2.getTrackbarPos('hmin','HueComp')
        hmx = cv2.getTrackbarPos('hmax','HueComp')


        smn = cv2.getTrackbarPos('smin','SatComp')
        smx = cv2.getTrackbarPos('smax','SatComp')


        vmn = cv2.getTrackbarPos('vmin','ValComp')
        vmx = cv2.getTrackbarPos('vmax','ValComp')

        # Apply thresholding
        hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
        sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
        vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))

        # AND h s and v
        tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))
        
        # Some morpholigical filtering
        dilation = cv2.dilate(tracking,kernel,iterations = 1)
        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
        closing = cv2.GaussianBlur(closing,(5,5),0)

        # Detect circles using HoughCircles
        circles = cv2.HoughCircles(closing,cv2.HOUGH_GRADIENT,2,120,param1=120,param2=50,minRadius=5,maxRadius=0)
        # circles = np.uint16(np.around(circles))

        #Draw Circles
        if circles is not None:
                for i in circles[0,:]:
                    # If the ball is far, draw it in green
                    if int(round(i[2])) < 30:
                        cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,255,0),5)
                        cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,255,0),10)
                    # else draw it in red
                    elif int(round(i[2])) > 35:
                        cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,0,255),5)
                        cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,0,255),10)
                        buzz = 1
        
        #Show the result in frames
        cv2.imshow('HueComp',hthresh)
        cv2.imshow('SatComp',sthresh)
        cv2.imshow('ValComp',vthresh)
        cv2.imshow('closing',closing)
        cv2.imshow('tracking',frame) 

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
finally:
    cap.release()
    cv2.destroyAllWindows()
    
