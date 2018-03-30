import picamera
from picamera.array import PiRGBArray
from SimpleCV import Image
import cv2
import commands
import io
import socket
import time
import imutils
from face_client import FaceClient

API_KEY = 'egk0ko9neatt4ftsgmhsmklf2r'
API_SECRET = '67doedp6s4dcnm5kmuhkgetj8p'
client = FaceClient(API_KEY, API_SECRET)
metrics = ['gender', 'mood', 'smiling', 'eyes']

def extract_identity(uids, threshold):
    max_confidence = 0
    identity = None
    for id_ in uids:
        confidence = id_['confidence']
        if confidence > threshold and confidence > max_confidence:
            identity = id_['uid']
            max_confidence = confidence
    return identity

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def recognize_faces(img, client, metrics):
    response = client.faces_recognize('all', img, namespace='projectfaces')  
    faces = response['photos'][0]['tags']
    face_descriptions = []
    for face in faces:
        attributes = face['attributes']
        threshold = face['threshold']
        if attributes['face']['confidence'] > (threshold-10) and attributes['face']['value'] == 'true': 
            description = merge_two_dicts(
                {
                'center': face['center'], \
                'identity': extract_identity(face['uids'], threshold), \
                },
                {
                metric: attributes[metric]['value'] if \
                attributes[metric]['confidence'] > threshold \
                else None for metric in metrics
                })
            face_descriptions.append(description)
    return face_descriptions


domain_name = 'loganrookspi.ddns.net'
filename = "/var/www/html/temp.jpg"
client = FaceClient(API_KEY, API_SECRET)
img_addr = 'http://{}/temp.jpg'.format(domain_name)

resolution = (640, 480)

camera = picamera.PiCamera()
camera.resolution = resolution
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=resolution)
time.sleep(2)

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True,):
    frame = f.array
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    descriptions = recognize_faces(img_addr, client, metrics)

print descriptions



    

