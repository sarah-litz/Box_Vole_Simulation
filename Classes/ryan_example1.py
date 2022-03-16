""" 
This is an example scenario that someone would run for the home_cage experiment. This is written mostly with pseudocode but includes function names and classes where possible
"""
import os
import time
from Map import Map
from mode import modeABC



#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
class mode1(modeABC):
    """This mode is the first of two. The setup is that for 12 hours, the doors are open and the vole has free reign to move into the second chamber. There is a lever in the first chamber and a free wheel in the second chamber. The lever is retracted during this time.

    Args:
        modeABC (class object): Inherited abstract base class
    """
    def __init__(self, timeout, map):
        super().__init__(self, timeout, map)

    def enter(self):
        self.active = True

    def exit(self):
        self.active = False

        # Moves into mode 2

    def run(self):
        # Run code of the class. This basically waits for the timeout

        print(' Mode 1 is Running ')
        # Retract the lever and open the door
        #self.map.chamber_lever.retract()
        #self.map.door.default = True # opened
        #self.map.door.trigger = None # No lever connected


        print( 'Mode 1 is entering Timeout Inteval')
        # set timeout boolean to True, then Wait for timeout interval
        self.inTimeout = True 
        while self.active & ((time.now() - self.startTime) < self.timeout):
            pass
        self.inTimeout = False 

        print( 'Mode 1 finished its Timeout Period and is now exiting ')

        self.exit()



class mode2(modeABC):
    """This is for the second twelve hours of the experiment, where the door between the chambers is closed. Here, the lever is extended, and controls access to the wheel in the second chamber. Every time the wheel is accessed, the number of presses required for the lever to increase is one.

    Args:
        modeABC (class object): Inherited abstract base class
    """
    
    def __init__(self):
        super().__init__()

    def enter(self):
        self.active = True

        # Extend the lever and close the door
        door.trigger = chamber_lever
        door.default = False
        chamber_lever.extend()

    def exit(self):
        self.active = False

    def run(self):

        # Logic to change the num presses every time the wheel is run
        while self.active:
            # If the wheel has been interacted with, increase the number of required presses
            if self.box.wheel_1.threshold:
                self.box.chamber_lever.numPresses += 1
            # END if
        # END while

if __name__ == "__main__":
    # Set up Map
    # Instantiate the hardware objects by creating the map 
    map = Map('/Users/sarahlitz/Projects/Donaldson Lab/Vole Simulator Version 1/Box_Vole_Simulation/Classes/Configurations')


    # Instantiate the modes
    mode1 = mode1(timeout = 43200, map = map)
    mode2 = mode2(timeout = 43200, map = map)

    # Set attributes

    # Begin the script 
    mode1.enter()
    mode1.run()

    # It should run continuously from this point on