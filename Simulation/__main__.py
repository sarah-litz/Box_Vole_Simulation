
# Standard Lib Imports 
import os 
cwd = os.getcwd() # current working directory
import time

# Local Imports 
from .Logging.loggingspecs import sim_log
from Control.Classes.Map import Map

# (TODO) Import Your ModeABC Implementations Here using the following syntax: from Control.Scripts.your_file_name import modeName1, modeName2, etc. 
from Control.Scripts.ryan_example1 import mode1, mode2

# (TODO) Import your SimulationABC Implementations Here using the following syntax: from .Scripts.your_file_name import SimulationClassName
from .Scripts.sim_attempt_move import SarahsSimulation


# Map Instantiation (which will also instantiate the hardware components) 
map = Map(cwd+'/Control/Configurations')


sim_log('\n\n\n\n-----------------------------New Simulation Running------------------------------------')


# (TODO) instantiate the modes that you want to run -- this should use the classes that you imported in the first "todo"
mode1 = mode1( timeout = 15, map = map ) 
mode2 = mode2( timeout = 15, map = map )


# (TODO) instantiate the Simulation, pass in the Mode objects, map, and Voles to create -- this should be using the class you imported in the second "todo"
sim = SarahsSimulation( modes = [mode1, mode2], map = map  ) 

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