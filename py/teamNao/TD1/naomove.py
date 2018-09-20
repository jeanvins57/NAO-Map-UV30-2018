import sys
import math
import time
from naoqi import ALProxy

def main(robotIP):
	PORT = 11212

	try:
		motionProxy = ALProxy("ALMotion", robotIP, PORT)
	except Exception,e:
		print "Could not create proxy to ALMotion"
		print "Error was: ",e
		sys.exit(1)

	try:
        	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
   	except Exception, e:
		print "Could not create proxy to ALRobotPosture"
		print "Error was: ", e



	postureProxy.goToPosture("Crouch", 0.5)#Nao debout
	postureProxy.goToPosture("StandInit", 0.5)#Nao debout

	x  = 0.2
	y  = 0.2
	theta  = math.pi/2
	#motionProxy.moveTo(x, y, theta)
	motionProxy.move(x,0,0)
	time.sleep(5)
	motionProxy.move(0,0,0)
	
if __name__ == "__main__":
    robotIp = "127.0.0.1"

    if len(sys.argv) <= 1:
        print "Usage python naomove.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
