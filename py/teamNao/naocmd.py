import sys
import motion
import time
from naoqi import ALProxy
import math
import almath as m
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on  Sep 21  2018

@author: Herve
"""

robotIp="localhost"
robotPort=11212
#robotIp="172.20.13.167"
#robotPort=9559

def Sit():

# Init proxies.
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
    
    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)

    fractSpeed=0.3
    postureProxy.goToPosture("Crouch", fractSpeed)
    motionProxy.setStiffnesses("Body", 0.0)
    motionProxy.rest()

    
def Move():
    try:
        motionProxy = ALProxy("ALMotion", robotIp, robotPort)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)
         
    try:
        postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
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



def StiffnessOn(proxy):
    
     pNames = "Body"
     pStiffnessLists = 1.5
     pTimeLists = 1.5
     proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists) 
    
def TurnLeft():
    
    try:
        motionProxy = ALProxy("ALMotion", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    StiffnessOn(motionProxy)


    motionProxy.setWalkArmsEnabled(True, True)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    initRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))

    X = 0.2
    Y = 0.0
    Theta = math.pi/6.0
    motionProxy.post.moveTo(X, Y, Theta)
    motionProxy.waitUntilMoveIsFinished()

  
    endRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))
    robotMove = m.pose2DInverse(initRobotPosition)*endRobotPosition
    print "Robot Move :", robotMove
    


def TurnRight():
    try:
        motionProxy = ALProxy("ALMotion", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    StiffnessOn(motionProxy)


    motionProxy.setWalkArmsEnabled(True, True)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    initRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))

    X = 0.2
    Y = 0.0
    Theta = -math.pi/6.0
    motionProxy.post.moveTo(X, Y, Theta)
    motionProxy.waitUntilMoveIsFinished()

  
    endRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))
    robotMove = m.pose2DInverse(initRobotPosition)*endRobotPosition
    print "Robot Move :", robotMove
    
    
    
    #fonction check
    
def Check():
    try:
        self.sonarProxy = ALProxy("ALSonar", self.robotIP, self.PORT)
    except Exception, e:
        print "Could not create proxy to ALSonar"
        print "Error was: ", e
        self.motionProxy.wakeUp()
        self.motionProxy.setStiffnesses("Body", 1.0)
         
    try:
        memoryProxy = ALProxy("ALMemory", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMemory"
        print "Error was: ", e

    try:
        sonarProxy = ALProxy("ALSonar", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALSonar"
        print "Error was: ", e

    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    print valL, valR
    sonarProxy.unsubscribe("SonarApp");
    return valL, valR
   
def Idle():
    #global robotIp, robotPort
    #robotIp="localhost"
    #robotPort=11212

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
        
    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)
    
    fractSpeed=0.8
    postureProxy.goToPosture("StandInit", fractSpeed)
    #time.sleep(1.0)
    #motionProxy.setStiffnesses("Body", 0.0)  
    
def End():
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
        
    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)
    
    fractSpeed=0.8
    postureProxy.goToPosture("Crouch", fractSpeed)
    time.sleep(1.0)
    motionProxy.setStiffnesses("Body", 0.0)  

if __name__ == "__main__":
    Idle()
    Move()
    End()
    
