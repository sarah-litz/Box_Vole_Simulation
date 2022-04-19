'''
Title: Simulation Executable
description:this file links a specified simulation class (a file w/in the Simulation/Scripts directory) 
            to run on top of a specified experimental class (a file w/in the Control/Scripts directory).
            
            If you want to change the script that will execute for the simulation and/or experiment, you will need to change the 
            import statements and the statements where the simulation and mode classes are instantiated. 
            This file contains a (TODO) to denote each of the places that these updates should be made. 
'''


# Imports
import os 
cwd = os.getcwd() # current working directory
import time
from .Logging.logging_specs import sim_log
from Control.Classes.Map import Map



# (TODO) Import Your ModeABC Implementations Here using the following syntax: from Control.Scripts.your_file_name import modeName1, modeName2, etc. 
from Control.Scripts.ModeScripts1 import mode1, mode2

# (TODO) Import your SimulationABC Implementations Here using the following syntax: from .Scripts.your_file_name import SimulationClassName
from .Scripts.SarahsSimulation import SarahsSimulation


# Map Instantiation (which will also instantiate the hardware components) 
map = Map(cwd+'/Control/Configurations')


sim_log('\n\n\n\n-----------------------------New Simulation Running------------------------------------')


# (TODO) instantiate the modes that you want to run -- this should use the classes that you imported in the first "todo"
mode1 = mode1( timeout = 60, map = map ) 
mode2 = mode2( timeout = 60, map = map )


# (TODO) instantiate the Simulation, pass in the Mode objects, map, and Voles to create -- this should be using the class you imported in the second "todo"
# (TODO) in the modes argument, pass a list of all of the modes that you instantiated above. These should get passed in in the same order that they will run in.
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

# (TODO) start experiment 

mode2.enter() 
#mode2.run() 


mode1.enter() 
#mode1.run() 

