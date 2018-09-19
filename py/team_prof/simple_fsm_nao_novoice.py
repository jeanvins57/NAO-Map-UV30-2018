import fsm
import time
import sys
import select
import tty 
import termios
import naocmd_novoice as naocmd


# global variables
robotIp="localhost"
#robotPort=11212   #for v-rep
robotPort=9559
f = fsm.fsm()  # finite state machine
lSpeed = 0.05  # 5 cm/s # on real NAO
rSpeed = 10.0  # 10 deg/s
#lSpeed = 0.15  # 15 cm/s # on virtual NAO
#rSpeed = 30.0  # 30 deg/s  

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getKey():
    #tty.setcbreak(sys.stdin.fileno())
    c='s'
    cok=False
    if isData():
        c = sys.stdin.read(1)
        cok=True
    return cok,c

# functions (actions of the fsm)
def doMotion():
    #print "go straight for 1 s"
    naocmd.walk(lSpeed)
    time.sleep(0.1)
    newKey,val = getKey();
    event="Go"
    if newKey:
        if val=="w":
            event="Wait"
        if val=="l":
            event="TurnLeft"
        if val=="r":
            event="TurnRight"
    return event

def doTurnRight():
    #print "rotate right for 1 seconds"
    naocmd.turn(-rSpeed)
    time.sleep(0.1)
    newKey,val = getKey();
    event="TurnRight"
    if newKey:
        if val=="l":
            event="TurnLeft"
        if val=="w":
            event="Wait"
    return event

def doTurnLeft():
    #print "rotate left for 1 seconds"
    naocmd.turn(rSpeed)
    time.sleep(0.1)
    newKey,val = getKey();
    event="TurnLeft"
    if newKey:
        if val=="r":
            event="TurnRight"
        if val=="w":
            event="Wait"
    return event

def doWait():
    #print "wait 1s for a command"
    naocmd.walk(0.0)
    naocmd.turn(0.0)
    time.sleep(0.1)
    newKey,val = getKey();
    #print  newKey,val
    event="Wait"
    if newKey:
        if val=="s":
            event="Stop"
        if val=="g":
            event="Go"
        if val=="l":
            event="TurnLeft"
        if val=="r":
            event="TurnRight"
    return event
    
def doStopAll():
    print "stop all"
    event="Stop"
    naocmd.walk(0.0)
    naocmd.turn(0.0)
    naocmd.stop()
    return event

if __name__== "__main__":
    if len(sys.argv) < 2:
        print "give at least IP address of the NAO ..."
        exit(0)
    if len(sys.argv) == 2:
      robotIp=sys.argv[1]
    if len(sys.argv) == 3:
      robotIp=sys.argv[1]
      robotPort=int(sys.argv[2])

    if robotPort > 10000:
        lSpeed = 0.15  # 15 cm/s # on virtual NAO
        rSpeed = 30.0  # 30 deg/s  

    
    # define the states
    f.add_state ("Idle")
    f.add_state ("RotateRight")
    f.add_state ("RotateLeft")
    f.add_state ("Move")
    f.add_state ("End")

    # defines the events
    f.add_event ("Wait")
    f.add_event ("Go")
    f.add_event ("TurnRight")
    f.add_event ("TurnLeft")
    f.add_event ("Stop")
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Idle","Wait",doWait);
    f.add_transition ("Idle","RotateLeft","TurnLeft",doTurnLeft);
    f.add_transition ("Idle","RotateRight","TurnRight",doTurnRight);
    f.add_transition ("Idle","Move","Go",doMotion);
    f.add_transition ("Idle","End","Stop",doStopAll);

    f.add_transition ("Move","Idle","Wait",doWait);
    f.add_transition ("Move","Move","Go",doMotion);
    f.add_transition ("Move","RotateLeft","TurnLeft",doTurnLeft);
    f.add_transition ("Move","RotateRight","TurnRight",doTurnRight);

    f.add_transition ("RotateLeft","Idle","Wait",doWait);
    f.add_transition ("RotateLeft","RotateRight","TurnRight",doTurnRight);
    f.add_transition ("RotateLeft","RotateLeft","TurnLeft",doTurnLeft);

    f.add_transition ("RotateRight","Idle","Wait",doWait);
    f.add_transition ("RotateRight","RotateLeft","TurnLeft",doTurnLeft);
    f.add_transition ("RotateRight","RotateRight","TurnRight",doTurnRight);

    naocmd.init(robotIp,robotPort)
    naocmd.setPosture("StandInit")
 
    # current state
    f.set_state ("Idle")
    # first event
    f.set_event ("Wait")

 
    # fsm loop
    run = True   
    while (run):
        funct = f.run ()
        if f.curState != "End":
            newEvent = funct()
            #print "New Event : ",newEvent
            f.set_event(newEvent)
        else:
            funct()
            run = False
            
    print "End of the programm"



