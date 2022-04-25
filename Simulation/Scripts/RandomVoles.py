
# Standard Lib Imports 
import site 
import sys
import os
import time

# Local Imports
from ..Logging.logging_specs import sim_log
from ..Classes.SimulationABC import SimulationABC



class RandomVoles(SimulationABC): 

    def __init__(self, modes, map):
        
        super().__init__(modes, map) 

        self.modes = modes 
    

    def mode1_timeout(self): 

        ## Logic for when Mode 1 Control Software Enters Timeout ## 
        ## Control Software Mode 1: Open Cage ## 
        

        # 
        # Simulation Goal: 1 Vole that makes random moves throughout the timeout
        # 


        # (NOTE) need to implement vole function that while in timeout, the vole just makes random moves 

        vole1 = self.get_vole(1)

        while self.modes[0].inTimeout: 
            vole1.attempt_random_action() # vole 1 makes random actions while in timeout 


    def mode2_timeout(self): 

        ## Logic for when Mode 2 Control Software Enters Timeout ## 
        ## Control Software Mode 2: Closed Cage, Lever1 Opens Door1, then lever.required_presses increases by 1 ## 

        #
        # Simulation Goal 2: 2 Voles that make a move at the same exact time (need to implement threading for the voles) 
        #
        vole1 = self.get_vole(1)
        vole1.attempt_random_action() 
        pass 