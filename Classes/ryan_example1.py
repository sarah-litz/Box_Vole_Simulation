""" 
This is an example scenario that someone would run for the home_cage experiment. This is written mostly with pseudocode but includes function names and classes where possible
"""
import os
import time
from Map import Map
from mode import modeABC

from Logging.logging_specs import debug 



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
        self.startTime = time.time() 
        self.active = True

    def exit(self):
        self.active = False

        # Moves into mode 2

    def run(self):
        # Run code of the class. This basically waits for the timeout

        print('Mode 1 is Running')
        # Retract the lever and open the door
        #self.map.chamber_lever.retract()
        #self.map.door.default = True # opened
        #self.map.door.trigger = None # No lever connected


        print('Mode 1 is entering Timeout Interval')
        # set timeout boolean to True, then Wait for timeout interval
        self.inTimeout = True 
        while self.active and ((time.time() - self.startTime) < self.timeout):
            pass
        self.inTimeout = False 

        print( 'Mode 1 finished its Timeout Period and is now exiting ')
        debug('____________________Mode 1 Fin____________________')

        self.exit()



class mode2(modeABC):
    """This is for the second twelve hours of the experiment, where the door between the chambers is closed. Here, the lever is extended, and controls access to the wheel in the second chamber. Every time the wheel is accessed, the number of presses required for the lever to increase is one.

    Args:
        modeABC (class object): Inherited abstract base class
    """
    
    def __init__(self, timeout, map):
        super().__init__(self, timeout, map)

    def enter(self):
        self.startTime = time.time() 
        self.active = True

    def exit(self):
        self.active = False


    def run(self):


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

        ''''
        class rfid:
            ## not sure what the normal code will look like ## 
            # Simulation Version! #  
            @threaded_fn
            def condition_for_threshold_to_get_set_to_true(): 
                # constantly looping and updating the rfid threshold val 
                if self.ping_queue gets new value: 
                    write val to output 
                    self.threshold = True 
                

        class Wheel: 
            @threaded_fn
            def condition_for_threshold_to_get_set_to_True(): 
                # constantly looping and updating the rfid threshold val 
                if self.moves is True: 
                    self.threshold = True 
                # simulation version of this function would look the same 
                # if the user specified to simulate the wheel, then the sim script will specify at what times the vole interacts with the wheel 
                # when vole interacts with the wheel, we will just directly set wheel.moves to True to "simulate" the movement. 
        class Lever: 
            @threaded_fn 
            def condition_for_threshold_to_get_set_to_true(): 
                if presses == self.required_presses: 
                    self.threshold = True 
            ## Simulation Version of this Function would look the same ##
            # if the user specified that we are simulating the lever (no physical hardware), then the user will directly specify in their simulation 
            # script that the vole should press the lever, by simply directly adding one to the self.pressed count 
            # ( or this will happen randomly if we are running a random_vole_moves() experiment ) 

        class Door: 
            @threaded_fn 
            def condition_for_threshold_to_get_set_to_true(open): 
                if open is True: # set threshold to True after successfully opening door 
                    self.open_door() 
                    self.threshold = True
                else: # set threshold to True after successfully closing door 
                    self.close_door() 
                    self.threshold = True

                    ~~~~~ simulation version of this funciton ~~~~    
                    ## If the user wants to abstract away from physical hardware, override the condition_for_threshold function ## 
                    ## ensures that we don't call any functions that interact with the rpi ## 
                    ## Simulation should Override the function condition_for_threshold_to_get_set_to_true(): 
                    def condition_for_threshold_to_get_set_to_true(open): 
                        if open is True: 
                            print('opening door')
                            self.threshold = True 
                        if open is False: 
                            print('closing door')
                            self.threshold = True 
            
            def isOpen(): 
                return state_switch # hardware! 
            def open_door(): 
                raspberry_pi_things.open # hardware
                if state_switch: # hardware! 
                    self.isOpen = True 
            def close_door(): 
                rpi.close # hardware! 
                if state_switch: #hardware!
                    self.isOpen = False         
        '''



        '''
        class rfid: 
            @threaded_fn 
            def condition_for_threshold_to_get_set_to_True(): 
                # constantly looping and updating the rfid threshold val
                if 3 items have been added to self.ping_queue: 
                    self.threshold = True 
        '''
        '''
            if self.box.rfid1.threshold is True: 
                self.box.door1.open() 
        '''
        print('Mode 2 is Running')
        # Retract the lever and open the door
        #self.map.chamber_lever.retract()
        #self.map.door.default = True # opened
        #self.map.door.trigger = None # No lever connected


        print('Mode 2 is entering Timeout Interval')
        # set timeout boolean to True, then Wait for timeout interval
        self.inTimeout = True 
        while self.active and ((time.time() - self.startTime) < self.timeout):
            pass
        self.inTimeout = False 

        print( 'Mode 2 finished its Timeout Period and is now exiting ')
        debug('____________________Mode 2 Fin____________________')

        self.exit()

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