
# Standard Lib Imports 
import time 

from Logging.logging_specs import debug, sim_log, control_log


# Local Imports 
from Simulation import SimulationABC
from Map import Map
from ryan_example1 import mode1, mode2

# 
# This is just an example --> Doesn't actually run yet. (config_testing.py has a more working version)
# 
class SarahsSimulation(SimulationABC): 

    def __init__(self, modes, map, vole_dict={}):
        
        super().__init__(modes, map, vole_dict) 



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
        
        # chmbr1.interactables['wheel1'].simulate(vole=1)
        #self.simulate_interactable(chmbr1.interactables['wheel1'], vole=1) 


        vole1 = self.get_vole(1)

        vole1.attempt_move(destination = 2)

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

        vole1.attempt_move(destination=1)

        time.sleep(5)

        print('Exiting the Mode 2 Simulation')
        return 




if __name__ == '__main__': 


    # instantiate map (which will also instantiate the hardware components) 
    map = Map('/Users/sarahlitz/Projects/Donaldson Lab/Vole Simulator Version 1/Box_Vole_Simulation/Classes/Configurations')

    res = map.get_edge(12).get_interactable_from_component('rfid1').__getattribute__('check_threshold_with_fn')
    print(res.__name__)


    sim_log('\n\n\n\n-----------------------------New Simulation Running------------------------------------')
    

    # instantiate the modes that you want to run
    mode1 = mode1( timeout = 15, map = map ) 
    mode2 = mode2( timeout = 15, map = map )

    
    # instantiate the Simulation, pass in the Mode objects, map, and Voles to create
    sim = SarahsSimulation( modes = [mode1, mode2], map = map, vole_dict = { 1:1, 2:1 }  ) 
    
    sim_log(f'(sim_attempt_move.py, {__name__}) New Simulation Created: {type(sim).__name__}')

    # simulation visualizations
    sim.draw_chambers() 
    sim.draw_edges() 


    time.sleep(5) # pause before starting up the experiment 

    # indicate the simulation function to run when the mode enters timeout 
    # optional second argument: indicate the number of times to run the simulation function. If this value is not passed in, then the simulation loops until the experiment finishes its timeout interval. 
    sim.simulation_func[mode1] = (sim.mode1_timeout, 1)
    sim.simulation_func[mode2] = (sim.mode2_timeout, 1) 

    # runs simulation as daemon thread. 
    t1 = sim.run_sim() 


    # start experiment 
    mode1.enter() 
    mode1.run() 

    mode2.enter() 
    mode2.run() 
    
