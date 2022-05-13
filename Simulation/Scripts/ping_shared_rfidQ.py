
# Standard Lib Imports 
import site 
import sys
import os
import time

# Local Imports
from ..Logging.logging_specs import sim_log
from ..Classes.SimulationABC import SimulationABC



class SimulatePings(SimulationABC): 

    def __init__(self, modes, map):
        
        super().__init__(modes, map) 

        self.modes = modes 
    

    def mode1_timeout(self): 

        ## Logic for when Mode 1 Control Software Enters Timeout ## 
        ## Control Software Mode 1: Open Cage ## 
        

        # 
        # Simulation Goal: Test the shared RFID queue functionality where control's Mode class listens for things to get added to shared q, and then notifies the corresponding rfid object if there is a ping. 
        # 

        self.map.instantiated_interactables['rfid1'].simulate = False # we don't want to simulate rfid1 in this one in order to test the functionality of modeABC.py shared_rfidQ and rfidListener() functionality

        mode = self.modes[0] 
        
        vole2 = self.get_vole(2) # vole 2 is sending the ping 
        rfid_tag = 1 # this will notify the rfid object with id=1
        mode.shared_rfidQ.put( (rfid_tag, vole2.tag, time.time()) ) # Artificial Ping 

        print('ping done')


    def mode2_timeout(self): 

        pass 

    def mode3_timeout(self): 
        # Control Software Mode3: same as Mode2. Closed box, lever1 will open door1. 

        #
        # Simulation Goal: 2 Voles that make a move at the same exact time (need to implement threading for the voles) 
        #

        pass 