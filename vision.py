import cv2
import numpy as np
import json
import time
import argparse
import imutils
from imutils.object_detection import non_max_suppression
import skimage.transform as transform


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--conf", default="./conf.json", help="path to JSON config file")
args = vars(parser.parse_args())

conf = json.load(open(args["conf"]))

# Capture images from webcam
camera = cv2.VideoCapture(0)
# Use HOGs for pedestrian detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

time.sleep(conf["camera_warmup_time"])
frameAvg = None
framesSinceMotion = 0
# Determining boundaries for the color red
lower = np.array(conf["green_boundary"][0], dtype="uint8")
upper = np.array(conf["green_boundary"][1], dtype="uint8")

while True:
    motionDetected = False

    (grabbed, frame) = camera.read()

    if not grabbed: # If it was not able to capture a photo, stop
        break

    # Image pre-processing
    frame = imutils.resize(frame, height=conf["resolution"][0], width=conf["resolution"][1])

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)


    if frameAvg is None: # Initialize frame average
        frameAvg = gray.copy().astype("float")
        continue

    # use a moving average of previous frames as the key frame to compare against
    cv2.accumulateWeighted(gray, frameAvg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(frameAvg))

    threshold = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)
    contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    for contour in contours:
        if cv2.contourArea(contour) < conf["min_delta_area"]:
            continue
        motionDetected = True

    framesSinceMotion = 0 if motionDetected else framesSinceMotion + 1

# Human Detection if there has been large motion
#     if framesSinceMotion < conf["max_frames_since_motion"]:
#         (rectangles, weights) = hog.detectMultiScale(frame, winStride=(5, 5),
#                                                 padding=(8, 8), scale=1.05)
#         rectangles = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rectangles])
#         suppressed = non_max_suppression(rectangles, probs=None, overlapThresh=conf["overlap_thresh"])
#
#         for (xA, yA, xB, yB) in suppressed:
#             cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

# Green ball detection
    if framesSinceMotion < conf["max_frames_since_motion"]:
        blurred = cv2.GaussianBlur(frame, (11,11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        center = None

        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            M = cv2.moments(contour)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > conf["min_radius"]:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

    if conf["show_video"]:
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Delta Thresh", threshold)
        cv2.imshow("Frame Delta", frameDelta)
        cv2.imshow("Green", mask)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
camera.release()
cv2.destroyAllWindows()
