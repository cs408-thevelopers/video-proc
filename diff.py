import cv2

for i in range(174):
	z = '0000' + str(i)
	z = z[-4:]
	i = cv2.imread('result/result_%s.png' % z)
	j = cv2.adaptiveThreshold(cv2.cvtColor(i, cv2.COLOR_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	cv2.imwrite("difference/diff_%s.png" % z, j)
