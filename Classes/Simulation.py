from Vole import Vole
from Map import Map
import copy

class Simulation: 

    def __init__(self, map, vole_dict={}): 
        
        # TODO: option for passing in voles dictionary, and we immediately initialize the voles as specified by the dictionary
        self.voles = []
        self.map = map

        for (i,c) in vole_dict.items(): self.new_vole(i,c) # instantiate new voles 
    

    #
    # Running the Simulation 
    #
    
    def __setup__(self): 

        raise Exception('you need to overwrite the __setup__ function! This is where you add/initialize any voles that you want to Simulate.')

    def run_sim(self, func_to_run, timeout_interval): 

        # TODO 
        # creates thread with target function 'func_to_run' 
        # returns after timeout_interval is up, even if the simulation function has not completely finished running 
        pass 
    
    #
    # Vole Getters and Setters 
    #
    def get_vole(self, tag): 
        # searches list of voles and returns vole object w/ the specified tag 
        for v in self.voles: 
            if v.tag == tag: return v  
        return None

    def new_vole(self, tag, start_chamber): 
        ''' creates a new Vole object and adds it to the list of voles. Returns Vole object on success '''

        # ensure vole does not already exist 
        if self.get_vole(tag) is not None: raise Exception(f'vole with tag {tag} already exists')

        # ensure that start_chamber exists in map
        if self.map.get_chamber(start_chamber) is None: raise Exception(f'chamber {start_chamber} does not exist')
        
        # Create new Vole 
        newVole = Vole(tag, start_chamber, self.map)
        self.voles.append(newVole)
        return newVole

        
    def remove_vole(self, tag): 
        ''' removes vole object specified by the vole's tag '''
        vole = self.get_vole(tag)
        if not vole: raise Exception(f'vole {tag} does not exist, so cannot be removed')
        self.voles.remove(vole)




    #
    #  Vole/Map Visualization 
    #         
    def draw_chambers(self): 

        for cid in self.map.graph.keys(): 
            
            chmbr = self.map.graph[cid]
            cvoles = [] 

            for v in self.voles: 
                if v.current_loc == chmbr.id: cvoles.append(v.tag)
            print(f'_____________\n|   (C{chmbr.id})    |')

            for v in cvoles: 
                if len(str(v)) > 8: 
                    v = str(v)[:7] + '-'
                space = 8 - len(str(v)) 
                print(f'|V[{v}]' + f"{'':>{space}}" + '|')
            
            for i in chmbr.interactables: 
                if len(str(i)) > 8: 
                    i = i[:7] + '-'
                space = 8 - len(str(i)) 
                print(f'|I[{i}]' + f"{'':>{space}}" + '|')

            print(f'-------------')

    
    def draw_edges(self): 
        edges = self.map.edges
        for e in edges: 
            interactables = [c.interactable for c in e] 
            print(f'({e.v1}) <---{interactables}----> ({e.v2})')
    
    
    
    #
    # Simulate Vole-Interactable Interactations
    #
    def simulate_interactable(self, interactable, vole): 

        interactable.set_threshold(True)

    


        
    '''
    def setup(self)
    def run(self)
    def reset(self)
    '''

        