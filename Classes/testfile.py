import unittest 
from Map import Map 


#
# Map Testing 
#
class MapTestCase(unittest.TestCase): 


    def est_new_chamber(self): 
        print(f'\nTest Case 1: New Chamber')
        map = Map() 
        map.new_chamber(5)
        map.new_chamber(2)
        map.print_graph_info()

    def est_new_edge(self): 
        print(f'\nTest Case 2: New Edge')
        map = Map() 
        map.new_chamber(1)
        map.new_chamber(2)
        try: map.new_bidirectional_edge(12,1,2)
        except Exception as e: print('Exception:', e)
        map.print_graph_info()
    
    
    def test_new_component(self): 
        map = Map() 
        map.new_chamber(1)
        map.new_chamber(2)
        map.new_shared_edge(12,1,2)
        

        map.new_chamber(4)
        map.new_shared_edge(14,1,4)
        edge14 = map.graph[1].connections[4]
        edge14.new_component('food')
        edge14.new_component('water')


        # Add Component 
        try: 
            edge = map.get_edge(12)
            edge.new_component('wheel')
        except Exception as e: print('Exception:', e)

        map.print_graph_info()
        

if __name__ == '__main__': 
    unittest.main()
