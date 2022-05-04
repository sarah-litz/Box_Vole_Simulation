"""
Authors: Sarah Litz, Ryan Cameron
Date Created: 1/24/2022
Date Modified: 4/6/2022
Description: Class definition for a simulated vole. Contains methods that allow for a vole to move throughout a box and simulate interactions with interactables along the way.

Property of Donaldson Lab at the University of Colorado at Boulder
"""


# Standard Lib Imports 
from itertools import count
import random
from re import I
import time 

# Local Imports 
from ..Logging.logging_specs import sim_log
from .Timer import countdown

class Vole: 

    def __init__(self, tag, start_chamber, map): 
        
        self.tag  = tag 
        self.map = map 

        ## Vole Location Information ## 
        # LEAVING OFF HERE!!! need to finish going thru and correcting all the spots in code where I reference self.current_loc
        self.curr_loc = self.map.get_chamber(start_chamber)

        # starting position between interactables is between chamber edge or wall and the first interactable in the chamber, if it exists
        self.prev_component = None # last interactable that vole moved away from (so we know the direction of movement)
        try: self.curr_component = self.curr_loc.headval # current interactable the vole is closest to
        except AttributeError: self.curr_component = None # (interactable1, interactable2)
        print(f'VOLE {self.tag} POSITION BETWEEN INTERACTABLES: {self.prev_component}, {self.curr_component}')
        

        '''self.prev_interactable = None # last interactable that vole moved away from (so we know the direction of movement)
        try: self.curr_interactable = self.curr_loc.headval.interactable # current interactable the vole is closest to
        except AttributeError: self.curr_interactable = None # (interactable1, interactable2)
        print(f'VOLE {self.tag} POSITION BETWEEN INTERACTABLES: {self.prev_interactable}, {self.curr_interactable}')
        '''
    

    
    ##
    ## Simulating Interactable thru setting attribute value or thru function call
    ##


    def update_location(self, newcomponent=None): 
        #TESTME
        ''' 
        updates vole's current component position 
        if current component position is None, then check to see if we need to update the vole's chamber/edge/id location 
        '''

        # make sure that the current chamber/edge/id reflects the newcomponent 
        prev_loc = self.curr_loc 
        self.curr_loc = self.map.get_location_object(newcomponent.interactable) 
        if prev_loc != self.curr_loc: 
            print(f'Vole {self.tag} traveled from {prev_loc.edge_or_chamber}{prev_loc.id} into {self.curr_loc.edge_or_chamber}{self.curr_loc.id}')

        self.prev_component = self.curr_component 
        self.curr_component = newcomponent 

        print(f'Updated Vole Interactable Location from {self.prev_component} to {self.curr_component} ')


    def pre_simulation_error_checks(self, interactable): 
        ''' checks for a bunch of edge cases to ensure that the called simulation is valid '''
    def simulate_autonomous_interactable(self, interactable): 
        ''' really this just applies to rfids at the moment. '''
        ''' any interactable that is classified as a Barrier interactable AND has no dependents is considered to be autonomous, and can be simulated by this quicker function. (skips all of the dependent loops and things) '''
     

    def at_location_of(self, interactable): 
        ''' 
            Physical Proximity Check: returns True if vole's location is at the current interactable, false otherwise.
            Depends on both the chamber/edge vole is in, as well as where the vole is positioned w/in the chamber. 
        '''

        if self.curr_component.interactable.name == interactable.name:
            return True 
        else: 
            return False 


        
    def simulate_vole_interactable_interaction(self, interactable): 

        ''' called from vole.attempt_move() in order to simulate a vole's interaction with an interactable '''
        ''' prior to simulation, checks if the requested simulation is valid. returns if not '''

        #
        # Independent vs Dependent check 
        #
        if len(interactable.dependents) > 0: 
            # a fully independent interacable means that it is dependent on the values of its dependents and independent of a vole's actions
            # i.e. it is pointless for the vole to interact directly with it. So return. (Doesn't mean we won't interact and simulate w/ its dependents tho)
            print(f'(Vole.py, simulate_vole_interactable_interaction) {interactable.name} isDependent on dependents, not on a vole interaction.')
            return 

        #
        # Active Check
        #
        if interactable.active is False: 
            print(f'(Vole.py, simulate_vole_interactable_interaction) {interactable.name} is inactive')
            # we don't care to simulate an inactive interactable
            # vole unable to effect the threshold attribute value of an inactive interactable (so threshold value is the same the entire time)
            return 

        #
        # Physical Proximity Check 
        #
        if not self.at_location_of(interactable): 
            print(f'(Vole.py, simulate_vole_interactable_interaction) vole{self.tag} is not at_location_of({interactable.name}). Failed the physical proximity check; cannot simulate.')
            return 




        #
        # Simulate
        #
        if interactable.simulate: 

            sim_log( f'(Vole.py, simulate_vole_interactable_interaction) simulating vole{self.tag} interaction with {interactable.name}' ) 
            print(f'(Vole.py, simulate_vole_interactable_interaction) Simulating vole{self.tag} interaction with {interactable.name}')
    
            if hasattr(interactable, 'simulate_with_fn'):
                
                # sets the attributes to values that meet the threshold condition by calling simulate_with_fn 
                interactable.simulate_with_fn(interactable, self.tag)

            else:
                
                # set value using the threshold condition attribute/value pairing 
                threshold_attr_name = interactable.threshold_condition["attribute"]
                # attribute = getattr(interactable, threshold_attr_name) # get object specified by the attribute name

                sim_log(f'(Vole.py, attempt_move) {interactable.name}, threshold attribute: {threshold_attr_name}, threshold value: {interactable.threshold_condition["goal_value"]}')
            
                # manually set the attribute to its goal value so we meet the threshold condition, and trigger the control side to add an event to the threshold_event_queue 
                setattr(interactable, threshold_attr_name, interactable.threshold_condition['goal_value'])
                
                newattrval = getattr(interactable, threshold_attr_name)
                # sim_log(f'{interactable.name}, manual attribute check: {interactable.state}')
                sim_log(f"(Vole.py, attempt_move) {interactable.name}, attribute result: {newattrval}")
            
            # countdown(5, f'simulating vole{self.tag} interaction with {interactable.name}')
    
        
        else:  # component should not be simulated, as the hardware for this component is present. 
            # assumes that there is a person present to perform a lever press, interrupt the rfid reader so it sends a ping, etc. 
            print ( f'\nif testing the hardware for {interactable.name}, take any necessary actions now.')
            # countdown(10, f'remaining to perform interactions to trigger a threshold event for {interactable.name}')
            
    
    
    ##
    ## Vole Movements
    ##
    def is_move_valid(self, destination): 
        # TESTME
        # attempt_move helper function
        '''Check validity of making a move from voles current location to some destination 
        Does not actually make move/update the voles location, just checks if the move is possible in a single move according to map layout 
        Return True if move is possible, False otherwise 
        '''
        # destination must be a chamber 
        # vole can be currently sitting on an edge or in a chamber 

        if self.curr_loc.edge_or_chamber == 'chamber': 
            if destination in self.curr_loc.connections.keys(): 
                return True # chamber has edge connecting it to destination 
        else: 
            if destination == self.curr_loc.v1 or destination == self.curr_loc.v1: 
                return True # edge is connected to destination chamber
        return False  
    

    def interactable_path ( self, destination, forward_ ): 

        ''' returns list of interactables that exist betewen the voles current location and the desired destination '''
        # use vole's starting position between interactables 

        # we want to grab everything on the edge that we need to traverse 

        # as we sort thru the edge components, if we encounter an 

    def move_next_component(self, component): 

        ''' vole positions itself in front of component. component specified must be a component that only requires a singular position change. '''
        ''' this does NOT simulate any interactions with this interactable. i.e. the component we are currently standing at has not necessarily been passed (aka threshold met) yet. But we are able to interact with it.'''
        

        print(f'move_next_component entered. Goal: {self.curr_component.interactable}->{component.interactable}')
        

        def getInteractable(component): 
            ## try except statement for retrieving components interactable. If component is None, this prevents errors from gettting thrown. ## 
            try: return component.interactable
            except AttributeError: return None


        # Interactables At/Around Vole's Current Position
        curr_interactable = getInteractable(self.curr_component)
        nxt_interactable = getInteractable(self.curr_component.nextval)
        prev_interactable = getInteractable(self.curr_component.prevval)

        # Interactables At/Around Goal Position 
        goal = getInteractable(component)
        goal_nxt = getInteractable(component.nextval)
        goal_prev = getInteractable(component.prevval)



        if curr_interactable == goal: 
            
            return  
        
        if nxt_interactable != goal and prev_interactable != goal: # if curr_component->nxt.interactable != goal AND currcomponent->prev != goal

            # possible that the next component is on an adjacent edge/chamber to the vole's current location 

            # extra check for scenario that current component is a chamber component
            if goal_prev != curr_interactable and goal_nxt != curr_interactable: # this scenario will happen when chamber interactables are added to an edge 
                # if goal->prev != curr_component ( if the target interactable doesn't link back to our current interactable )
                # if goal->nxt != curr_component ( if the target interactable doesn't link forward to our current interactable )
                # invalid move request 

                print(f'(Vole.py, move_next_component) only accepts components as arguments that are directly next to the voles location: {self.curr_component}. prev={self.curr_component.prevval}, next={self.curr_component.nextval}. The arugment passed in {component} has prev={component.prevval} and next={component.nextval}')
                return 

            else: 

                pass # valid move requested from a chamber component -> adjacent edge component

        
        #
        # Check that we are able to move past the interactable that vole is currently positioned at 
        #
    
        # interactable is not a barrier 
        if curr_interactable.barrier is False: 
            # we can make move freely, update location 
            return self.update_location(component)
                

        # barrier interactables require that threshold is True, or possible simulation 
        if curr_interactable.threshold is True: 
            # threshold is True, we can freely make move 
            print(f'(Simulation/Vole.py, move_next_component) the threshold condition was met for {curr_interactable}. Vole{self.tag} making the move from {self.curr_component} to {component}.')
            return self.update_location(component)


        # barrier interactable with false threshold. Check if we can simulate without dependents 
        if len(curr_interactable.dependents) > 0: 
            # component requires dependent interaction in order to get threshold to become True. This would require other movements, so exiting from this request 
            print(f'(Simulation/Vole.py, move_next_component) Movement from {self.curr_component}->{component} cannot be completed because {self.curr_component} threshold is False, and would require interactions with its dependents in order to pass.')
        

        else: 
            # component does not have dependents, so can simulate in a simple step. 
            self.simulate_vole_interactable_interaction(curr_interactable)
            time.sleep(5) 
            if curr_interactable.threshold: # recheck the threshold 
                print(f'(Simulation/Vole.py, move_next_component) the threshold condition was met for {curr_interactable}. Vole{self.tag} making the move from {self.curr_component} to {component}.')
                # update location 
                return self.update_location(component)
            else: 
                print(f'(Simulation/Vole.py, move_next_component) Movement from {self.curr_component}->{component} cannot be completed because after simulating {self.curr_component} the threshold is still False.')
                return 




        

    def attempt_move( self, destination, validity_check = True ): 
        ''' called by a Vole object ''' 
        ''' attempts to executes a move. if validity_check is set to True, then we check if the move is physically valid or not. '''
        ''' SETTING the interactable's to meet their goal_value by calling simulate_vole_interaction '''
        ''' GETTING the thresholds of each interactable and checking that it is True '''
        ''' if the threshold of any interactable is not True, then we cannot successfully make the move '''

        sim_log(f'(Vole.py, attempt_move) Entering the attempt move function. Vole {self.tag} is currently in {self.curr_loc.edge_or_chamber}{self.curr_loc.id}. Destination: {destination}.')

        if validity_check: 

            if not self.is_move_valid(destination): 
                # print reason that move is invalid, and then return.
                if self.curr_loc == destination: 
                    sim_log(f'(Vole.py, attempt_move) Vole{self.tag} is already in chamber{destination}!')
                    print(f'(Vole.py, attempt_move) Vole{self.tag} is already in chamber {destination}!')
                else: 
                    sim_log(f'(Vole.py, attempt_move) attempting a move that is not physically possible according to Map layout. Skipping Move Request')
                    print(f'(Vole.py, attempt_move) attempting a move that is not physically possible according to Map layout. Skipping Move Request.')

                return False


        # compile a list of interactables we need to pass over to reach destination (include both chamber and edge interactables)
        
        # sort thru chamber interactables, and only add the ones that are related to the goal movement (i.e. they are a barrier or they)

        # then, we can update the vole's location by using the interactable location info 


        # # # # # # # # # # # # # # # # 
        # retrieve edge between current location and the destination, and check threshold for each of these 
        edge = self.curr_loc.connections[destination]

        sim_log(f'(Vole.py, attempt_move) traversing the edge: {edge}')

        # check if we need to do a forwards or backwards traversal of the edge components 
        if destination == edge.v1: 
            # reverse order of the components 
            edge = edge.reverse_components() 
            reversed = True 
        
        else: 
            # converts to list of components
            edge = edge.get_component_list()
            reversed = False 

        #
        # Edge Traversal 
        #

        ## for now, assuming that the vole just needs to traverse an edge. will deal with chamber movement later. 

        # position start location along the edge to be where the vole's current position is 
        # if the current position is None, then we will start at the beginning of the list and loop thru all components on edge.
        # if the current position is Not None, traverse along edge until we find edge component, where self.curr_component == component

        # begin simulation from the vole's current interactable position. 
        if self.curr_component is None: 
            self.curr_component = edge[0] # first component on edge 
 
        # remove components that come before vole's current position 
        i = 0
        while self.curr_component.interactable.name != edge[i].interactable.name: 
            i+=1 
        edge = edge[i::]

        # traverse the linked list containing the edge components 
        for i in range(len(edge)):

            component = edge[i] 
            for c in edge: print(c)
            self.move_next_component(edge[i])
            # print(f'Updated Vole Interactable Location from {self.prev_component} to {self.curr_component} ')

            # check that vole's position allows us to simulate
            if self.curr_component.interactable.name != component.interactable.name: 
                
                raise Exception(f'(Vole.py, attempt_move) Vole is positioned at {self.curr_component}, so unable to simulate interaction with {component.interactable.name}')
                print(self.curr_component, component)
                pass 
            
            else: 
                 
                #
                # Simulation for Single Interactable
                #
                interactable = component.interactable
                for dependent in interactable.dependents:
                    self.simulate_vole_interactable_interaction(dependent)
                self.simulate_vole_interactable_interaction(interactable) # function call which simulates interaction thru function call or changing vals of specified attributes




                
                #
                # Wait for Control Side Software to react to Simulation of this Interactable
                #
                ################################################
                time.sleep(10)  # Pause to give control side a moment to assess if there was a threshold event 
                ################################################




                #
                # Check if Threshold has been met, in which case Vole completed correct moves to "pass" this interactable
                #

                # self.pass_interactable(interactable)

                # The only thresholds that we actually care about are Barrier Interactables 
                # if we encounter an active, barrier interactable (either a door or rfid) that has a False threshold, then something went wrong. 
                # if 
                if not component.interactable.barrier: # non-barrier interactables wont directly prevent a voles movement, so we can move past this one no matter what the threshold is 
                    
                    pass 

                else: 
                    
                    # handle barrier components 
                    print(f'(Simulation/Vole.py, attempt_move) Barrier Component Handling: {component}')

                    if (component.interactable.active and not component.interactable.threshold): # active component with a false threshold
                        # if the threshold condition was not met, then display message to tell user that attempted move was unsuccessful, and return from function. 
                        print(f'(Simulation/Vole.py, attempt_move) the threshold condition was not met for {component.interactable.name}. Vole{self.tag} cannot complete the move from chamber {self.current_loc} to chamber {destination}.')
                        return False 

                    ## Inactive Interactable Handling ## 
                    elif component.interactable.active is False: # inactive component has no way of its threshold getting set to true, so we manually check here 
                        # Inactive means that the component is sitting idle, however, we still want to check if it is currently sitting at its threshold goal state, because if it is the vole can successfully make its move. 
                        threshold_attr_name = component.interactable.threshold_condition["attribute"]
                        attribute = getattr(component.interactable, threshold_attr_name) # get object specified by the attribute name
                        
                        if hasattr(component.interactable, 'check_threshold_with_fn'): 
                            attribute = attribute(component.interactable)
                        if attribute == component.interactable.threshold_condition['goal_value']: pass # threshold is True, continue executing function
                        else: return False # threshold is False, return from attempt_move
                    
                    else: 
                        pass # active component with a true threshold. update location and continue to next component
                


            
            ## END FOR: Done Simulating Components along the Edge ##


        # All Component Thresholds Reached; loop back thru and reset the dependent components threshold values to False now that we have confirmed an event occurred 
        print('\n')
        for component in edge:     
            component.interactable.threshold = False  # reset the components threshold
            print(f'(Simulation/Vole.py, attempt_move) the threshold condition was met for {component.interactable.name}.') #CHANGE Event: {event}')
        
        


        ## Update Vole Location ## 
        self.current_loc = destination

        sim_log(f'(Vole.py, attempt_move) Simulated Vole {self.tag} successfully moved into chamber {self.current_loc}')
        print(f'Simulated Vole{self.tag} Move Successful: New Location is Chamber {self.current_loc}')
        return True



    def make_multichamber_move(self, goal): 
        pass 
     
    def random_move(self): 
        ''' chooses a random neighboring chamber to try to move to '''


    #
    # Random Vole 
    #   
    def possible_actions(self): 
        # NOTE: this function has not been updated, so before use will need fixing!! 

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
            actions.append( (self.attempt_move, adj_chmbr) ) # add to list of possible moves 
        
        # add all possible "interact w/in chamber interactables" options
        for interactable in self.map.graph[self.current_loc].interactables: # for all of the interactables in the current chamber
            actions.append( (self.simulate_vole_interactable_interaction, interactable) )
        
        return actions



    def attempt_random_action(self): 
        ''' calls random_action to chose an action at random (or w/ weighted probabilities), and then calls the chosen function '''

        (action_fn, arg) = self.random_action() 
            
        sim_log(f'(Vole.py, attempt_random_action) Vole{self.tag} attempting: {action_fn.__name__} (arg: {arg}) ')
        print(f'(Vole.py, attempt_random_action) Vole{self.tag} attempting: {action_fn.__name__} (arg: {arg}) ')

        action_fn(arg) 



    def random_action(self): 
        ''' Randomly choose between interacting with an interactable or making a move or doing nothing
            Returns the (function, arguments) of the chosen action
        '''

        '''
        randomly choose between the following options: 
        1. pass, i.e. vole sits still. Have vole sleep for 1<x<10 number of seconds. 
        2. vole interacts w/ an interactable in its chamber (look @ self.map.graph[self.current_loc].interactables to randomly choose an interactable to interact with)
        3. vole attempts to make a move to a random chamber (look @ self.map.graph[self.current_loc].connections to randomly choose a neighboring chamber to choose to)
        '''

        possible_actions = self.possible_actions()
        # print('possible actions: ', possible_actions)
        
        # choose action from possible_actions based on their value in the current chamber's probability distribution

        action_probability = self.map.graph[self.current_loc].action_probability_dist
        if action_probability is not None: 
            # User has set probabilities for the actions, make decision based on this. 
            print('action probability:', action_probability)
            pd = [] # list to contain probabilities in same order of actionobject_probability
            for a in possible_actions: 
                # retrieve each possible actions corresponding probability, and append to an ordered lsit 
                pd.append(action_probability[a])
            
            idx = random.choices( [i for i in range(0,len(possible_actions)-1)], weights = pd, k = 1 )

        
        else: 
            # no probabilities have been set, make decision where every possible action has an equal decision of being chosen
            idx = random.randint(0, len(possible_actions)-1)

        return possible_actions[idx] # returns the ( function, arguments ) of randomly chosen action



    

    def set_action_probability(self, action, probability): 

        ''' adjust the probability of Vole taking a certain action, where vole either sleeps, interacts w/ interactables, or moves chambers
        automatically adjusts the probability of the other actions accordingly 
        e.g. if we increase probability of action=sleep to 10%, then we will auto-adjust the probability of action and interactable to 45% each. 
        '''
        
    
