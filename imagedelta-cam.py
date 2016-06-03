import numpy, cv2

#camera = cv2.VideoCapture("test5.mp4")
camera = cv2.VideoCapture(0)

_, frame1 = camera.read()
_, frame2 = camera.read()

temp = cv2.bitwise_xor(frame1,frame1)

def gray(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray

cc = list()

while True:
    frame1 = frame2
    for i in range(30): _, frame2 = camera.read()
    #if not _: break
    
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
    
    cv2.waitKey(1)

