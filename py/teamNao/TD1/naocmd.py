from naoqi import ALProxy
import math
import sys
import time



class Robot:

	def __init__(self, robotIP, PORT):
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


	def move(self):
	

		self.sonarProxy.subscribe("SonarApp");
	    	time.sleep(0.25)
		valL = self.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
		valR = self.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
		print valL, valR
		if valL < 0.5 or valR < 0.5:
			self.motionProxy.stopMove()
		else:
			self.motionProxy.move(1,0,0)

		self.sonarProxy.unsubscribe("SonarApp");

	def wait(self):

		self.motionProxy.move(0,0,0)
		self.postureProxy.goToPosture("StandInit", 0.5)#Nao debout

	def turnRight(self):
	
		self.motionProxy.move(0,0,0)
		self.motionProxy.move(0,0,-math.pi/2)

	def turnLeft(self):
	
		self.motionProxy.move(0,0,0)
		self.motionProxy.move(0,0,math.pi/2)

	def crouch(self):
	
		self.motionProxy.move(0,0,0)
		self.postureProxy.goToPosture("Crouch", 0.5)
		self.motionProxy.setStiffnesses("Body", 0.0)


