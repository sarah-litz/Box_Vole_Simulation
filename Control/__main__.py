
# Imports
import os 
cwd = os.getcwd()
from .Logging.loggingspecs import control_log
from .Classes.Map import Map 

# (TODO) Import Your ModeABC Implementations here using the following syntax: from Scripts.your_file_name import mode_name_1, mode_name_2, etc.
from .Scripts.ryan_example1 import mode1, mode2 


control_log(f'\n\n\nrunning {__name__}: New Experiment! ')

# Map Instantiation (which will also instantiate the hardware components) 
map = Map(cwd+'/Control/Configurations')

# (TODO) instantiate the modes that you want to run -- this should use the classes that you imported in the first "todo"
mode1 = mode1(timeout = 8, map = map)
mode2 = mode2(timeout = 8, map = map)


# start experiment
mode1.enter()
mode1.run()

mode2.enter() 
mode2.run() 
