import cv2
import numpy as np
import json
import time
import argparse
import imutils
import skimage.transform as transform


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--conf", default="./conf.json", help="path to JSON config file")
args = vars(parser.parse_args())

conf = json.load(open(args["conf"]))

camera = cv2.VideoCapture(0)
time.sleep(conf["camera_warmup_time"])
frameAvg = None

while True:
    (grabbed, frame) = camera.read()

    if not grabbed:
        break

    frame = imutils.resize(frame, height=conf["resolution"][0], width=conf["resolution"][1])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    if frameAvg is None:
        frameAvg = gray.copy().astype("float")
        continue

    cv2.accumulateWeighted(gray, frameAvg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(frameAvg))

    threshold = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)
    contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    for contour in contours:
        if cv2.contourArea(contour) < conf["min_area"]:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if conf["show_video"]:
            cv2.imshow("Security Feed", frame)
            cv2.imshow("Thresh", threshold)
            cv2.imshow("Frame Delta", frameDelta)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
camera.release()
cv2.destroyAllWindows()
