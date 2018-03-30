# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
import time
import cv2
import serial
import time


def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth

def calculate_distance(ref_frame, known_width, known_distance):
    gray = cv2.cvtColor(ref_image, cv2)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
    cnts, bounds, val = cv2.findContours(edged.copy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = max(bounds, key = cv2.contourArea)
    pixel_width = cv2.minEnclosingCircle(c)
    return pixel_width

def tracking(frame, greenboundary, consts = {}, KNOWN_WIDTH = 7, KNOWN_DISTANCE = 30):
    # pass in a frame o    # capture frames from the camera
    #for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
    KNOWN_PIXEL_WIDTH = calculate_distance(frame, KNOWN_WIDTH, KNOWN_DISTANCE)   
    
    #KNOWN_PIXEL_WIDTH = 50 #15#250 # px
    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)
    focalLength = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH
    
    x, y, radius = None, None, None
    center = None
     
    # convert colr scheme
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         
    # construct a mask for the color "green", then perform a series of 
    # dilations and erosions to remove any small blobs left in the mask
    green_lower, green_upper = greenboundary
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]  
    center = None
        
        
    # only proceed if at least one contour was found
    if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    # add check to ensure that the area overlaps
    #print( len(cnts))
    if x == None:
        cnts.sort( key= cv2.contourArea)              
        c_int = len(cnts) -1
        c = cnts[c_int]
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        #'''
    else:
        #due to current code structure, this will never run it'll always go through the if statement        
        #iterate over contours, take one that overlaps with old tracker
        cnts.sort( key= cv2.contourArea)
        c_int = len(cnts) -1
        #print("Start", c_int)
        s_int = c_int
        while c_int >=0 :

            c = cnts[c_int]
            
            # x will be first given a non None value here
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            #if its within old circle, keep it
            print()
            c_int -=1
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    if radius > 5 :
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
        cv2.circle(image, center, 5, (0, 0, 255), -1)

        distance = distance_to_camera(KNOWN_WIDTH, focalLength, radius)

                
        offset_x = image.shape[0]/2 - x
        offset_y = image.shape[1]/2 - y
#        print("offset", offset_x, offset_y)
        return distance, offset_x, offset_y
        

        

