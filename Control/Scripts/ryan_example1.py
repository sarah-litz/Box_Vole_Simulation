""" 
This is an example scenario that someone would run for the home_cage experiment. This is written mostly with pseudocode but includes function names and classes where possible
"""
import os
import time
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
    def enter(self):
        self.startTime = time.time() 
        self.active = True

    def exit(self):
        self.active = False

        # Moves into mode 2

    def run(self):
        # Run code of the class. This basically waits for the timeout

        print('Mode 1 is Running')
        control_log('NEW MODE : Mode 1')

        # Retract the lever and open the door
        #self.map.chamber_lever.retract()
        #self.map.door.default = True # opened
        #self.map.door.trigger = None # No lever connected


        print('Mode 1 is entering Timeout Interval')
        # set timeout boolean to True, then Wait for timeout interval
        self.inTimeout = True 

        time.sleep(10) 

        while self.active and ((time.time() - self.startTime) < self.timeout):

            time.sleep(0.25)

        self.inTimeout = False 

        print( 'Mode 1 finished its Timeout Period and is now exiting ')
        control_log('End of Mode 1\n')

        self.exit()



class mode2(modeABC):
    """This is for the second twelve hours of the experiment, where the door between the chambers is closed. Here, the lever is extended, and controls access to the wheel in the second chamber. Every time the wheel is accessed, the number of presses required for the lever to increase is one.

    Args:
        modeABC (class object): Inherited abstract base class
    """
    
    def __init__(self, timeout, map):
        super().__init__(timeout, map)

    def __str__(self): 
        return 'Mode 2'
    def enter(self):
        self.startTime = time.time() 
        self.active = True

    def exit(self):
        self.active = False


    def run(self):

        control_log('NEW MODE: Mode 2')

        '''# Logic to change the num presses every time the wheel is run
        while self.active:
            # If the wheel has been interacted with, increase the number of required presses
            if self.box.wheel_1.threshold:
                self.box.chamber_lever.required_presses += 1
            
            # if lever was pressed required number of times, open door, reset the tracked num of lever presses to 0  
            if self.box.chamber_lever.threshold is True: 
                self.box.chamber_lever.presses = 0 
                self.door.condition_for_threshold_to_get_set_to_True(open=True) 
            
            # if rfid1 and rfid2 were pinged (meaning the vole moved to the next chamber), close door 
            if self.box.rfid1.threshold and self.box.rfid2.threshold: 
                self.door.condition_for_threshold_to_get_set_to_True(open=False)

            # END if
        # END while'''

  
        print('Mode 2 is Running')
        # Retract the lever and open the door
        #self.map.chamber_lever.retract()
        #self.map.door.default = True # opened
        #self.map.door.trigger = None # No lever connected


        print('Mode 2 is entering Timeout Interval')
        # set timeout boolean to True, then Wait for timeout interval
        self.inTimeout = True 
        while self.active and ((time.time() - self.startTime) < self.timeout):
            
            time.sleep(0.25)
            
        self.inTimeout = False 

        print( 'Mode 2 finished its Timeout Period and is now exiting ')
        control_log('End of Mode 2\n')

        self.exit()

if __name__ == "__main__":

    control_log(f'\n\n\nrunning {__name__}: New Experiment! ')
    # Set up Map
    # Instantiate the hardware objects by creating the map 
    map = Map('/Users/sarahlitz/Projects/Donaldson Lab/Vole Simulator Version 1/Box_Vole_Simulation/Classes/Configurations')

    # Instantiate the modes
    mode1 = mode1(timeout = 15, map = map)
    mode2 = mode2(timeout = 15, map = map)

    # Set attributes

    # Begin the script 
    mode1.enter()
    mode1.run()

    # It should run continuously from this point on
