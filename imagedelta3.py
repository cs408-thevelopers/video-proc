import numpy, cv2, os, sys

frm=10
fps=30
period=20 # Default period: 20 sec

width=640
height=360

CAM_LAPTOP = 1
CAM_DESKTOP = 0

def gray(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray

def doCapture(name_video, name_class, name_lesson, period):

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

		framecount = framecount + 1
		if framecount == (fps*period/frm):
			cv2.imwrite((name_class+'/'+name_lesson+'/'+'save{0}.jpg').format(picCount), temp)
			framecount = 0
			picCount = picCount + 1
			print('Captured...')
			
		cv2.waitKey(1)
		
	camera.release()
	
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
	doCapture(int(sys.argv[4]), sys.argv[1], sys.argv[2], int(sys.argv[3]))

cv2.destroyAllWindows()


    
