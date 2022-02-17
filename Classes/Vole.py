


class Vole: 

    def __init__(self, tag, start_chamber, map): 
        self.tag  = tag 
        self.current_loc = start_chamber
        self.map = map 
    

    #
    # Vole Movements
    #
    def send_move_request(self, destination): 
        '''Check validity of making a move from voles current location to some destination 
        Does not actually make move/update the voles location, just checks if the move is possible according to map layout 
        Return True if move is possible, False otherwise 
        '''
        curr_chamber = self.map.graph[self.current_loc]
        if destination in curr_chamber.connections.keys(): 
            return True 
        else: return False
    

    def make_move(self, destination): 
        ''' executes a move. Assumes that we have already checked if move is valid or not. '''
        
        # retrieve edge between current location and the destination, and check threshold for each of these 

    def make_multichamber_move(self, goal): 
        pass 



    #
    # Component Simulation; simulates Vole's interaction w/ some interactable 
    # 
    ## TODO: simulate_component and make_move needs Work based on Control Software ## 
    def simulate_component(self, obj): 

        # (OPTION 1) set threshold to True, simulating to the control software that a certain threshold condition has been met 
        obj.set_threshold(True)

        # (OPTION 2) each object will contain logic w/in control software that makes the exact "moves" to meet the threshold 
        obj.meet_threshold(goal=True)

        
    def send_interaction_requestion(self, interactable): 
        ''' Checks validity of interacting with some interactable/component 
        Does not simulate any interaction, just checks if it is possible according to map layout 
        Return True if interaction is possible, False otherwise 
        '''
        pass 

    def reset_components(self): 
        pass 
