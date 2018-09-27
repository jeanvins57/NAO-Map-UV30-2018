import sys
from naoqi import ALProxy
import math

try:
	motionProxy = ALProxy("ALMotion", "172.20.13.167", 9559)
except Exception,e:
	print "Could not create proxy to ALMotion"
	print "Error was: ",e
	sys.exit(1)

try:
	postureProxy = ALProxy("ALRobotPosture", "172.20.13.167", 9559)
except Exception, e:
	print "Could not create proxy to ALRobotPosture"
	print "Error was: ", e

motionProxy.wakeUp()
motionProxy.setStiffnesses("Body", 1.0)

x = 0
y = 0.0
theta = -math.pi

motionProxy.moveTo(x, y, theta,
        [ ["MaxStepX", 0.02],         # step of 2 cm in front
          ["MaxStepY", 0.16],         # default value
          ["MaxStepTheta", 0.4],      # default value
          ["MaxStepFrequency", 0.0],  # low frequency
          ["StepHeight", 0.01],       # step height of 1 cm
          ["TorsoWx", 0.0],           # default value
          ["TorsoWy", 0.0] ])         # torso bend 0.0 rad in front
x = 0.5
y = 0.0
theta = 0

motionProxy.moveTo(x, y, theta,
        [ ["MaxStepX", 0.02],         # step of 2 cm in front
          ["MaxStepY", 0.16],         # default value
          ["MaxStepTheta", 0.4],      # default value
          ["MaxStepFrequency", 0.0],  # low frequency
          ["StepHeight", 0.005],       # step height of 1 cm
          ["TorsoWx", 0.0],           # default value
          ["TorsoWy", 0.0] ])         # torso bend 0.0 rad in front
x = 0
y = 0.0
theta = math.pi

motionProxy.moveTo(x, y, theta,
        [ ["MaxStepX", 0.02],         # step of 2 cm in front
          ["MaxStepY", 0.16],         # default value
          ["MaxStepTheta", 0.4],      # default value
          ["MaxStepFrequency", 0.0],  # low frequency
          ["StepHeight", 0.01],       # step height of 1 cm
          ["TorsoWx", 0.0],           # default value
          ["TorsoWy", 0.0] ])         # torso bend 0.0 rad in front
x = 0.5
y = 0.0
theta =0

motionProxy.moveTo(x, y, theta,
        [ ["MaxStepX", 0.02],         # step of 2 cm in front
          ["MaxStepY", 0.16],         # default value
          ["MaxStepTheta", 0.4],      # default value
          ["MaxStepFrequency", 0.0],  # low frequency
          ["StepHeight", 0.005],       # step height of 1 cm
          ["TorsoWx", 0.0],           # default value
          ["TorsoWy", 0.0] ])         # torso bend 0.0 rad in front

postureProxy.goToPosture("Crouch", 0.5)
motionProxy.setStiffnesses("Body", 0.0)

"""
ROT pi/2
motionProxy.moveTo(x, y, theta,
        [ ["MaxStepX", 0.02],         # step of 2 cm in front
          ["MaxStepY", 0.16],         # default value
          ["MaxStepTheta", 0.4],      # default value
          ["MaxStepFrequency", 0.0],  # low frequency
          ["StepHeight", 0.01],       # step height of 1 cm
          ["TorsoWx", 0.0],           # default value
          ["TorsoWy", 0.0] ])         # torso bend 0.0 rad in front
"""
