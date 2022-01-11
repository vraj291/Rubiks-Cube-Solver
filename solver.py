from cv2 import error
import kociemba
from config import CUBE_ORIENTATIONS

class Solver:

	# Solves given cubeString
	def solveCube(self,cubeString):
		try:
			algorithm = kociemba.solve(cubeString)
			stepNotations = algorithm.split(' ')
			steps = []	
			for notation in stepNotations:
				step = ""
				if(len(notation) == 1):
					step = f'Turn {CUBE_ORIENTATIONS[notation[0]]} face clockwise 90 degrees.'
				elif(notation[1] == "'"):
					step = f'Turn {CUBE_ORIENTATIONS[notation[0]]} face anticlockwise 90 degrees.'
				else:
					step = f'Turn {CUBE_ORIENTATIONS[notation[0]]} face 180 degrees.'
				steps.append(step)
			return steps
		except Exception:
			return []

	def printSteps(self,steps):
		if len(steps) == 0:
			print('An error occured. The cube could not be solved.')
		else:
			print(f"Cube can be solved in the following {len(steps)} steps: \n")
			for index,step in enumerate(steps,1):
				print(str(index) + ") " + step)
