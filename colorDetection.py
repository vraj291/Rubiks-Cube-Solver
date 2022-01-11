import cv2
from config import COLOR_PALETTE,CUBE_FACES
from utils import containsRectangle

class ColorDetection:

	def __init__(self,frame):
		self.frame = frame

	def preprocessFrame(self):
		grayFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		blurredFrame = cv2.blur(grayFrame, (3, 3))
		cannyFrame = cv2.Canny(blurredFrame, 30, 60, 3)
		dilatedFrame = cv2.dilate(cannyFrame, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)))
		return dilatedFrame

	def getSquareContours(self,frame):
		contours,hierarchy = cv2.findContours(frame,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		final_contours = []

		for contour in contours:
			contourArea = cv2.contourArea(contour)
			x,y,w,h = cv2.boundingRect(contour)

			# Check similarity with bounding square
			squareRatio = float(contourArea/w/h)

			if(squareRatio >= 0.8 and squareRatio <= 1.2 and w >= h-8 and w <= h+8):
				
				if(len(final_contours) == 0):
					final_contours.append((x,y,w,h))
				else:
					valid = True

					# Check for overlapping squares
					for temp in final_contours:
						if (containsRectangle((x,y,w,h),temp) or containsRectangle(temp,(x,y,w,h))):
							valid = False
							break
					if valid:
						final_contours.append((x,y,w,h))
		
		return final_contours

	def getCubeContours(self,contours):
		found = False
		contour_neighbors = {}
		for index, contour in enumerate(contours):
			(x, y, w, h) = contour
			contour_neighbors[index] = []
			center_x = x + w / 2
			center_y = y + h / 2
			radius = 1.5

			# Obtain a contour with 9 neighbours (central cube block)
			neighbor_positions = [
				[(center_x - w * radius), (center_y - h * radius)],
				[center_x, (center_y - h * radius)],
				[(center_x + w * radius), (center_y - h * radius)],
				[(center_x - w * radius), center_y],
				[center_x, center_y],
				[(center_x + w * radius), center_y],
				[(center_x - w * radius), (center_y + h * radius)],
				[center_x, (center_y + h * radius)],
				[(center_x + w * radius), (center_y + h * radius)],
			]

			for neighbor in contours:
				(x2, y2, w2, h2) = neighbor
				for (x3, y3) in neighbor_positions:
					if (x2 < x3 and y2 < y3) and (x2 + w2 > x3 and y2 + h2 > y3):
						contour_neighbors[index].append(neighbor)

		for (contour, neighbors) in contour_neighbors.items():
			if len(neighbors) == 9:
				found = True
				contours = neighbors
				break

		if not found:
			return []
		
		return contours

	# Sort processed contours in cube format
	def sortCubeContours(self,contours):
		y_sorted = sorted(contours, key=lambda item: item[1])
		top_row = sorted(y_sorted[0:3], key=lambda item: item[0])
		middle_row = sorted(y_sorted[3:6], key=lambda item: item[0])
		bottom_row = sorted(y_sorted[6:9], key=lambda item: item[0])
		sorted_contours = top_row + middle_row + bottom_row
		return sorted_contours

	# Get dominant color in contour
	def getBlockColor(self,region):
		average = region.mean(axis=0).mean(axis=0).round()
		diff = 999999
		color = ""
		for [key,rgbVal] in COLOR_PALETTE.items():
			temp = abs(average[0]-rgbVal[0]) + abs(average[1]-rgbVal[1]) + abs(average[2]-rgbVal[2])
			if diff > temp:
				diff = temp
				color = key
		return color
	
	def getFaceString(self,contours):
		colorString = ""

		for contour in contours:
			x,y,w,h = contour
			region = self.frame[y:y+h, x:x+w]
			color = self.getBlockColor(region)
			colorString = colorString + CUBE_FACES[color]
			cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0,0,255), 2)

		cv2.imshow('Contours',self.frame)
		return colorString

	def run(self):

		preprocessedFrame = self.preprocessFrame()
		squareContours = self.getSquareContours(preprocessedFrame)
		if len(squareContours) < 9:
			return -1
		cubeContours = self.getCubeContours(squareContours)
		if len(cubeContours) != 9:
			return -1
		colorString = self.getFaceString(self.sortCubeContours(cubeContours))
		return colorString 