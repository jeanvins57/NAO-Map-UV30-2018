from naoqi import ALProxy
import math
import sys
import time
import almath



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
		self.poseInit = almath.Pose2D(self.motionProxy.getRobotPosition(False))
#poseInit=abs(x),abs(y),abs(theta)
		self.deltaX = deltaX


	def move(self):#bouge de deltaX

		position = almath.Pose2D(self.motionProxy.getRobotPosition(False))
		self.motionProxy.moveTo(position.x+self.deltaX,0,0)

	def idle(self):

		self.motionProxy.move(0,0,0)
		self.postureProxy.goToPosture("StandInit", 0.5)#Nao debout

	def turnRight(self):
	
		self.motionProxy.stopMove()
		position = almath.Pose2D(self.motionProxy.getRobotPosition(False))
		theta = math.radians(position.theta)
		self.motionProxy.moveTo(0,0,theta-math.pi/2)

	def turnLeft(self):
	
		self.motionProxy.stopMove()
		position = almath.Pose2D(self.motionProxy.getRobotPosition(False))
		theta = math.radians(position.theta)
		self.motionProxy.moveTo(0,0,theta+math.pi/2)

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

		position = almath.Pose2D(self.motionProxy.getRobotPosition(False))
		position.x = position.x - self.poseInit.x
		position.y = position.y - self.poseInit.y
		position.theta = position.theta - self.poseInit.theta
		return position

################
#     TEST     #
################
if __name__ == "__main__":

	naorob = Robot("localhost", 11212, 1)

	print "Init: ", naorob.poseInit
	print "Pose: ", naorob.getPosition()
	print "Move"
	naorob.move()

	print "Pose: ", naorob.getPosition()
	print "Right"
	naorob.turnRight()

	print "Pose: ", naorob.getPosition()
	print "Left"
	naorob.turnLeft()

	print "Pose: ", naorob.getPosition()
	print "Move"
	naorob.move()
	print "Pose: ", naorob.getPosition()

