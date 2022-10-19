import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np 
import pickle
import RPi.GPIO as GPIO
from time import sleep

relay = [14]
green = [20]
yellow = [21]
red = [16]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.output(relay, 0)
GPIO.output(green, 0)
GPIO.output(yellow, 0)
GPIO.output(red, 0)

#We load pickle file
with open('labels', 'rb') as f:
	dicti = pickle.load(f)
	f.close()

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

#Load the classifier
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

font = cv2.FONT_HERSHEY_SIMPLEX

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	GPIO.output(yellow, 1)
	frame = frame.array
	#Read Frame and convert it to grayscale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
	for (x, y, w, h) in faces:
		roiGray = gray[y:y+h, x:x+w]

		id_, conf = recognizer.predict(roiGray)
		
        #Look in dictionary 
		for name, value in dicti.items():
			if value == id_:
				print(name)
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
				cv2.putText(frame, name + str(conf), (x, y), font, 2, (0, 0 ,255), 2,cv2.LINE_AA)

        #Check confidence, If <70 the doors open
		if conf <= 70:
			GPIO.output(relay, 1)
			GPIO.output(green, 1)
			print("Door Unlock")			
			#Rectangle frame will output
			

		else:
			GPIO.output(relay, 0)
			GPIO.output(red, 1)

	cv2.imshow('frame', frame)
	key = cv2.waitKey(1)

	rawCapture.truncate(0)

	if key == 27:
		break

cv2.destroyAllWindows()
