from frameReader import FrameReader
from solver import Solver
from video import Video

def solve(mode = 0):
	if mode == 0:
		cubeString = FrameReader().getCubeString()
	else:
		cubeString = Video().capture()
	
	solver = Solver()
	solver.printSteps(solver.solveCube(cubeString))

if __name__ == "__main__":
	solve(1)
