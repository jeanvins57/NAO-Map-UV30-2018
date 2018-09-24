import fsm
import time
import sys

# use keyboard to control the fsm
#  w : event "Pause"
#  s : event "Terminer la mission"
#  g : event "Avancer" 
#  l : event "Tourner à gauche"
#  r : event "Tourner à droite"

# global variables
f = fsm.fsm();  # finite state machine

def getKey():
    c='s'
    cok=False
    # insert your code here
    # this function must return cok=True if a key has been hit
    #                           and cok=False if no key has been hit
    # c is the code of key
    return cok,c

# functions (actions of the fsm)
# example of a function doRun 
def doRun():
    print ">>>>>> action : run for 1 s"   # do some work
    time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="Go" # define the default event
    if newKey:
        if val=="w":
            event="Wait"  # new event if key "w" is pressed
    return event # return event to be able to define the transition
# define here all the other functions (actions) of the fsm 
# ...

if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle") # example
    # add here all the states you need
    # ...

    # defines the events 
    f.add_event ("Wait") # example
    # add here all the events you need
    # ...
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Idle","Wait",doWait); # example
    # add here all the transitions you need
    # ...

    # initial state
    f.set_state ("Idle") # ... replace with your initial state
    # first event
    f.set_event ("Wait") # ...  replace with you first event 
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



