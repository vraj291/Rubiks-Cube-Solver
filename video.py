import cv2
from colorDetection import ColorDetection
import time

class Video:

	def __init__(self):
		self.cam = cv2.VideoCapture(0)
		print("Webcam Started.")

	# Capture cube from device webcam
	def capture(self):
		faces = ['UP','RIGHT','FRONT','DOWN','LEFT','BEHIND']
		currFace = 0

		cubeString = ""

		while(True):
			ret, frame = self.cam.read()
			cv2.putText(frame, faces[currFace], (100,100), cv2.FONT_HERSHEY_SIMPLEX,2, (255,0,0), 3, cv2.LINE_AA)
			cv2.imshow('Camera', frame)

			# Check if current face can be captured accurately
			faceString = ColorDetection(frame).run()
			if(faceString != -1):
				print(faceString)
				cubeString =  cubeString + faceString
				print(faces[currFace] + ' Scanned.')
				currFace = currFace + 1
				time.sleep(2)

			if currFace == len(faces) or (cv2.waitKey(1) & 0xFF == ord('q')):
				break
	
		self.cam.release()
		cv2.destroyAllWindows()

		print(cubeString)
		return cubeString
