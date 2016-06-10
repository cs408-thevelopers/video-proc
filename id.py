import numpy, cv2, os, glob, sys
from chalkboard import *
from to_pdf import *
import zipfile, requests

frm=10 # frame numbers to be skipped(almost meaning combined)
fps=30 # fps of the video, or webcam
period=20 # sec

width=640
height=360

# The external webcam's default number for cv2.videoCapture(). If you want to use laptop's internal webcam, set this variable to 0.
CAM_LAPTOP = 1
CAM_DESKTOP = 0

url = 'http://cs408.pikachu.io/lesson/create'

# This function sends a post request to server then returns the status code.
# file_path : string. Name of path that contains zip file to be sent.
# url : string. Global url variable that is written on line 15 will be used for here.
def sendFile(file_path, url):
	payloads = {'klass_id' : 1, 'name' : 'Test'}
	file = {'file': open(file_path, 'rb')}
	r = requests.post(url, params=payloads, files=file)
	return r.status_code

# This function compresses a folder as a .zip file. Returns nothing.
# output_name : string. name of the output file. ex. 'test.zip'
# src_path : string. Name of the src path that contains pictures of frames to compress. ex) 'class/lectures/'
def zipFolder(output_name, src_path):
	file = zipfile.ZipFile(output_name, "w")
	for pic in glob.glob(src_path+"/*"):
                if not "rv" in os.path.basename(pic):
		        file.write(pic, os.path.basename(pic), zipfile.ZIP_DEFLATED)
	file.close()
        print("zipFolder: Successfully made a zip file to send")

# This function returns grayscaled frame of the input frame.
def gray(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray

# This function is the key function of our program.
# 1. Find or make appropriate path for the name of class and name of lesson.
# 2. Capture the webcam(real-time) or capture a video, and extract only background, not instructor.
# 3. Calculate the amount of texts as ratio in the extracted frame(That's why this file imports chalkboard module).
# 4. Save png of the choosen frame that has maximum ratio in specific period(This period can be changed by user).
# 5. Exits when the video is end, or the webcam shutdowns.
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
	
	max_frame = temp
	
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
		framecount = framecount + 1
		
		# Get most-written frame in a period, and export it as png.
		# After that, the max_frame must be initialized for re-comparing in new period's start.
		if getRatioPercent(getChalkBoard(max_frame)) < getRatioPercent(opening):
		        max_frame = temp
		if framecount == (fps*period/frm):
			cv2.imwrite((name_class+'/'+name_lesson+'/'+'save{0:02d}.jpg').format(picCount), max_frame)
			framecount = 0
			picCount = picCount + 1
			max_frame = temp
			print('Captured!')
		
		if cv2.waitKey(1)==113:
			break
	print("Total captures :" + str(picCount))
	camera.release()

print('Capturing...')
l = len(sys.argv)

code = ''

className = 'myClass'
lectureName = '1'
videoname = CAM_LAPTOP
 
# Set variables by different options according to the argv
# Make zip file and send it to server right after the capturing function ends.
if l>=2:
	className = sys.argv[1]
if l>=3:
	lectureName = sys.argv[2]
if l>=4:
	period = int(sys.argv[3])
if l>=5:
	videoname = sys.argv[4]

doCapture(videoname, className, lectureName, period)
toPdf(className, lectureName)
zipFolder(className+"_"+lectureName+".zip", className+"/"+lectureName)
code = sendFile(className + "_" + lectureName + ".zip", url)
print('file send request status: '+str(code))

# Close all of the cv2 windows
cv2.destroyAllWindows()
