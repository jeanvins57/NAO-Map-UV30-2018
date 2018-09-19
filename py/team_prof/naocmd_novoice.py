# -*- coding: utf-8 -*-
import sys
import motion
import time
from naoqi import ALProxy
import math


#robotIp="localhost"
#robotPort=11212
##robotIp="172.20.16.13" # epsilon
##robotIp="172.20.15.23" # gamma
#robotIp="172.20.11.241" # alpha
#robotPort=9559
motionProxy=None
postureProxy=None
ttsProxy=None
lSpeedLast = 0.0
rSpeedLast = 0.0

  

# Init proxies.
def init(robotIp, robotPort):
    global motionProxy,postureProxy,ttsProxy

    try:
        motionProxy = ALProxy("ALMotion", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    # Set NAO in Stiffness On 
    # using wakeUp (new feature in 1.14.1)
    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)


def setPosture(name):
    fractSpeed=0.3
    if (name == "StandZero"):
        print "go to posture : stand zero"
        postureProxy.goToPosture("StandZero", fractSpeed)
    if (name == "StandInit"):
        print "go to posture : stand init"
        postureProxy.goToPosture("StandInit", fractSpeed)
    if (name == "Crouch"):
        print "go to posture : crouch"
        postureProxy.goToPosture("Crouch", fractSpeed)


def walk(speed):  # speed in m/s
    global lSpeedLast
    if (speed != lSpeedLast):
        lSpeedLast = speed
        if (speed == 0.0):
            motionProxy.stopMove()
            #setPosture("StandInit")
        else:
            print "walk at %f cm/s"%(speed*100.0)
            motionProxy.moveInit();
            motionProxy.move(speed,0.0,0.0)

def turn(speed):  # speed in deg/s
    global rSpeedLast
    if (speed != rSpeedLast):
        rSpeedLast = speed
        if (speed == 0.0):
            motionProxy.stopMove()
            #setPosture("StandInit")
        else:
            print "turn at %f deg/s"%(speed)
            motionProxy.moveInit();
            motionProxy.move(0.01,0.0,speed*math.pi/180.0)


def stop():
    motionProxy.stopMove()
    setPosture("Crouch")
    motionProxy.setStiffnesses("Body", 0.0)
    motionProxy.rest()
    print "end"
