import numpy, cv2, os, sys
from scan1 import *
from chalkboard import *

frm=10
fps=30
period=20 # sec

width=640
height=360

CAM_LAPTOP = 1
CAM_DESKTOP = 0

DELTA_RANGE = period*fps

list_contain = []

def gray(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray

def doCapture(name_video, name_class, name_lesson, period):
	list_contain = []
	list_ratio = []
	list_frame = []
	
	if not os.path.isdir("./" + name_class + "/"):
		os.mkdir("./" + name_class + "/")
	if not os.path.isdir("./" + name_class + "/" + name_lesson + "/"):
		os.mkdir("./" + name_class + "/" + name_lesson + "/")

	camera = cv2.VideoCapture(name_video)
	_, frame1 = camera.read()
	_, frame2 = camera.read()
	temp = cv2.bitwise_xor(frame1, frame1)
	
	cc = list()
	picCount = 0
	framecount = 0
	
	while True:
		frame1 = frame2
		for i in range(frm):
			_, frame2 = camera.read()

		if not _:
			break
		
		gray1 = gray(frame1)
		gray2 = gray(frame2)
		dframe = cv2.absdiff(gray1, gray2)
		
		(_, mask) = cv2.threshold(dframe, 5, 255, cv2.THRESH_BINARY)
		mask = cv2.dilate(mask, None, iterations = 6)

		contours, hierarcy = cv2.findContours(mask, 1, 2) 

		cc.append(contours)
		if len(cc) > 5: cc.pop(0)
		
		for contours in cc:
			for c in contours:
				x, y, w, h = cv2.boundingRect(c)
				cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
		
		new = cv2.bitwise_and(frame2, frame2, mask = cv2.bitwise_not(mask))
		old = cv2.bitwise_and(temp, temp, mask = mask)
		temp = cv2.add(new, old)
		
		cv2.imshow('original video', frame1)
		cv2.imshow('delta frame', dframe)
		cv2.imshow('mask', mask)
		cv2.imshow('record', temp)
		opening = getChalkBoard(temp)

		list_ratio.append(getRatioPercent(opening))
		list_frame.append(temp)
		#framecount = framecount + 1
		#if framecount == (fps*period/frm):
			#temp = imgProcess(temp)
		
		trigger = localTrigger(list_ratio, list_frame, list_contain)
		if trigger != 0:
			cv2.imwrite((name_class+'/'+name_lesson+'/'+'save{0}.jpg').format(picCount), list_frame[trigger])
			framecount = 0
			picCount = picCount + 1
			print('Captured...')
			
		cv2.waitKey(15)
		
	camera.release()

def localTrigger(list_ratio, list_frame, list_contain):
	l = len(list_ratio)

	index_max = 0
	if l > DELTA_RANGE:
		for i in range(0, DELTA_RANGE):
			if list_ratio[l-DELTA_RANGE+i] > list_ratio[index_max]:
				index_max = l-DELTA_RANGE+i

	if list_contain==[] or index_max - list_contain[len(list_contain)-1] > DELTA_RANGE:
		list_contain.append(index_max)
		list_ratio = []
		list_frame = []
		return index_max
	else:
		return 0

'''		
	if index_max in list_contain:
		return 0
	else:
		list_contain.append(index_max)
		return index_max
'''
print('Capturing...')
l = len(sys.argv)
if l==1:
	doCapture(CAM_LAPTOP, 'myClass', '1', 10)
elif l==2:
	doCapture(CAM_LAPTOP, sys.argv[1], '1', 10)
elif l==3:
	doCapture(CAM_LAPTOP, sys.argv[1], sys.argv[2], 10)
elif l==4:
	doCapture(CAM_LAPTOP, sys.argv[1], sys.argv[2], int(sys.argv[3]))
elif l==5:
	doCapture(sys.argv[4], sys.argv[1], sys.argv[2], int(sys.argv[3]))

cv2.destroyAllWindows()
