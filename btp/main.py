# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2
import time
from mss import mss
from PIL import Image
import pyautogui
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True, help="Path to template image")
# ap.add_argument("-i", "--images", required=True,
# 	help="Path to images where template will be matched")
# ap.add_argument("-v", "--visualize",
# 	help="Flag indicating whether or not to visualize each iteration")
args = vars(ap.parse_args())

# load the image image, convert it to grayscale, and detect edges
template = cv2.imread(args['template'])
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
# cv2.startWindowThread()
# cv2.imshow("Template", template)
# cv2.waitKey()

mon = {'top': 0, 'left': 0, 'width': 1366, 'height': 767}

sct = mss()

while 1:
	sct.get_pixels(mon)
	img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
	image_r = np.array(img)
	gray = cv2.cvtColor(image_r, cv2.COLOR_BGR2GRAY)
	found = None

	for scale in np.linspace(.2, 1.0, 20)[::-1]:
		resized = imutils.resize(gray, width=int(gray.shape[1]*scale))
		r = gray.shape[1] / float(resized.shape[1])

		if resized.shape[1] < tW or resized.shape[0] < tH:
			break

		edged = cv2.Canny(resized, 50, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)

	(_, maxLoc, r) = found
	(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
	(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

	# draw a bounding box around the detected result and display the image
	# cv2.rectangle(image_r, (startX, startY), (endX, endY), (0, 0, 255), 2)
	xPos = int((startX + endX) / 2)
	yPos = int((startY + endY) / 2)
	x, y = pyautogui.position()
	positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
	print positionStr
	pyautogui.click(xPos, yPos)
	time.sleep(2)

	# cv2.imshow("Image", image_r)
	# cv2.waitKey(0)
    # cv2.imshow('test', np.array(img))
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break

# # for image in glob.glob(args["images"]):
# image_r = cv2.imread()
# gray = cv2.cvtColor(image_r, cv2.COLOR_BGR2GRAY)
# found = None

# for scale in np.linspace(.2, 1.0, 20)[::-1]:
# 	resized = imutils.resize(gray, width=int(gray.shape[1]*scale))
# 	r = gray.shape[1] / float(resized.shape[1])

# 	if resized.shape[1] < tW or resized.shape[0] < tH:
# 		break

# 	edged = cv2.Canny(resized, 50, 200)
# 	result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
# 	(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

# 	if found is None or maxVal > found[0]:
# 		found = (maxVal, maxLoc, r)

# (_, maxLoc, r) = found
# (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
# (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

# # draw a bounding box around the detected result and display the image
# cv2.rectangle(image_r, (startX, startY), (endX, endY), (0, 0, 255), 2)
# cv2.imshow("Image", image_r)
# cv2.waitKey(0)