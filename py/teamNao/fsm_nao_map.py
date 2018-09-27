import fsm
import time
import sys
import select
import naocmd
import map
import math

# use keyboard to control the fsm
#  w : event "Wait"
#  s : event "Stop"
#  g : event "Go" 

delay=0.1



# global variables
f = fsm.fsm();  # finite state machine
naorob = naocmd.Robot("172.20.13.167", 9559,0.15)
carte = []

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getKey():
    c='s'
    cok=False
    if isData():
        c = sys.stdin.read(1)
        cok=True
    return cok,c

    # insert your code here
    # this function must return cok=True if a key has been hit
    #                           and cok=False if no key has been hit
    # c is the code of key
   

# functions (actions of the fsm)
# example of a function doRun 
def doIdle():
    print "Robot a l'etat initial"   # do some work
    
    naorob.idle()
	
    time.sleep(delay)
    newKey,val = getKey(); # check if key pressed
    event="wait" # define the default event
    if newKey:
        if val=="g":
            event="go"
        if val=="o":
            event="bye"# new event if key "w" is pressed
    return event # return event to be able to define the transition
# define here all the other functions (actions) of the fsm 
# ...
def domove():
    print "Robot move"
    event="detect"
    time.sleep(delay)
    naorob.move()

    newKey,val = getKey();
    if newKey :
        if val=="w":
            event="wait"

    return event 

def dowait():
    print "Robot pret"
    time.sleep(delay)

    event="wait"

    naorob.idle()
    map.printMap(carte,5)

    return event 


def doleft():
    print "Robot tourne a gauche"
    time.sleep(delay) 
    naorob.turnLeft()
    newKey,val = getKey(); # check if key pressed
    event="left"

    if newKey :
	if val=="w":
	    event="wait"


    time.sleep(delay)
    event="detect"
    return event 

def doright():
    print "Robot tourne a droite"
    time.sleep(delay) 
    naorob.turnRight()
    newKey,val = getKey(); # check if key pressed
    event="right"

    if newKey :
        if val=="w":
            event="wait"



    time.sleep(delay)
    event="detect"
    return event 

def docheck():
    a,b = naorob.check()
    print "Robot Check"
    time.sleep(delay)
    newKey,val = getKey(); # check if key pressed
    event="go"
    if a < 0.50 or b < 0.50:
        if a < b:
	    position = naorob.getPosition()
	    print position, a,b
	    map.addPoint(carte, -position.y, position.x, position.theta+math.pi/2,(a+b)/2)
            event="right"
        if (a > b):
	    position = naorob.getPosition()
	    print position, a,b
	    map.addPoint(carte, -position.y, position.x, position.theta+math.pi/2,(a+b)/2)
            event="left"

    if newKey :
        if val=="w":
            event="wait"
    
    return event  


def doOff():
    print "Robot Eteint"   # do some work
    time.sleep(delay)
    newKey,val = getKey(); # check if key pressed

    naorob.end()

    event="bye" # define the default event
    if newKey:
        if val=="o":
            event="bye"  # new event if key "w" is pressed
    return event # return event to be able to define the transition

if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle")
    f.add_state ("move")
    f.add_state ("check")
    f.add_state ("turnRight")
    f.add_state ("turnLeft")
    f.add_state ("end")
    # example
    # add here all the states you need
    # ...

    # defines the events 
    f.add_event ("wait")
    f.add_event ("go")
    f.add_event ("detect")
    f.add_event ("right")
    f.add_event ("left")
    f.add_event ("bye")

    # example
    # add here all the events you need
    # ...
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Idle","wait",doIdle)
    f.add_transition ("Idle","move","go",domove)
    f.add_transition ("check","turnRight","right",doright)
    f.add_transition ("check","turnLeft","left",doleft)
    f.add_transition ("turnLeft","check","detect",docheck)
    f.add_transition ("turnLeft","Idle","wait",dowait)
    f.add_transition ("turnRight","check","detect",docheck)
    f.add_transition ("turnRight","Idle","wait",dowait)
    f.add_transition ("move","check","detect",docheck)
    f.add_transition ("check","move","go",domove)
    f.add_transition ("check","Idle","wait",dowait)
    f.add_transition ("move","Idle","wait",dowait)
    f.add_transition ("Idle","end","bye",doOff)
    # example
    # add here all the transitions you need
    # ...

    # initial state
    f.set_state ("Idle") # ... replace with your initial state
    # first event
    f.set_event ("wait") # ...  replace with you first event 
    # end state
    end_state = "end" # ... replace  with your end state

 
    # fsm loop
    run = True   
    while (run):
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
            print "New Event : ",newEvent
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
    print "End of the programm"



