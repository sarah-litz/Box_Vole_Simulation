
# Standard Lib Imports 
import site 
import sys
import os
import time

# Local Imports
from ..Logging.logging_specs import sim_log
from ..Classes.SimulationABC import SimulationABC

# 
# This is just an example --> Doesn't actually run yet. (config_testing.py has a more working version)
# 
class SarahsSimulation(SimulationABC): 

    def __init__(self, modes, map):
        
        super().__init__(modes, map) 



        '''Interactable Behavior: 
        - in running a simulation, we will automatically add an attribute to each interactable that allows 
        - default behavior ( if left unchanged )
        '''

        ## Set Interactable Behavior ## 
        # map.instantiated_interactables[]: 

    def mode1_timeout(self): 

        #
        # Script to specify what should happen when we enter mode1's timeout interval
        #
        sim_log(f'(sim_attempt_move.py, SarahsSimulation, mode1_timeout) Running the Mode 1 Simulation')
        print('Running the Mode 1 Simulation ')

        chmbr1 = self.map.graph[1]
        
        vole1 = self.get_vole(1)

        vole1.attempt_move(destination = 1)

        time.sleep(5)

        # self.simulate_interactable(chmbr1.interactables['door1'].dependent['lever1'].simulate(vole=1))

        print('Exiting the Mode 1 Simulation')

    def mode2_timeout(self): 

        #
        # Script to specify what should happen when mode2 enters its timeout interval
        #
        sim_log(f'(sim_attempt_move.py, SarahsSimulation, mode2_timeout) Running the Mode 2 Simulation')

        print('Running the Mode 2 Simulation')

        vole1 = self.get_vole(1)

        vole1.attempt_move(destination=2)

        time.sleep(5)

        print('Exiting the Mode 2 Simulation')
        return 





    
