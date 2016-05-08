
# coding: utf-8

# In[1]:

import numpy, cv2


# In[2]:

camera = cv2.VideoCapture("test3.mp4")


# In[3]:

_, frame1 = camera.read()
_, frame2 = camera.read()


# In[4]:

temp = cv2.bitwise_xor(frame1,frame1)


# In[5]:

def gray(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (25, 25), 0)
    return gray


# In[6]:

def add_image(frame, dframe, temp):
    (_, mask) = cv2.threshold(dframe, 1, 255, cv2.THRESH_BINARY)

    new = cv2.bitwise_and(frame, frame, mask = cv2.bitwise_not(mask))
    old = cv2.bitwise_and(temp, temp, mask = mask)
    temp = cv2.add(new, old)
    return temp


# In[7]:
height , width , layers =  frame1.shape

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # note the lower case
fps = 15

video = cv2.VideoWriter('video.avi', fourcc, fps, (width,height))

while True:
    frame1 = frame2
    for i in range(10): _, frame2 = camera.read()
    if not _:
        break
    
    gray1 = gray(frame1)
    gray2 = gray(frame2)
    dframe = cv2.absdiff(gray1, gray2)
    
    temp = add_image(frame2, dframe, temp)
    
    video.write(temp)

video.release()
