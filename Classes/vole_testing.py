import unittest 
unittest.TestLoader.sortTestMethodsUsing = None
from Map import Map
from Simulation import Simulation



class VoleTests(unittest.TestCase): 
    sim = Simulation(Map())
    map = sim.map 

    #
    # Initalize Map and Voles 
    #
    def test1_add_stuff(self): 
        chamber1 = self.map.new_chamber(1)
        chamber2 = self.map.new_chamber(2)
        chamber3 = self.map.new_chamber(3)
        
        edge12 = self.map.new_shared_edge(12,1,2)
        edge13 = self.map.new_shared_edge(13,1,3)

        
        edge12.new_component('water')
        edge12.new_component('wheel')
        edge12.new_component('couch')
        edge12.new_component('bed')
        chamber1.new_interactable('C1Food')
        
        self.sim.new_vole(1,1)
        self.sim.new_vole(2,1)
        self.sim.new_vole(3,2)

        self.sim.draw_chambers() 
        self.sim.draw_edges()
    
    def test2_send_move_request(self): 

        print('Move Request Result: ',self.sim.get_vole(1).send_move_request(destination=2))
        print('Move Request Result: ', self.sim.get_vole(3).send_move_request(destination=3))
    
    def test3_make_move(self): 
        pass 

    def test4_remove_vole(self): 
        print([i.tag for i in self.sim.voles])
        self.sim.remove_vole(tag=1)
        print([i.tag for i in self.sim.voles]) 


if __name__ == '__main__': 
    unittest.main()