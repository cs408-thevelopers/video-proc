import imutils
import cv2
import numpy as np

#camera = cv2.VideoCapture(0)
camera = cv2.VideoCapture("test2.mp4")
time.sleep(0.25)
 
firstFrame = None

while True:
	for i in range(10):
		(grabbed, frame) = camera.read()
 
	if not grabbed:
		break

	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	if firstFrame == None:
		firstFrame = gray
		continue

	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 10, 255, cv2.THRESH_BINARY)[1]
 
	firstFrame = gray
	
	# gather the pixels which are invariant
		

	cv2.imshow("Original", frame)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()
