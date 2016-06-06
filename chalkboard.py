import cv2
import numpy as np

THRESH_WHITE = 105
THRESH_BLACK = 130

originCheck = False
black_origin = -1

cap = False

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
	cap = captureTrigger(opening, black_origin)
	
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
	
def captureTrigger(frame, origin):
	blacks = cv2.inRange(frame, 0, 128)
	num = cv2.countNonZero(blacks)
	#print("total : " + str(frame.size))
	#print("blacks: " + str(num))
	background = frame.size - origin
	ratio = float(num-origin)/float(background)
	#print("num: "+str(num))
	#print("origin: "+str(origin))
	#print("background: "+str(background))
	#print("ratio: "+str(ratio*100)+" %")
	if ratio > 0.5:
		return True
	else:
		return False

#img = cv2.imread('chalkboard.jpg')
#getChalkBoard(img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
