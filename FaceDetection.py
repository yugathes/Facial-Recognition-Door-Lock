import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np 
import os
import sys

#Camera Resolution
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30

#Capture Variable
rawCapture = PiRGBArray(camera, size=(640, 480))

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

font = cv2.FONT_HERSHEY_SIMPLEX

#File to save images of a person
name = input("What's his/her Name? ")
dirName = "./images/" + name
print(dirName)
if not os.path.exists(dirName):
	os.makedirs(dirName)
	print("Directory Created")
else:
	print("Name already exists")
	sys.exit()

count = 1
#Continuous Capture Frame
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #Convert frame to grayscale
	if count > 30:
	    break
	frame = frame.array
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	#Face detect
	faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
	
	#Collecting Images from frames(30 images)
	for (x, y, w, h) in faces:
		print("Picture Taken = " + str(count))
		roiGray = gray[y:y+h, x:x+w]
		fileName = dirName + "/" + name + str(count) + ".jpg"
		cv2.imwrite(fileName, roiGray)
		cv2.imshow("face", roiGray)
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		cv2.putText(frame, count, (x, y), font, 2, (0, 0 ,255), 2,cv2.LINE_AA)
		count += 1
		
    #Output Image		
	cv2.imshow('frame', frame)
	key = cv2.waitKey(1)
	
	#Clear the stream
	rawCapture.truncate(0)

    #key for end	
	if key == 27:
		break
		
cv2.destroyAllWindows()

