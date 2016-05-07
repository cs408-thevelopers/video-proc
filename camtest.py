import datetime
import imutils
import time
import cv2
 
#camera = cv2.VideoCapture(0)
camera = cv2.VideoCapture("disjointset.mp4")
time.sleep(0.25)
 
firstFrame = None

while True:
	(grabbed, frame) = camera.read()
 
	if not grabbed:
		break

	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	
	if firstFrame == None:
		firstFrame = gray
		continue

	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 40, 255, cv2.THRESH_BINARY)[1]
 
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
 
	for c in cnts:
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
 
	firstFrame = gray
	
	cv2.imshow("Original", frame)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()
