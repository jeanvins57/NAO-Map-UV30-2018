import fsm
import time
import sys

import naocmd

import select


def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

# use keyboard to control the fsm
#  w : event "Pause"
#  s : event "Terminer"
#  g : event "Avancer" 
#  l : event "Gauche"
#  r : event "Droite"

# global variables
f = fsm.fsm();  # finite state machine
naorob = naocmd.Robot("172.20.13.167", 9559)

def getKey():
    c='s'
    cok=False
    # insert your code here
    # this function must return cok=True if a key has been hit
    #                           and cok=False if no key has been hit
    # c is the code of key
    if isData():
        c = sys.stdin.read(1)
        cok=True
    return cok,c

# functions (actions of the fsm)
# example of a function doRun 
# define here all the other functions (actions) of the fsm 
def doWait():
	print ">>>>>> action : wait for 1 s"
	naorob.wait()
	time.sleep(0.2)
	newKey, val = getKey()
	event = "Pause"
	if newKey:
		if val == "g": #on avance
			event="Avancer"
	return event

def doMove():
	print ">>>>>> action : move for 1 s"
	naorob.move()
	time.sleep(0.2)
	newKey, val = getKey()
	event = "Avancer"
	if newKey:
		if val=="l":
			event = "Gauche"
		if val=="r":
			event = "Droite"
		if val=="s":
			event = "Terminer"
	return event

def doTurnRight():
	print ">>>>>> action : turn right for 1 s"
	naorob.turnRight()
	time.sleep(0.2)
	newKey, val = getKey()
	event = "Droite"
	if newKey:
		if val=="g":
			event = "Avancer"
		if val=="l":
			event = "Gauche"
		if val=="s":
			event="Terminer"
	return event

def doTurnLeft():
	print ">>>>>> action : turn left for 1 s"
	naorob.turnLeft()
	time.sleep(0.2)
	newKey, val = getKey()
	event = "Gauche"
	if newKey:
		if val=="g":
			event = "Avancer"
		if val=="r":
			event = "Droite"
		if val=="s":
			event="Terminer"
	return event

def doEnd():
	print ">>>>>> action : crouch for 1 s"
	naorob.crouch()
	time.sleep(0.2)
	newKey, val = getKey()
	event = "Pause"
	if newKey:
		if val== "b":
			event = "Go"
	return event
def doStop():
	print ">>>>>> action : wait for 1 s"
	naorob.wait()
	time.sleep(0.2)
	newKey, val = getKey()
	event = "Terminer"
	if newKey:
		if val== "e":
			event = "Fin"
	return event

if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle") # example
    # add here all the states you need
    f.add_state ("Avancer")
    f.add_state ("Gauche")
    f.add_state ("Droite")
    f.add_state ("Stop")
    f.add_state ("End")

    # defines the events 
    f.add_event ("Pause") # example
    # add here all the events you need
    f.add_event ("Avancer")
    f.add_event ("Gauche")
    f.add_event ("Droite")
    f.add_event ("Terminer")
    f.add_event("Go")
    f.add_event("Fin")
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Idle","Pause",doWait); # example
    # add here all the transitions you need
    f.add_transition ("Idle","Avancer","Avancer",doMove);

    f.add_transition ("Avancer","Avancer","Avancer",doMove);
    f.add_transition ("Avancer","Gauche","Gauche",doTurnLeft);
    f.add_transition ("Avancer","Droite","Droite",doTurnRight);
    f.add_transition ("Avancer","Stop","Terminer",doStop);

    f.add_transition ("Gauche","Gauche","Gauche",doTurnLeft);
    f.add_transition ("Gauche","Stop","Terminer",doStop);
    f.add_transition ("Gauche","Avancer","Avancer",doMove);
    f.add_transition ("Gauche","Droite","Droite",doTurnRight);

    f.add_transition ("Droite","Droite","Droite",doTurnRight);
    f.add_transition ("Droite","Stop","Terminer",doStop);
    f.add_transition ("Droite","Gauche","Gauche",doTurnLeft);
    f.add_transition ("Droite","Avancer","Avancer",doMove);

    f.add_transition ("Stop","Stop","Terminer",doStop);
    f.add_transition ("Stop","End","Fin",doEnd);

    f.add_transition ("End","End","Fin",doEnd);

    # initial state
    f.set_state ("Idle") # ... replace with your initial state
    # first event
    f.set_event ("Pause") # ...  replace with you first event 
    # end state
    end_state = "End" # ... replace  with your end state

 
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



