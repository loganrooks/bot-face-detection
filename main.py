import cv2
import picamera
from picamera.array import PiRGBArray
from face_client import FaceClient
from faces import *

API_KEY = 'egk0ko9neatt4ftsgmhsmklf2r'
API_SECRET = '67doedp6s4dcnm5kmuhkgetj8p'
client = FaceClient(API_KEY, API_SECRET)
metrics = ['gender', 'mood', 'smiling', 'eyes']
domain_name = 'loganrookspi.ddns.net'
filename = "/var/www/html/temp.jpg"
img_addr = 'http://{}/temp.jpg'.format(domain_name)

resolution = (640, 480)

camera = picamera.PiCamera()
camera.resolution = resolution
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=resolution)
time.sleep(2)

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True, ):
    frame = f.array
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    descriptions = recognize_faces(img_addr, client, metrics)

