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

        print('---- EDGE 12 ------')
        for c in edge12: 
            print(c)
        
        chamber1.new_interactable('C1Food')
        
        self.sim.new_vole(1,1)
        self.sim.new_vole(2,1)
        self.sim.new_vole(3,2)

        self.sim.draw_chambers() 
        self.sim.draw_edges()
    
    def test2_move_validity_check(self): 

        print('Move Request Result: ',self.sim.get_vole(1).is_move_valid(destination=2))
        print('Move Request Result: ', self.sim.get_vole(3).is_move_valid(destination=3))
    
    def test3_attempt_move(self): 

        vole1 = self.sim.get_vole(1)
        vole1.attempt_move(2) 

    def est4_remove_vole(self): 
        print([i.tag for i in self.sim.voles])
        self.sim.remove_vole(tag=1)
        print([i.tag for i in self.sim.voles]) 
    
    def test5_random_voles(self): 
        vole4 = self.sim.new_vole(4,1)
        vole4.random_action() # LEAVING OFF HERE; don't think this function is entirely working


if __name__ == '__main__': 

     unittest.main()