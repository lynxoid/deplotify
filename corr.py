# compute correlation

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats#pearsonr
from scipy import ndimage
from scipy import misc
import sys
import cv2
import cv2.cv


figure = cv2.imread(sys.argv[1])#, cv2.CV_LOAD_IMAGE_GRAYSCALE)
if figure == None:
	print 'Can not open'
else:
	# print figure.shape
	# print figure.max()
	# figure *= 1./255;
	# print figure
	figure = cv2.medianBlur(figure, 1)
	# print figure
	cvImage = cv2.cvtColor(figure, cv2.COLOR_BGR2GRAY)
	# cv2.imshow('grayscale', cvImage)
	# cv2.waitKey(0)
	circles =  cv2.HoughCircles(cvImage, method=cv2.cv.CV_HOUGH_GRADIENT, dp=2, minDist=1, param1=300, param2=20, minRadius=2, maxRadius=10) 
	if circles == None:
		print 'No circles'
	else:
		print 'Found', len(circles[0]), 'circles'

		for i in circles[0,:]:
		    # draw the outer circle
		    cv2.circle(figure,(i[0],i[1]),i[2],(0,0,255),2)
		    # draw the center of the circle
		    # cv2.circle(cvImage,(i[0],i[1]),2,(0,0,255),3)

		# cv2.imshow('detected circles', figure)
		# cv2.waitKey(0)

		# map X values to the range of 80-130
		w = figure.shape[1]
		minx = 80
		maxx = 130
		real_w = maxx - minx
		biopac = [minx + c[0] * 1.0 / w * real_w for c in circles[0, :] ]
		# print biopac

		# map Y values to the range of 20-120
		h = figure.shape[0]
		miny = 20
		maxy = 120
		real_h = maxy - miny
		basis = [miny + (h - c[1]) * 1.0 / h * real_h for c in circles[0, :] ]

		# print min(biopac)

		zipped = zip(biopac, basis)
		print "Before filter:", len(zipped)
		filtered = filter(lambda x: x[1] > 78, zipped)
		left_out = filter(lambda x: x[1] <= 78, zipped)
		print  "After filter:", len(filtered)
		print len(left_out) * 100.0 / len(filtered)
		biopac, basis = zip(*filtered)
		biopac_left, basis_left = zip(*left_out)

		R = stats.pearsonr(biopac, basis)
		print 'Pearson R =', R

		S = stats.spearmanr(biopac, basis)
		print 'Spearman R =', S

		plt.plot(biopac, basis, 'o')
		# plt.plot(biopac_left, basis_left, 'o')
		plt.xlabel('biopac')
		plt.ylabel('basis')
		plt.xlim([75, 125])
		plt.ylim([75, 125])
		plt.savefig("trimmed_plot.pdf")
		plt.show()

		# plt.clf()
		# plt.plot(biopac)
		# plt.plot(basis)
		# plt.show()