import cv2
from colorDetection import ColorDetection

class FrameReader:

	def getFrames(self,files = ['UP','RIGHT','FRONT','DOWN','LEFT','BEHIND']):
		frames = []
		for file in files:
			frames.append(cv2.imread(f'images/{file}.PNG'))
		return frames
	
	def getCubeString(self):
		cubeFrames = self.getFrames()
		cubeString = ""

		for frame in cubeFrames:
			faceString = ColorDetection(frame).run()
			if(faceString == -1):
				print("Cube could not be scanned correctly.")
				quit()
			cubeString = cubeString + faceString
		
		return cubeString