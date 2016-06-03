import cv2
import numpy as np
from matplotlib import pyplot as plt

for j in range(2, 3):
	img = cv2.imread("a/asdf%s.png" % ('0000' + str(j))[-4:])
	color = ('b', 'g', 'r')
	for i,col in enumerate(color):
		histr = cv2.calcHist([img], [i], None, [256], [0, 256])
		plt.plot(histr, color = col)
		plt.xlim([0, 256])
	plt.show()
