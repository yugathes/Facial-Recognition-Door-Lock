import os
import numpy as np 
from PIL import Image 
import cv2
import pickle

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#Recognizer for face
recognizer = cv2.face.LBPHFaceRecognizer_create()

#Going into images directory
baseDir = os.path.dirname(os.path.abspath(__file__))
imageDir = os.path.join(baseDir, "images")

currentId = 1
labelIds = {}
yLabels = []
xTrain = []

#Looking for images in directory
for root, dirs, files in os.walk(imageDir):
	print(root, dirs, files)
	for file in files:
		print(file)
		if file.endswith("png") or file.endswith("jpg"):
			path = os.path.join(root, file)
			label = os.path.basename(root)
			print(label)

			if not label in labelIds:
				labelIds[label] = currentId
				print(labelIds)
				currentId += 1

			id_ = labelIds[label]
			pilImage = Image.open(path).convert("L")
			imageArray = np.array(pilImage, "uint8")
			
			#Again face detection and prepare trainer
			faces = faceCascade.detectMultiScale(imageArray, scaleFactor=1.1, minNeighbors=5)

			for (x, y, w, h) in faces:
				roi = imageArray[y:y+h, x:x+w]
				xTrain.append(roi)
				yLabels.append(id_)

#Store the dictionary
with open("labels", "wb") as f:
	pickle.dump(labelIds, f)
	f.close()

#Train the data
recognizer.train(xTrain, np.array(yLabels))
recognizer.save("trainer.yml")
print(labelIds)