# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
import time
import cv2
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

    
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

focalLength = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH
x, y, radius = None, None, None
old_x = None
old_y = None
old_radius = None
center = None
frameAvg = None
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
        
        #resize frame
        #image = imutils.resize(image, width = 300)

        #if frameAvg is None: # Initialize frame average
        #    frameAvg = image.copy().astype("float")
        #    continue





        # convert colr scheme
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)	
         
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
                                print()
                                #if ( (x-old_x)**2 + (y - old_y)**2 ) < (radius**2 + old_radius**2):
                                #        #print("End", c_int)
                                #        break
                                #        #else:
                                #        #c_int = np.argmax(cnts, key = cv2.contourArea)
                                #        #del cnts[c_int]
                                #else:
                                c_int -=1
                        #if s_int != c_int:
                        #        print("End", s_int, c_int)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > 5 :
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                        cv2.circle(image, center, 5, (0, 0, 255), -1)

                        inches = distance_to_camera(KNOWN_WIDTH, focalLength, radius)
                        print(inches)
                        cv2.putText(image, "%.2fcm" % (inches),
                                    (image.shape[1] - 200, image.shape[0] - 200), cv2.FONT_HERSHEY_SIMPLEX,
                                    2.0, (0, 255, 0), 3)
                       
                        print("Dist", inches, radius)
                        offset_x = image.shape[0]/2 - x
                        offset_y = image.shape[1]/2 - y
                        print("offset", offset_x, offset_y)
                    
                if x!= None:
                        #will start tracking after first image
                        old_x = x
                        old_y = y
                        #print("Old_radius", old_radius)
                        old_radius = radius
                        #print("radius", radius)  
                # if the `q` key was pressed, break from the loop
                #key = cv2.waitKey(1) 
                #if key == ord("q"):
                #        break
                #
        #add dist calculation

        # show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) #& 0xF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
                break
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)	#break
