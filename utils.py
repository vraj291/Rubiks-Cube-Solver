def containsRectangle(rec1,rec2):
	x,y,w,h = rec1
	x1,y1,w1,h1 = rec2
	if (x>x1 and (x+w)<(x1+w1) and y>y1 and (y+h)<(y1+h1)):
		return True
	return False