
from Map import Map 
from Simulation import Simulation 


sim = Simulation(Map())
map = sim.map 
fp = '/Users/sarahlitz/Projects/Donaldson Lab/Vole Simulator Version 1/Box_Vole_Simulation/Classes/map_config.json'
map.configure_setup(fp)
map.print_graph_info()
sim.draw_chambers() 
sim.draw_edges()