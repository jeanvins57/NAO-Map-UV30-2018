import fsm
import time
import sys
import pygame

pygame.init()
# draw a little area (to fucus on to get keys)
pygame.display.set_mode((100,  100))

# use keyboard to control the fsm
#  w : event "Wait"
#  s : event "Stop"
#  g : event "Go" 

# global variables
f = fsm.fsm();  # finite state machine

# example of a function doWait 
def doWait():
    time.sleep(1) # Pretend we are doing something
    #newKey, val = getKey() # check if key pressed
    event="Wait" # define the default event
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_q]:
        event = "ShutDown"
    elif key_pressed[pygame.K_UP]:
        print("Key UP is pressed")
    return event # return event to be able to define the transition

def doShutDown():
    print("Powering off Nao")
    # we don't return any new event here as it's the end state

if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle") # example
    f.add_state ("End") # example
    # add here all the states you need
    # ...

    # defines the events 
    f.add_event ("Wait") # example
    f.add_event ("ShutDown") # example
    # add here all the events you need
    # ...
   
    # defines the transition matrix
    # current state,  next state,  event,  action in next state
    f.add_transition ("Idle", "Idle", "Wait", doWait); # example
    f.add_transition ("Idle", "End", "ShutDown", doShutDown); # example
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
        pygame.event.pump()
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
            print "New Event : ", newEvent
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
    print "End of the programm"



