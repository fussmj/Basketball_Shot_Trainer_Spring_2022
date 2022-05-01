import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#hsv_orange = cv2.inRange(hsv, (7,180,180), (11, 255, 255))

cv2.namedWindow('HueComp')
cv2.namedWindow('SatComp')
cv2.namedWindow('ValComp')
cv2.namedWindow('Enable')
cv2.namedWindow('Erosion and Dilation')


def nothing(input):
    pass
cv2.createTrackbar('hmin', 'HueComp', 120, 255, nothing)
cv2.createTrackbar('hmax', 'HueComp', 130, 255, nothing)

cv2.createTrackbar('smin', 'SatComp', 85, 255, nothing)
cv2.createTrackbar('smax', 'SatComp', 180, 255, nothing)

cv2.createTrackbar('vmin', 'ValComp', 85, 255, nothing)
cv2.createTrackbar('vmax', 'ValComp', 180, 255, nothing) 

cv2.createTrackbar('erosionArraySize1', 'Erosion and Dilation', 5, 20, nothing)
cv2.createTrackbar('dilationArraySize1', 'Erosion and Dilation', 5, 20, nothing)


cv2.createTrackbar('test', 'Enable', 1, 1, nothing)

cv2.createTrackbar('blur', 'Erosion and Dilation', 2, 10, nothing)

cv2.createTrackbar('iterations', 'Erosion and Dilation', 1, 10, nothing)






try:
    while(1):

        # Take each frame
        _, im = cap.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
        
        #get 3 variables for adjusting individually
        hue,sat,val = cv2.split(hsv)

        #get tracker bar values
        hmn = cv2.getTrackbarPos('hmin','HueComp')
        hmx = cv2.getTrackbarPos('hmax','HueComp')

        smn = cv2.getTrackbarPos('smin','SatComp')
        smx = cv2.getTrackbarPos('smax','SatComp')

        vmn = cv2.getTrackbarPos('vmin','ValComp')
        vmx = cv2.getTrackbarPos('vmax','ValComp')
        
        erosion_size = cv2.getTrackbarPos('erosionArraySize1','Erosion and Dilation')
        dilation_size = cv2.getTrackbarPos('dilationArraySize1','Erosion and Dilation')
        
        blur_size = 2*cv2.getTrackbarPos('blur','Erosion and Dilation') + 1
        
        iterations = cv2.getTrackbarPos('iterations','Erosion and Dilation')
        
        morphex = cv2.getTrackbarPos('test','Enable')
        
        #adjust outputs based on updated tracker bar values
        hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
        sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
        vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))
        
        lower = np.array([hmn,smn,vmn])
        upper = np.array([hmx,smx,vmx])

        # Threshold the HSV image to get only orange colors
        
        mask = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))
        #mask = cv2.inRange(hsv, lower, upper)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(im,im, mask= mask)
        
        # Perform opening to remove smaller elements
        erosion = np.ones((erosion_size,erosion_size)).astype(np.uint8)
        dilation = np.ones((dilation_size,dilation_size)).astype(np.uint8)
        
        im_hsv = mask.copy()
        
        for i in range(iterations):
            im_hsv = cv2.erode(im_hsv, erosion)
            im_hsv = cv2.dilate(im_hsv, dilation)
        
        if morphex == 1:
            kernel = np.ones((blur_size,blur_size),np.uint8)
            im_hsv = cv2.morphologyEx(im_hsv, cv2.MORPH_CLOSE, kernel,iterations=iterations)
        
        im_hsv = cv2.GaussianBlur(im_hsv,(blur_size,blur_size),0)

        points = np.dstack(np.where(im_hsv>0)).astype(np.float32)
        # fit a bounding circle to the orange points
        center, radius = cv2.minEnclosingCircle(points)
        # draw this circle
        #cv2.circle(im, (int(center[1]), int(center[0])), int(radius), (255,0,0), thickness=3) 
        
        # Detect circles using HoughCircles
        circles = cv2.HoughCircles(im_hsv,cv2.HOUGH_GRADIENT,2,120,param1=120,param2=50,minRadius=5,maxRadius=0)
        
        #Draw Circles
        if circles is not None:
            for i in circles[0,:]:
                # If the ball is far, draw it in green
                if int(round(i[2])) < 30:
                    cv2.circle(im,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,255,0),5)
                    cv2.circle(im,(int(round(i[0])),int(round(i[1]))),2,(0,255,0),10)
                # else draw it in red
                elif int(round(i[2])) > 35:
                    cv2.circle(im,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,0,255),5)
                    cv2.circle(im,(int(round(i[0])),int(round(i[1]))),2,(0,0,255),10)
                    buzz = 1
        
        
        cv2.imshow('HueComp',hthresh)
        cv2.imshow('SatComp',sthresh)
        cv2.imshow('ValComp',vthresh)
        cv2.imshow('Erosion and Dilation',im_hsv)
        cv2.imshow('Final',im)
        
        

        if cv2.waitKey(5) == ord('q'):
            break

finally:
    cv2.destroyAllWindows()
    cap.release()
        



""" import cv2
import numpy as np

# My experimental values
hmn = 12
hmx = 37
smn = 145
smx = 255
vmn = 186
vmx = 255

#define blank method because one is required for trackbar method
def nothing(input):
    pass

cv2.createTrackbar('hmin', 'HueComp', 174, 255, nothing)
cv2.createTrackbar('hmax', 'HueComp', 247, 255, nothing)

cv2.createTrackbar('smin', 'SatComp', 74, 255, nothing)
cv2.createTrackbar('smax', 'SatComp', 144, 255, nothing)

cv2.createTrackbar('vmin', 'ValComp', 38, 255, nothing)
cv2.createTrackbar('vmax', 'ValComp', 191, 255, nothing) 

#get camera input
vidStream = cv2.VideoCapture(0)
cv2.waitKey(1000)


try:
    while(1):
        _, im = vidStream.read()

        # convert to HSV space
        im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        # take only the orange, highly saturated, and bright parts
        mins = (hmn,smn,vmn)
        maxes = (hmx,smx,vmx)
        im_hsv = cv2.inRange(im_hsv, mins, maxes)

        # To show the detected orange parts:
        im_orange = im.copy()
        im_orange[im_hsv==0] = 0
        # cv2.imshow('im_orange',im_orange)

        # Perform opening to remove smaller elements
        element = np.ones((5,5)).astype(np.uint8)
        im_hsv = cv2.erode(im_hsv, element)
        im_hsv = cv2.dilate(im_hsv, element)

        points = np.dstack(np.where(im_hsv>0)).astype(np.float32)
        # fit a bounding circle to the orange points
        center, radius = cv2.minEnclosingCircle(points)
        # draw this circle
        cv2.circle(im, (int(center[1]), int(center[0])), int(radius), (255,0,0), thickness=3)

        out = np.vstack([im_orange, im])
        cv2.imshow('out', out)  
"""