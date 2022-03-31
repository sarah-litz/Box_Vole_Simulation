# from Classes.mode import interactableABC
import mode 
import random
import time 

from Logging.logging_specs import debug

class Vole: 

    def __init__(self, tag, start_chamber, map): 
        self.tag  = tag 
        self.current_loc = start_chamber
        self.map = map 
    

    #
    # Vole Movements
    #
    ## TODO: make_move and make_multichamber_move need work based on Control Software
    def is_move_valid(self, destination): 
        '''Check validity of making a move from voles current location to some destination 
        Does not actually make move/update the voles location, just checks if the move is possible according to map layout 
        Return True if move is possible, False otherwise 
        '''
        curr_chamber = self.map.graph[self.current_loc]
        if destination in curr_chamber.connections.keys(): 
            return True 
        else: return False
    

    def attempt_move(self, destination, validity_check=True): 
        ''' called by Vole object ''' 
        ''' attempts to executes a move. if validity_check is set to True, then we check if the move is physically valid or not. '''
        ''' GETTING the thresholds of each interactable and checking that it is True '''
        ''' if the threshold of any interactable is not True, then we cannot successfully make the move '''

        debug(f'Entering the attempt move function. Vole {self.tag} is currently in chamber {self.current_loc}. Destination: {destination}.')

        if validity_check: 
            if not self.is_move_valid(destination): 

                debug(f'attempting a move that is not physically possible according to Map layout. Skipping Move Request')

                print('attempting a move that is not physically possible according to Map layout. Skipping Move Request.')

                return False
        # retrieve edge between current location and the destination, and check threshold for each of these 
        edge = self.map.graph[self.current_loc].connections[destination]

        debug(f' traversing the edge: {edge} ')

        # traverse the linked list 
        for component in edge: 


            # check if the component should be simulated 
            if component.interactable.simulate: 
                ##
                ## Simulating Interactable thru setting attribute value or thru function call
                ##
                interactable = component.interactable

                print( f'simulating vole{self.tag} interaction with {component.interactable.name}' ) 
                debug( f'(Vole.py, attempt_move) simulating vole{self.tag} interaction with {component.interactable.name}' ) 

                
                if hasattr(component.interactable, 'simulate_with_fn'):
                    
                    # sets the attributes to values that meet the threshold condition by calling simulate_with_fn 
                    component.interactable.simulate_with_fn(component.interactable, self.tag)

                else:
                    
                    # set value using the threshold condition attribute/value pairing 
                    threshold_attr_name = interactable.threshold_condition["attribute"]
                    attribute = getattr(interactable, threshold_attr_name) # get object specified by the attribute name
                    
                    debug(f'{interactable.name}, threshold attribute: {threshold_attr_name}, threshold value: {interactable.threshold_condition["value"]}')
                
                    # manually set the attribute to its goal value so we meet the threshold condition, and trigger the control side to add an event to the threshold_event_queue 
                    setattr(component.interactable, threshold_attr_name, interactable.threshold_condition['value'])
                    # debug(f'{interactable.name}, manual attribute check: {interactable.state}')
                    debug(f"{interactable.name}, attribute result: {attribute}")

                
            else: 
                # component should not be simulated, as the hardware for this component is present. 
                # assumes that there is a person present to perform a lever press, interrupt the rfid reader so it sends a ping, etc. 
                print ( f'if testing the hardware for {component.interactable.name}, take any necessary actions now.')
                
            # TODO: automate the watch_for_threshold function 
            component.interactable.watch_for_threshold_event()
            ########################
            
            # Pause to give control side a moment to assess if there was a threshold event 
            time.sleep(3)

            # check if the control side added a threshold event, meaning this interactables threshold condition was met 
            # if the threshold condition was not met, then display message to tell user that attempted move was unsuccessful, and return from function. 
            if component.interactable.threshold_event_queue.empty(): 
                print(f'the threshold condition was not met for {component.interactable.name}. Vole{self.tag} cannot complete the move from chamber {self.current_loc} to chamber {destination}.')
                return False 
            else:
                event = component.interactable.threshold_event_queue.get()
                print(f'the threshold condition was met for {component.interactable.name}. Event: {event}')
        ## END FOR: Done Simulating Components along the Edge ##


        ## Update Vole Location ## 
        self.current_loc = destination

        debug(f'Vole {self.tag} successfully moved into chamber {self.current_loc}')




    def make_multichamber_move(self, goal): 
        pass 
     
    def random_move(self): 
        ''' chooses a random neighboring chamber to try to move to '''




    #
    # Component Simulation; simulates Vole's interaction w/ some hardware interactable 
    # 
        
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
            actions.append( (self.attempt_move, adj_chmbr) ) # add to list of possible moves 
        
        # add all possible "interact w/ chamber interactables" options
        for interactable in self.map.graph[self.current_loc].interactables: # for all of the interactables in the current chamber
            # TODO: once using control software, change to an actual interactable.simulate 
            actions.append( ('interactable.simulate', self) )
        
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
        print('possible actions: ', possible_actions)
        
        # choose action from possible_actions based on their value in the current chamber's probability distribution

        action_probability = self.map.graph[self.current_loc].action_probability_dist
        if action_probability is not None: 
            # User has set probabilities for the actions, make deicision based on this. 
            print('action probability:', action_probability)
            pd = [] # list to contain probabilities in same order of actionobject_probability
            for a in possible_actions: 
                # retrieve each possible actions corresponding probability, and append to an ordered lsit 
                pd.append(action_probability[a])
            
            idx = random.choices( [i for i in range(0,len(possible_actions)-1)], weights = pd, k = 1 )

        
        else: 
            # no probabilities have been set, make decision where every possible action has an equal decision of being chosen
            idx = random.randint(0, len(possible_actions)-1)


        # LEAVING OFF HERE
        possible_actions[idx][0]( *possible_actions[idx][1:] )


    

    def set_action_probability(self, action, probability): 

        ''' adjust the probability of Vole taking a certain action, where vole either sleeps, interacts w/ interactables, or moves chambers
        automatically adjusts the probability of the other actions accordingly 
        e.g. if we increase probability of action=sleep to 10%, then we will auto-adjust the probability of action and interactable to 45% each. 
        '''
        
    
