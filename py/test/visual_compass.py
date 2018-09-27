# -*- encoding: utf-8 -*-

import sys
import time
import pickle
from naoqi import ALProxy
import cv2,Image
import numpy as np
import math

def init (robotIp,robotPort):
    PORT = robotPort

    try:
        motionProxy = ALProxy("ALMotion", robotIp, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)
    try:
        memoryProxy = ALProxy("ALMemory", robotIp, PORT)
    except Exception,e:
        print "Could not create proxy to ALMemory"
        print "Error was: ",e
        sys.exit(1)
    try:
        compassProxy = ALProxy("ALVisualCompass", robotIp, PORT)
    except Exception,e:
        print "Could not create proxy to ALVisualCompass"
        print "Error was: ",e
        sys.exit(1)

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    return motionProxy, memoryProxy, compassProxy, postureProxy


def extractImage (refImage,saveFile=None):
    imageWidth = refImage[0]
    imageHeigth = refImage[1]
    array=refImage[6] #cioe prelevo il sesto campo, ovvero l'immagine in formato ASCII
    pilImg = Image.frombytes("L", (imageWidth, imageHeigth), array) 
    if not (saveFile is None):
        pilImg.save(saveFile, "PNG")
    return pilImg

if __name__ == "__main__":
    robotIp = "127.0.0.1"
    robotPort = 11212

    if len(sys.argv) >= 1:
        robotIp = sys.argv[1]
    if len(sys.argv) >= 2:
        robotPort = int(sys.argv[2])

    motionProxy, memoryProxy, compassProxy, postureProxy = init(robotIp,robotPort)

    
    # Reference will be set each time the module is subscribed.
    compassProxy.enableReferenceRefresh(False);
    # Image resolution is QVGA (320x240).
    compassProxy.setResolution(1);

    # Subscribe to launch the processing.
    # Get the reference image for display.
    compassProxy.subscribe("VisualCompassTest");
    refImage = compassProxy.getReferenceImage();
    pilRefImg = extractImage (refImage,saveFile="imgOriginal.png")

    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)
    fractSpeed=0.5
    postureProxy.goToPosture("StandInit", fractSpeed)

    motionProxy.moveTo(0.0,0.0,math.pi/6.0)

    curImage = compassProxy.getCurrentImage();
    pilCurImg = extractImage (curImage,saveFile="imgCurrent.png")

    motionProxy.moveTo(0.0,0.0,-math.pi/6.0)
    endImage = compassProxy.getCurrentImage();
    pilEndImg = extractImage (endImage,saveFile="imgFinal.png")

    postureProxy.goToPosture("Crouch", fractSpeed)
    motionProxy.setStiffnesses("Body", 0.0)
    motionProxy.rest()
