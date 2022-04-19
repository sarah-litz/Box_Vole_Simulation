""" 
This is an example scenario that someone would run for the home_cage experiment. This is written mostly with pseudocode but includes function names and classes where possible
"""
import os
import time
import threading 
import queue

from ..Classes.Timer import countdown
from ..Classes.Map import Map
from ..Classes.ModeABC import modeABC

from Logging.logging_specs import control_log 




#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
class mode1(modeABC):
    """This mode is the first of two. The setup is that for 12 hours, the doors are open and the vole has free reign to move into the second chamber. There is a lever in the first chamber and a free wheel in the second chamber. The lever is retracted during this time.

    Args:
        modeABC (class object): Inherited abstract base class
    """
    def __init__(self, timeout, map):
        super().__init__(timeout, map)

    def __str__(self): 
        return 'Mode 1'
    
    def setup(self): 
        ''' any tasks to setup before run() gets called '''

        ## Free Range Box ## 
        # door just sits open. Set lever to inactive since door is not dependent on it, and set door's state to open.
        # all that should be running is the rfid readers.
            
        self.map.instantiated_interactables['lever1'].active = False  
        self.map.instantiated_interactables['door1'].state = True # Set To Open # NOTE: when open() is more implemented, just call open() here rather than manually setting the state variable.


    def run(self):
        # Run code of the class. This basically waits for the timeout

        #  Mode 1 Description: Open Cage! Voles are free to run around. # 
        while self.active: 

            time.sleep(self.timeout)


            # Retract the lever and open the door
            #self.map.chamber_lever.retract()
            #self.map.door.default = True # opened
            #self.map.door.trigger = None # No lever connected




class mode2(modeABC):
    """This is for the second twelve hours of the experiment, where the door between the chambers is closed. Here, the lever is extended, and controls access to the wheel in the second chamber. Every time the wheel is accessed, the number of presses required for the lever to increase is one.

    Args:
        modeABC (class object): Inherited abstract base class
    """
    
    def __init__(self, timeout, map):
        super().__init__(timeout, map)

    def __str__(self): 
        return 'Mode 2'


    def setup(self): 

        '''' any tasks to setup before run() gets called '''
        pass 

    def run(self):

        ## Timeout Logic ## 

        self.inTimeout = True

        control_log('NEW MODE: Mode 2')

        # Logic to change the num presses every time the wheel is run  
        # if lever was pressed required number of times, open door, reset the tracked num of lever presses to 0  
        while self.active: 

            ## Timeout Logic ## 
            door1 = self.map.get_edge(12).get_interactable_from_component('door1') 
            lever1 = door1.dependents[0] 


            # check for a lever threshold event 
            event = lever1.threshold_event_queue.get() # blocks until something is added. If nothing is ever added, then will jsut run until timeout ends. ( can add a timeout arg to this call if needed )
            
            ## Lever Threshold Met ## 
            print(f"(mode2, run()) Threshold Event for lever1, event: {event}" )
            lever1.pressed = 0 # reset num of presses 
            lever1.threshold_condition['goal_value'] += 1 # increase required number of presses by 1
            print(f"(mode2, run()) New Lever1 Threshold (required presses): {lever1.threshold_condition['goal_value']}")


            # door1.open() # open door


            #
            # LEAVING OFF HERE
            #

        # Retract the lever and open the door
        #self.map.chamber_lever.retract()
        #self.map.door.default = True # opened
        #self.map.door.trigger = None # No lever connected
        



