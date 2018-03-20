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
greenUpper =  (215, 255, 152)  #(44, 255, 255) # 64
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

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
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
        if x ==None:
            cnts.sort( key= cv2.contourArea)
           
            c_int = len(cnts) -1
            c = cnts[c_int]
            ((x, y), radius) = cv2.minEnclosingCircle(c)
        #'''
        else:
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
                if ( (x-old_x)**2 + (y - old_y)**2 ) < (radius**2 + old_radius**2):
                    #print("End", c_int)
                    break
                #else:
                    #c_int = np.argmax(cnts, key = cv2.contourArea)
                    #del cnts[c_int]
                else:
                    c_int -=1
            if s_int != c_int:
                print("End", s_int, c_int)
        #'''
        #:w
        #focalLength = (radius * KNOWN_DISTANCE) / KNOWN_WIDTH
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        '''
        if old_x != None:
            # only proceed if the radius meets a minimum size   
            if radius > 10 and (((x-old_x)**2 + (y - old_y)**2 ) < (radius**2 + old_radius**2)):
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                inches = distance_to_camera(KNOWN_WIDTH, focalLength, radius)
                cv2.putText(frame, "%.2fcm" % (inches),
                (frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                2.0, (0, 255, 0), 3)
                # update the points queue
                pts.appendleft(center)
                
        else:
        '''
        if radius > 5 :
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            inches = distance_to_camera(KNOWN_WIDTH, focalLength, radius)
            print(inches)
            cv2.putText(frame, "%.2fcm" % (inches),
                        (frame.shape[1] - 200, frame.shape[0] - 200), cv2.FONT_HERSHEY_SIMPLEX,
                        2.0, (0, 255, 0), 3)
            # update the points queue
            pts.appendleft(center)
            print("Dist", inches, radius)
        
        if x!= None:
            #will start tracking after first image
            old_x = x
            old_y = y
            #print("Old_radius", old_radius)
            old_radius = radius
            #print("radius", radius)  
   
        #add dist calculation
    
    
    # loop over the set of tracked points
    for i in xrange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
            
            