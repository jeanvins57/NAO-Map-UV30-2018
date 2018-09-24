from naoqi import ALProxy
import math
import sys
import time



class Robot:

	def __init__(self, robotIP, PORT, deltaX):
        	self.PORT =PORT
		self.robotIP = robotIP
	
		try:
			self.motionProxy = ALProxy("ALMotion", self.robotIP, self.PORT)
		except Exception,e:
			print "Could not create proxy to ALMotion"
			print "Error was: ",e
			sys.exit(1)

		try:
			self.postureProxy = ALProxy("ALRobotPosture", self.robotIP, self.PORT)
	   	except Exception, e:
			print "Could not create proxy to ALRobotPosture"
			print "Error was: ", e

		try:
		    self.memoryProxy = ALProxy("ALMemory", self.robotIP, self.PORT)
		except Exception, e:
		    print "Could not create proxy to ALMemory"
		    print "Error was: ", e

		try:
		    self.sonarProxy = ALProxy("ALSonar", self.robotIP, self.PORT)
		except Exception, e:
		    print "Could not create proxy to ALSonar"
		    print "Error was: ", e


		self.motionProxy.wakeUp()
		self.motionProxy.setStiffnesses("Body", 1.0)
		self.poseInit = Pose2D(self.motionProxy.getRobotPosition(False))
#poseInit=abs(x),abs(y),abs(theta)
		self.deltaX = deltaX


	def move(self):#bouge de deltaX

		position = self.motionProxy.getRobotPosition(False)
		self.motionProxy.moveTo(position[0]+deltaX,position[1],position[2])

	def idle(self):

		self.motionProxy.move(0,0,0)
		self.postureProxy.goToPosture("StandInit", 0.5)#Nao debout

	def turnRight(self):
	
		self.motionProxy.move(0,0,0)
		position = Pose2D(self.motionProxy.getRobotPosition(False))
		self.motionProxy.moveTo(position[0],position[1],position[2]-math.pi/2)

	def turnLeft(self):
	
		self.motionProxy.move(0,0,0)
		position = Pose2D(self.motionProxy.getRobotPosition(False))
		self.motionProxy.move(position[0],position[1],position[2]+math.pi/2)

	def end(self):
	
		self.motionProxy.move(0,0,0)
		self.postureProxy.goToPosture("Crouch", 0.5)
		self.motionProxy.setStiffnesses("Body", 0.0)
	
	def check(self):

		self.sonarProxy.subscribe("SonarApp");
	    	time.sleep(0.25)
		valL = self.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
		valR = self.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
		
		return valL, valR

	def getPosition(self):#donne la position dans le repere poseInit

		position = Pose2D(self.motionProxy.getRobotPosition(False))
		position[0] = position[0]-self.poseInit[0]
		position[1] = position[1]-self.poseInit[1]
		position[2] = position[2]-self.poseInit[2]
		return position


