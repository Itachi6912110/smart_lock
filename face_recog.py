import cognitive_face as CF
import requests
from io import BytesIO
import numpy as np
import motor_run
from time import sleep
import cv2

KEY = '81584f93ae644d1497bb4982d5ff6ef9'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)
# If you need to, you can change your base API url with:
#CF.BaseUrl.set('https://westcentralus.api.cognitive.microsoft.com/face/v1.0/')

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)


def get_face_data(filename):
	headers = {
    	'Content-Type': 'application/octet-stream',
     	'Ocp-Apim-Subscription-Key': KEY,
	}
	params = {
    	'returnFaceId': 'true',
	}
	path_to_face_api = '/detect'
	with open(filename, 'rb') as f:
		img_data = f.read()
	response = requests.post(BASE_URL + path_to_face_api,
    	                     data=img_data, 
        	                 headers=headers,
            	             params=params)
	parsed = response.json()
	print(parsed)
	return parsed

def get_face_data_img(img):
	headers = {
    	'Content-Type': 'application/octet-stream',
     	'Ocp-Apim-Subscription-Key': KEY,
	}
	params = {
    	'returnFaceId': 'true',
	}
	path_to_face_api = '/detect'
	response = requests.post(BASE_URL + path_to_face_api,
    	                     data=img, 
        	                 headers=headers,
            	             params=params)
	parsed = response.json()
	print(parsed)
	return parsed

def show_webcam():
    cam = cv2.VideoCapture(0)
    ret_val, img = cam.read()
    cv2.imwrite('test.jpg', img)
    _, img = cv2.imencode('.jpg', img)
    return img.tostring()

#################################################
filename1 = '/home/pi/smart_lock/photo_Make/Joe/1.jpg'
filename2 = '/home/pi/smart_lock/photo_Make/Cynthia/2.jpg'
filename3 = '/home/pi/smart_lock/photo_Make/Louis/3.jpg'
filename4 = '/home/pi/smart_lock/photo_Make/Pierre/4.jpg'

files = [filename1, filename2, filename3, filename4]

results = []
for f in files:
    r = get_face_data(f)
    results.append(r)

all_faceid = [f['faceId'] for image in results for f in image]


req_count = 5   # To avoid violate max request send, only do 5 times
while(req_count): 
    # return recognize result, 0: no match; 1: Joe; 2: Cynthia; 3: Louis; 4: Pierre
    recogize_result = 0

    test_img = show_webcam()
    test_result = get_face_data_img(test_img)
    if len(test_result) != 0:
        test_faceId = test_result[0]['faceId']
        sim_face = 1
        max_confidence = 0
        for f in all_faceid:
            r = CF.face.verify(f, test_faceId)
            print(r)
            if r['isIdentical'] and r['confidence']>max_confidence:
        	    recogize_result = sim_face
        	    max_confidence = r['confidence']
            sim_face += 1

    print (str(recogize_result))

    open_door()
    
    #control slipper cars
    if recogize_result == '0': #nobody
        pass
    elif recogize_result == '1': #Joe
        slipper_1_out()
        sleep(3)
        slipper_1_in()
    elif recogize_result == '2': #Cynthia
        slipper_2_out()
        sleep(3)
        slipper_2_in()
    elif recogize_result == '3': #Louis
        slipper_3_out()
        sleep(3)
        slipper_3_in()
    else:
        pass
    
    req_count -= 1