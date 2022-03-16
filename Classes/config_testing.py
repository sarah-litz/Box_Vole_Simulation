
from ftplib import FTP_PORT
from Map import Map 
from Simulation import Simulation 
from run_sim_example import SarahsSimulation



# Map Configuration Filepath
fd = '/Users/sarahlitz/Projects/Donaldson Lab/Vole Simulator Version 1/Box_Vole_Simulation/Classes/Configurations'
fp = '/Users/sarahlitz/Projects/Donaldson Lab/Vole Simulator Version 1/Box_Vole_Simulation/Classes/Configurations/map.json'

#
# Setup Simulation w/ Map Specifications
#

# setup map 
map = Map(fd) 

# setup hardware
# LEAVING OFF HERE!!! 
map.configure_setup(fp) # TODO: leaving off here!! Figure out why errors aren't getting thrown when adding an interactable with weird name types

# setup simulation
# sim = Simulation(map = map, vole_dict = {1:1, 2:1, 3:1, 4:2} ) 
# map = sim.map

sim2 = SarahsSimulation(map = map)


#
# Visualize Map after Setup
# 
map.print_graph_info()
sim2.draw_chambers() 
sim2.draw_edges()


