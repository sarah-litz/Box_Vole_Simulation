
# Standard Lib Imports 
import time 

# Local Imports 
from Simulation import Simulation


class SarahsSimulation(Simulation): 

    def __init__(self):
        
        super().__init__() 
    
    def __setup__(self): 

        # create voles 
        self.new_vole(1, 1)
        self.new_vole(2, 1)
    
    def mode1_timeout(self): 

        #
        # Script to specify what should happen when we enter mode1's timeout interval
        #
          
        chmbr1 = self.map.graph[1]
        
        # chmbr1.interactables['wheel1'].simulate(vole=1)
        self.simulate_interactable(chmbr1.interactables['wheel1'], vole=1) 

        time.sleep(5)

        self.simulate_interactable(chmbr1.interactables['door1'].dependent['lever1'].simulate(vole=1))


    def mode2_timeout(self): 

        #
        # Script to specify what should happen when mode2 enters its timeout interval
        #


        pass 