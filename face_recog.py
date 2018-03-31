import cognitive_face as CF
import requests
from io import BytesIO
import numpy as np
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
filename1 = '/home/louiefu/Desktop/makentu/photo_Make/Joe/1.jpg'
filename2 = '/home/louiefu/Desktop/makentu/photo_Make/Cynthia/2.jpg'
filename3 = '/home/louiefu/Desktop/makentu/photo_Make/Louis/3.jpg'
filename4 = '/home/louiefu/Desktop/makentu/photo_Make/Pierre/4.jpg'
#test_file = '/home/louiefu/Desktop/makentu/photo_Make/Pierre/29893563_1724619870894340_1212997725_o.jpg'

files = [filename1, filename2, filename3, filename4]

results = []
for f in files:
    r = get_face_data(f)
    results.append(r)

all_faceid = [f['faceId'] for image in results for f in image]

#test_result = get_face_data(test_file)

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

print(str(recogize_result))



# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
#img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
#faces = CF.face.detect(img_url)
#print(faces)

#Convert width height to a point in a rectangle
#def getRectangle(faceDictionary):
#    rect = faceDictionary['faceRectangle']
#    left = rect['left']
#    top = rect['top']
#    bottom = left + rect['height']
#    right = top + rect['width']
#    return ((left, top), (bottom, right))

#Download the image from the url
#response = requests.get(img_url)
#img = Image.open(BytesIO(response.content))

#For each face returned use the face rectangle and draw a red box.
#draw = ImageDraw.Draw(img)
#for face in faces:
#    draw.rectangle(getRectangle(face), outline='red')

#Display the image in the users default image browser.
#img.show()
