import unittest 
unittest.TestLoader.sortTestMethodsUsing = None
from Map import Map 
from Simulation import Simulation

#
# Vole Testing
#
class VoleTestCase(unittest.TestCase): 

    map = Map()
    sim = Simulation(map)

    def test1_new_vole(self): 
        self.sim.map.new_chamber(1) 
        self.sim.map.new_chamber(2)
        self.sim.new_vole(101, 1)
        self.sim.new_vole(102, 1)
        self.sim.draw_map()



#
# Map Testing 
#
class MapTestCase(unittest.TestCase): 


    
    map = Map() 

    def test1_new_chamber(self): 
        self.map.new_chamber(1) 
        self.map.new_chamber(2)
        self.map.new_chamber(3)
        self.map.new_chamber(4)

    def test2_new_edge(self): 
        self.map.new_shared_edge(12,1,2)
        self.map.new_shared_edge(13,1,3)
        self.map.new_shared_edge(14,1,4)
    
    
    def test3_new_component(self): 

        edge14 = self.map.graph[1].connections[4] # grabs the shared edge w/ id 14 that goes from 1<->4

        # Add Components
        edge14.new_component('food')
        edge14.new_component('water')
        edge14.new_component('wheel')


        # Different Method of getting an Edge: 
        edge12 = self.map.get_edge(12)
        edge12.new_component('wheel')    

    def test4_get_component(self): 
        
        edge12 = self.map.get_edge(12)
        print('edge 12: ', edge12)
        print('Wheel Located? ', edge12.get_component('wheel') ) 
        print('Door located? ', edge12.get_component('door'))


        edge14 = self.map.get_edge(14)
        print('edge 14: ', edge14)
        print('Water Located? ', edge14.get_component('water'))

        self.map.print_graph_info()
    

if __name__ == '__main__': 
    unittest.main()
