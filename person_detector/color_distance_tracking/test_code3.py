# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
 
    
    
    
def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth
    
# initialize the known distance from the camera to the object, which
KNOWN_DISTANCE = 30.0 # cm
 
# initialize the known object width, which in this case, the piece of
KNOWN_WIDTH = 4.5 # cm

KNOWN_PIXEL_WIDTH = 50 #15#250 # px
    
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

#greenLower = (58, 162, 45) #(29, 86, 6)
#greenUpper =  (215, 255, 152)  #(44, 255, 255) # 64
pts = deque([10])


# because it can get confused, track old position, and limit
# how much the new position can deviate from the first

#select video path
camera = cv2.VideoCapture("test_video_silent.mp4")
focalLength = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH
x, y, radius = None, None, None
old_x = None
old_y = None
old_radius = None
center = None
# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    # frame shape is 1280, 720
    
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    frame = imutils.resize(frame, width=600)
    #scaled down to 1066*600
    #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform a series of 
    # dilations and erosions to remove any small blobs left in the mask
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
        # centroid add check to ensure that the area overlaps

        # During the first iteration, take max contour
        if x ==None:
            cnts.sort( key= cv2.contourArea)
            c = cnts[-1]
            ((x, y), radius) = cv2.minEnclosingCircle(c)
        else:
            #iterate over contours, take one that overlaps with old contour
            cnts.sort( key= cv2.contourArea)
            c_int = len(cnts) -1
            s_int = c_int
            #work your way down
            while c_int >=0 :

                c = cnts[c_int]
                
                # x will be first given a non None value here
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                #if its within old circle, keep it
                if ( (x-old_x)**2 + (y - old_y)**2 ) < (radius**2 + old_radius**2):
                    #print("End", c_int)
                    break
                #else:
                    #c_int = np.argmax(cnts, key = cv2.contourArea)
                    #del cnts[c_int]
                else:
                    c_int -=1
            

        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        #print(center)
        #'''
        #this means that the contour wont be shown for the very first image
        if old_x != None:
            # only proceed if the radius meets a minimum size   
            if radius > 10 and (((x-old_x)**2 + (y - old_y)**2 ) < (radius**2 + old_radius**2)):
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                #distance calculation
                inches = distance_to_camera(KNOWN_WIDTH, focalLength, radius)
                cv2.putText(frame, "%.2fcm" % (inches),
                (frame.shape[1] - 190, frame.shape[0] - 150), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 255, 0), 3)
                #offset_x = frame.shape[0] 
                
                
                offset_x = frame.shape[0]/2 - x
                offset_y = frame.shape[1]/2 - y
                print("offset", offset_x, offset_y)

        if x!= None:
            #will start tracking after first image
            old_x = x
            old_y = y
            #print("Old_radius", old_radius)
            old_radius = radius
            #print("radius", radius)  
   
    

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
            
            