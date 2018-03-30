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




    
