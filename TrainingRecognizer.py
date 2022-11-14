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
buzzer = [26]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

GPIO.setup(buzzer, 0)
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

		id_, loss = recognizer.predict(roiGray)
		conf = 100-loss
		
        #Look in dictionary 
		for name, value in dicti.items():
			if value == id_:
				print("Name : " + name + " --- Confidence : " + str(conf))
				#Rectangle frame will output
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
				cv2.putText(frame, name + str(loss), (x, y), font, 2, (0, 0 ,255), 2,cv2.LINE_AA)

        #Check lossidence, If <70 the doors open
		if loss <= 70:
			GPIO.output(relay, 1)
			GPIO.output(green, 1)
			GPIO.output(red, 0)
			GPIO.output(buzzer, 1)
			print("Door Unlock")
			print("In 10 seconds Door Lock again")
			sleep(10)			
			GPIO.output(relay,0)
			GPIO.output(green,0)
			GPIO.output(buzzer, 0)			

		else:
			GPIO.output(relay, 0)
			GPIO.output(red, 1)
			GPIO.output(buzzer, 0)

	cv2.imshow('frame', frame)
	key = cv2.waitKey(1)

	rawCapture.truncate(0)

	if key == 27:
		GPIO.output(red, 0)
		GPIO.output(yellow, 0)
		GPIO.output(relay, 0)
		GPIO.output(green, 0)
		GPIO.output(buzzer, 0)
		break

cv2.destroyAllWindows()
