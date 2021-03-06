import random
import math

try:
    import pylab as pyl
    HAS_PYLAB = True
except ImportError:
    print "Matplotlib not found. this example will not plot data"
    HAS_PYLAB = False



def addPoint(carte, xRob, yRob, thetaRob, rangeSonar):#on veut addPoint au repere R0, la carte est vide au debut
	
	point = []
	thetaRob = math.radians(thetaRob)
	
	X = xRob + math.sin(thetaRob)*rangeSonar#place le point au repere du robot sin(thetaRob+pi/2)?
	Y = yRob + math.cos(thetaRob)*rangeSonar#place le point au repere du robot cos(thetaRob+pi/2)?
	
	print "Theta: ", thetaRob
	print "MAP: ", X,Y
	point.append(X)
	point.append(Y)
	carte.append(point)
	return carte

def printMap(carte, size):

	if (HAS_PYLAB):
		#################
		#  Plot  point  #
		#################
		pyl.figure()
		
		for point in carte:
			pyl.plot(point[0], point[1], color="red", marker="x", markersize=size)
			print point, ", "
		
		pyl.show()
		#end plot

################
#     TEST     #
################
if __name__ == "__main__":
	i=0
	carte = []
	while i<50:
		addPoint(carte, random.randint(-25,25),random.randint(-25,25), math.pi/2,random.randint(0,5))
		i+=1

	printMap(carte,5)

