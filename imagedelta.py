# coding: utf-8
import numpy, cv2

camera = cv2.VideoCapture("test4.mp4")

_, frame1 = camera.read()
_, frame2 = camera.read()

temp = cv2.bitwise_xor(frame1,frame1)

def gray(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	return gray

def add_image(frame, dframe, temp):
    (_, mask) = cv2.threshold(dframe, 1, 255, cv2.THRESH_BINARY)

    new = cv2.bitwise_and(frame, frame, mask = cv2.bitwise_not(mask))
    old = cv2.bitwise_and(temp, temp, mask = mask)
    temp = cv2.add(new, old)
    return temp

for i in range(600): _, frame2 = camera.read()

while True:
    frame1 = frame2
    for i in range(10): _, frame2 = camera.read()
    if not _:
        break
    
    gray1 = gray(frame1)
    gray2 = gray(frame2)
    dframe = cv2.absdiff(gray1, gray2)
    
    (_, mask) = cv2.threshold(dframe, 2, 255, cv2.THRESH_BINARY)
    mask = cv2.dilate(mask, None, iterations = 4)

    contours, hierarcy = cv2.findContours(mask, 1, 2) 
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w * h >= 50:
            cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
    
    new = cv2.bitwise_and(frame2, frame2, mask = cv2.bitwise_not(mask))
    old = cv2.bitwise_and(temp, temp, mask = mask)
    temp = cv2.add(new, old)
	
	cv2.imshow('record', temp)
	cv2.imshow('original video', frame1)
	cv2.imshow('delta frame', dframe)
	cv2.imshow('mask', mask); cv2.waitKey(1)

