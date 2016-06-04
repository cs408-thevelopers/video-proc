import numpy, cv2
from matplotlib import pyplot as plt
import datetime

#video input
filename = "test2.mp4"
camera = cv2.VideoCapture(filename)
fps = camera.get(cv2.cv.CV_CAP_PROP_FPS)
_, frame1 = camera.read()
width, height = frame1.shape[:2]
temp = cv2.bitwise_xor(frame1,frame1)
t = datetime.datetime.now()

# constant
startsecond = 20
captureinterval = 60
frameskipping = 20
linethickness = 5
contourlimit = 3
colorthresh = 7
gaussianradius = 5 # odd number
dilateiteration = 5

#relative variable
minimumwidth = (45 * width / 360)
framelimit = int(round(captureinterval * fps / frameskipping))
#print framelimit

for i in range(int(round(startsecond * fps))):
    _, frame1 = camera.read()
_, frame2 = camera.read()

# gray : colored frame -> grayscale frame
# grayscale frame is transformed by gaussian blur
def gray(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (gaussianradius, gaussianradius), 0)
    return gray

# iterating varaibles
framecount = recordcount = 0
contourset = list()

while True:
    # frame iterating
    frame1 = frame2
    for i in range(frameskipping):_, frame2 = camera.read()
    framecount += 1
    #print framecount
    
    #if the next frame is not valid, stop iteration
    if not _:break
    
    #finding a difference of the frame
    dframe = cv2.absdiff(gray(frame1), gray(frame2))
    
    # relative thresholding by neighbor pixels
    #th2 = cv2.adaptiveThreshold(dframe,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,4)
    #th2 = cv2.bitwise_not(th2)
    
    (_, mask) = cv2.threshold(dframe, colorthresh, 255, cv2.THRESH_BINARY)
    mask = cv2.dilate(mask, None, iterations = dilateiteration)
    
    # find a contour sets from the image; which is the border of the moving person
    contours, _ = cv2.findContours(mask, 1, 2) 
    contourset.append(contours)
    if len(contourset) > contourlimit: contourset.pop(0)
    
    
    mask = cv2.bitwise_xor(mask, mask)
    for contours in contourset:
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w >= minimumwidth:
				cv2.rectangle(mask, (x, y), (x + w, height - 1), 255, -1)
				cv2.rectangle(mask, (x, y), (x + w, height - 1), 255, 2*linethickness)
	
	# combine current and updated background
    new = cv2.bitwise_and(frame2, frame2, mask = cv2.bitwise_not(mask))
    old = cv2.bitwise_and(temp, temp, mask = mask)
    temp = cv2.add(new, old)
    
    cv2.imshow('original video', frame2)
    cv2.imshow('mask', mask)
    cv2.imshow('record', temp)
    #cv2.imshow('chalkboard_density', density)

    if framecount >= framelimit: 
        u = datetime.datetime.now()
        density = cv2.adaptiveThreshold(gray(temp),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        cv2.imwrite("result/result_%s_%s.png" % (filename, ('0000' + str(recordcount))[-4:]), temp)
        cv2.imwrite("difference/diff_%s_%s.png" % (filename, ('0000' + str(recordcount))[-4:]), density)
        print u - t,
        print "color of frame %s: " % recordcount,
        print cv2.mean(density)[0]
        t = u
        framecount = 0
        recordcount += 1
    
    cv2.waitKey(1)


u = datetime.datetime.now()
density = cv2.adaptiveThreshold(gray(temp),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
cv2.imwrite("result/result_%s_%s.png" % (filename, ('0000' + str(recordcount))[-4:]), temp)
cv2.imwrite("difference/diff_%s_%s.png" % (filename, ('0000' + str(recordcount))[-4:]), density)
print u - t,
print "color of frame %s: " % recordcount,
print cv2.mean(density)[0]
