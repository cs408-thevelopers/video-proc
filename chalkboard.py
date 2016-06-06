import cv2
import numpy as np

THRESH_WHITE = 105
THRESH_BLACK = 130

originCheck = False
black_origin = -1

def getChalkBoard(frame):
	global originCheck, black_origin
	frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	cv2.imshow('gray', frame2)
	
	ret, thresh1 = cv2.threshold(frame2, THRESH_BLACK, 255, cv2.THRESH_BINARY_INV)
	
	cv2.imshow('thresh1', thresh1)
	
	kernel = np.ones((5,5), np.uint8)
	erosion = cv2.erode(thresh1, kernel, iterations=1)
	
	opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
	
	if not originCheck:
		black_origin = getDefaultTrigger(opening)
		originCheck = True
		
	cv2.imshow('opening', opening)
	
	return opening

def getDefaultTrigger(frame):
	return getBlacks(frame)
	
def getBlacks(frame):
	blacks = cv2.inRange(frame, 0, 128)
	num = cv2.countNonZero(blacks)
	return num
	
def getRatioPercent(frame):
	global black_origin
	background = frame.size - black_origin
	num_black = getBlacks(frame)
	return 100*float(num_black - black_origin)/float(background)
	
