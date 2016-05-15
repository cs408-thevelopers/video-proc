
import numpy as np
import cv2
from matplotlib import pyplot as plt

fast = cv2.FastFeatureDetector(threshold = 15);

cap = cv2.VideoCapture('./test1.mp4')
#cap = cv2.VideoCapture(0)

while(True):

	ret, frame = cap.read()
	kp = fast.detect(frame, None)
	frame2 = cv2.drawKeypoints(frame, kp, color=(255, 0, 0))
	
	cv2.imshow('frame', frame2)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()

