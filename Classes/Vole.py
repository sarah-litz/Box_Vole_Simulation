


import random
import time 

class Vole: 

    def __init__(self, tag, start_chamber, map): 
        self.tag  = tag 
        self.current_loc = start_chamber
        self.map = map 
    

    #
    # Vole Movements
    #

    ## TODO: make_move and make_multichamber_move need work based on Control Software
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
        pass 

    def make_multichamber_move(self, goal): 
        pass 
     
    def random_move(self): 
        ''' chooses a random neighboring chamber to try to move to '''




    #
    # Component Simulation; simulates Vole's interaction w/ some hardware interactable 
    # 
    ## TODO: simulate_component and make_move needs Work based on Control Software ## 
    def simulate_interactable(self, obj): 

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





    #
    # Random Vole 
    #   
    def possible_actions(self): 
        ''' returns a list of all possible actions a vole can take given the voles current location'''
        # Reference on how to add functions to a list, where we will call the function at a later point in time: https://stackoverflow.com/questions/26881396/how-to-add-a-function-call-to-a-list
        '''
        possible_actions is a list of tuples, where each tuple contains a function to call followed by the arguments to pass that function
        -> the 0th position w/in each tuple is the function name, and positions [1:] in the tuple are the arguments
        -> possible_actions[0][0](*possible_actions[0][1:])
        -> possible_actions[1][0](*possible_actions[1][1:])
        '''

        actions = [ (time.sleep,5)  ]  # initialize with option to do nothing, as this action is always available, independent of the vole's current location


        # add all possible "move chamber" options 
        for adj_chmbr in self.map.graph[self.current_loc].connections: # for all of the current chamber's neighboring chambers
            actions.append( (self.make_move, adj_chmbr) ) # add to list of possible moves 
        
        # add all possible "interact w/ chamber interactables" options
        for interactable in self.map.graph[self.current_loc].interactables: # for all of the interactables in the current chamber
            actions.append( (self.simulate_interactable, interactable) )
        
        return actions




    def random_action(self): 
        ''' Randomly choose between interacting with an interactable or making a move or doing nothing'''

        '''
        randomly choose between the following options: 
        1. pass, i.e. vole sits still. Have vole sleep for 1<x<10 number of seconds. 
        2. vole interacts w/ an interactable in its chamber (look @ self.map.graph[self.current_loc].interactables to randomly choose an interactable to interact with)
        3. vole attempts to make a move to a random chamber (look @ self.map.graph[self.current_loc].connections to randomly choose a neighboring chamber to choose to)
        '''

        possible_actions = self.possible_actions()
        
        # randomly choose action to take from list of possible_actions
        idx = random.randint(0, len(possible_actions)-1)
        # LEAVING OFF HERE
        possible_actions[idx][0]( *possible_actions[idx][1:] )


    

    def set_action_probability(self, action, probability): 

        ''' adjust the probability of Vole taking a certain action, where vole either sleeps, interacts w/ interactables, or moves chambers
        automatically adjusts the probability of the other actions accordingly 
        e.g. if we increase probability of action=sleep to 10%, then we will auto-adjust the probability of action and interactable to 45% each. 
        '''
        
    
