from Vole import Vole
from Map import Map
import copy

class Simulation: 

    def __init__(self, map): 
        
        self.voles = []
        self.map = map

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
            
        
    '''
    def setup(self)
    def run(self)
    def reset(self)

    def new_vole(self) 
    def 
    '''

        