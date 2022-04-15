
"""
Authors: Sarah Litz, Ryan Cameron
Date Created: 1/24/2022
Date Modified: 4/6/2022
Description: Class definition for Map, a network of Vertices and Edges, where vertices are chambers, and edges are the connections existing between chambers. 
            Objects that represent the hardware (subclasses of InteractableABC) in a box are assigned to either an edge or a chamber within the map. 
            All outside software recieves a Map object, and will go through the Map class in order to interact with any physical hardware.

Property of Donaldson Lab at the University of Colorado at Boulder
"""


# Standard Lib Imports 
from code import interact
from collections import deque
import time
import json 
import os

# Local Imports 
from Logging.logging_specs import control_log
from .ModeABC import modeABC 
from . import InteractableABC
from .InteractableABC import lever, door, rfid

class Map: 
    def __init__(self, config_directory): 
        ''' key is id assigned to vertex: Chamber instance'''
        
        self.graph = {} 

        self.edges = [] # list of all edge objects that have been created ( can also access thru each Chamber instance )

        self.instantiated_interactables = {} # dict of (interactable name: (type=edge or chamber, id) ) to represent every object of type interactableABC that has been created to avoid repeats
        
        self.config_directory = config_directory # directory containing all of the configuration files 

        self.configure_setup(config_directory + '/map.json')

    def print_graph_info(self): 
        for chamber in self.graph.values(): 
            print(chamber)                       # chamber id and adjacent vertices
            for adj in chamber.connections.keys(): 
                edge = chamber.connections[adj]  
                print(edge)                      # edge id and vertices it connects

    #
    # Getters and Setters 
    #        
    def instantiate_interactable_hardware( self, name, type ): 

        ''' anytime that an interactable is added (either to a chamber or to an edge), first a call to this function is made. 
            called from configure_setup in 2 places: 
                (1) first called to instantiate objects that are added to chamber.interactables 
                (2) second called to instantiate objects that are added to chamber.connections[adjacent_chmbr_id].components
            based on the object type and object id, instantiates a new interactableABC subclass object
            the specified "type" is a string representation of an existing interactableABC subclass, specified in the map configuration file
        '''


        # Edge Case: if type is not a valid subclass of interactableABC, raise Exception
        try: getattr(InteractableABC, type)
        except: raise Exception(f' unknown interacatable type: {type} ')


        # Edge Case: if an object of the same type and id has already been created
        if name in self.instantiated_interactables.keys(): raise Exception(f'the interactable {name} already exists. please assign unique names to the interactables.')


        # Edge Case: missing configuration file for either this type of interactable
        config_filepath = None 
        filename = type+'.json'
        for root, dirs, files in os.walk(self.config_directory): 
            if filename in files: 
                config_filepath = os.path.join(root,filename)
        if config_filepath is None: raise Exception(f'there is no configuration file for {type} in {self.config_directory}')
            
        #
        # Read in the config file for this type of interactable
        #
        f = open( config_filepath ) # opening json file 
        
        data = json.load( f ) # returns json object as a dictionary 

        f.close() # close file

        # edge case: configuration file does not have specifications for an object with this name
        try: objspec = data[name]
        except: raise Exception(f'there is no entry for {name} in the {type} configuration file, {filename}')

        #
        # Instantiate New Interactable
        # 
        if type == 'door': 
            
            # get door w/ <id> from the door config file 
            try: new_obj = door(ID=objspec['id'], servoPin = objspec['servoPin'], threshold_condition = objspec['threshold_condition']) # instantiate door 
            except Exception as e: raise Exception(f'there was a problem instantiating the object {name}: {e}')

        elif type == 'rfid': 

            try: new_obj = rfid(ID=objspec['id'], threshold_condition = objspec['threshold_condition']) # ASK: also need to pass in rfidQ?? confused on where this comes from though. 
            except Exception as e: raise Exception(f'there was a problem instantiating the object: {name}: {e}')

        elif type == 'lever': 
            
            try: new_obj = lever(ID=objspec['id'], signalPin = objspec['signalPin'], threshold_condition = objspec['threshold_condition'])
            except Exception as e: raise Exception(f'there was a problem instantiating the object {name}: {e}')


        else: 

            raise Exception(f'interactableABC does not have a subclass {type} implemented in InteractableABC.py')


        # dynamically set any attributes that can be optionally added to an interactable's configurations
        if "check_threshold_with_fn" in objspec.keys(): 
            setattr(new_obj, 'check_threshold_with_fn', eval(objspec['check_threshold_with_fn']) ) # function for checking if the threshold condition has been met
        if "update_goal_after_threshold_event" in objspec.keys(): 
            setattr(new_obj, 'update_goal_after_threshold_event', eval(objspec['update_goal_after_threshold_event'])) # function to call once the threshold condition has been met
        if "dependents" in objspec.keys(): 
            setattr( new_obj, 'dependent_names', objspec['dependents'] ) # interactable that the threshold is dependent on (e.g. if we want lever1 to control door1, then set door1's dependent to be lever1. )
            
        
        self.instantiated_interactables[name] = new_obj  # add string identifier to list of instantiated interactables
        
        # activate the object so it begins watching for threshold events --> can potentially reposition this to save CPU energy since each interactable gets its own thread. 
        # be careful/don't add the activation statement to the interactable's __init__ statements, because then we get a race condition between this function which sets "check_threshold_with_fn" and the watch_for_threshold_event which gets the "check_threshold_with_fn" value.  

        new_obj.activate()
        return new_obj

        


    #
    # Map Configuration 
    #
    def configure_setup(self, config_filepath): 
        ''' function to read/parse configuration file map.py and set up map accordingly '''

        # opening JSON file 
        f = open(config_filepath)

        # returns json object as a dictionary 
        data = json.load(f) 

        # closing JSON file
        f.close() 

        # Iterate thru to chambers list to initalize the diff chambers and their interactables 
        for chmbr in data['chambers']: 
            
            new_c = self.new_chamber( chmbr['id'] )
            
            for i in chmbr['interactables']: 
                
                # instantiate interactable hardware 
                #try: 
                    new_i = self.instantiate_interactable_hardware( i['interactable_name'], i['type'] )
                    # assign the interactable to a chamber object
                    new_c.new_interactable( new_i )
                
            '''except Exception as e: 
                    print(f"Ran into an issue when trying to instantiate the interactable object: {i['interactable_name']}")
                    print('Error Message: ', e)
                    print(f'would you like to continue running the experiment without instantiating this interactable? If yes, I wont be aware of any interactions a vole may have with it. If no, I will exit the experiment immediately.')
                    ans = input('input (y/n) \n')
                    if ans == 'n': exit() '''
                    
 
        
        # Iterate thru edges list to make connections between the chambers 
        for edge in data['edges']: 

            if edge['type'] == 'shared': 
                
                new_edge = self.new_shared_edge(edge['id'], edge['start_chamber_id'], edge['target_chamber_id'])
                
                for i in edge['components']:

                    # instantiate interactable hardware
                    new_i = self.instantiate_interactable_hardware( i['interactable_name'], i['type'] )

                    new_edge.new_component( new_i )
            
            '''
            elif edge['type'] == 'unidirectional': 

                new_edge = self.new_unidirectional_edge

                for c in edge['components']: 

                    # Unidirectional Edges bring up special case where we may need to reuse/point to an already instantiated interactable.
                    # i.e. the components along the edge may have already been instantiated if a unidirectional edge connecting the same 2 chambers was already created.
                    # If this is the case, then we need to point to the existing component instead of instantiating a new one.  
            '''
        
        self.set_dependent_interactables()
    
         

    def set_dependent_interactables(self): 

        # if an interactable specified a "dependent" in its configuration file, then it gets an attribute "interactable_name" which serves as a string representation of the interactable
        # after all objects have been instantiated, we now want to assign the actual interactable objects rather than just their string representation

        # loop thru all instantiated interactables and check for the attribute interactable_name 
        for i_name in self.instantiated_interactables:
            
            i = self.instantiated_interactables[i_name]
            if hasattr(i, 'dependent_names'): 
                dependents = []
                for dname in i.dependent_names:
                    try: dependents.append(self.instantiated_interactables[dname])
                    except KeyError as e: 
                        print(f' specified an unknown interactable {e} as a dependent for {i.name}. Double check the config files for {e} and for {i.name} to ensure they are correct.')
                        ans = input(f' would you like to carry on the experiment without adding {e} as a dependent for {i.name}? (y/n)')
                        if ans == 'n': exit()


                i.dependents = dependents # store list of dependent objects in the interactables dependent list
                
                delattr(i, 'dependent_names')  # delete the dependent_names attribute since we don't need it anymore 



    def get_chamber(self, id): 
        ''' returns chamber object with specified id '''
        for cid in self.graph.keys(): 
            if cid == id: 
                return self.graph[cid]
        return None

    def new_chamber(self, id): 
        ''' new Chamber instantiated and added to graph'''
        if self.get_chamber(id) is not None: 
            raise Exception(f'chamber with id {id} already exists')
        
        newChamber = self.Chamber(id)
        self.graph[id] = newChamber
        return newChamber


    def new_shared_edge(self, id, v1, v2, components=None):
        ''' single Edge object that is shared by both vertices. Ordering of linked list will require checking the vertex indices ''' 
        if not all(v in self.graph.keys() for v in [v1, v2]): raise Exception(f'Could Not Create Edge: one or both of the chambers has not been created yet, so could not add edge between them.')
        if self.get_edge(id): raise Exception(f'An edge with the id {id} already exists, could not create edge.')
        
        newEdge = self.Edge(id, v1, v2,'shared')
        self.graph[v2].connections[v1] = newEdge 
        self.graph[v1].connections[v2] = newEdge
        self.edges.append(newEdge)
        return newEdge
        

    def new_unidirectional_edges(self, id, v1, v2, components=None): 
        ''' creates 2 new Edges for connecting 2 chambers -- each has a different Edge instance tho, so components may differ '''
        if not all(v in self.graph.keys() for v in [v1, v2]): raise Exception(f'Could Not Create Edge: one or both of the chambers has not been created yet, so could not add edge between them.')
        if self.get_edge(id): raise Exception(f'An edge with the id {id} already exists, could not create edge.')
        
        edge1 = self.Edge(id,v1,v2,"unidirectional")
        self.graph[v1].connections[v2] = edge1 # add edges to vertices' adjacency dict 
        
        rev_id = int(str(id)[::-1]) # reverse the id for the edge going the reverse direction 
        edge2 = self.Edge(rev_id, v2, v1, "unidirectional")
        self.graph[v2].connections[v1] = edge2
        
        self.edges.extend([edge1, edge2]) # add new edges list of map edges
        return (edge1, edge2)

    
    def get_edge(self, edgeid): 
        # sort thru chamber edges and locate edge with <id> 
        for cid in self.graph.keys(): # for all chambers stored in graph
            chamber = self.graph[cid] # get Chamber object
            for adj_id in chamber.connections.keys(): # for all of its adjacent vertices 
                if chamber.connections[adj_id].id == edgeid: # check if vertex has edge w/ that id 
                    return chamber.connections[adj_id]

        return None

    #
    # Path Finding Methods
    #
    def get_path(self, start, goal): 
        '''Returns list of sequential chambers to move from start->goal chamber'''
        def trace_path(previous, s): #helper function for get_path 
            # recursive trace back thru previous dictionary to get path 
            if s is None: return [] 
            else: return trace_path(previous, previous[s])+[s]
        
        # check that start and end chamber exist 
        if start not in self.graph.keys() or goal not in self.graph.keys(): 
            raise Exception(f'chamber {start} and/or chamber {goal} does not exist in the map, so cannot find path')
        
        # BFS 
        frontier = deque([start]) # chambers already explored 
        previous = {start: None} # keeps track of the chamber that came before current chamber 
        if start == goal: return start 
        while frontier: 
            chmbr_id = frontier.popleft() 
            for adj in self.graph[chmbr_id].connections: 
                if (adj not in previous) and (adj not in frontier): 
                    frontier.append(adj) 
                    previous[adj] = chmbr_id # set new chamber's parent chamber 
                    # Goal Check 
                    if adj == goal: 
                        return trace_path(previous, adj)



    # 
    # Chamber -- vertices in the graph
    #  
    class Chamber: 
        def __init__(self,id): 
            self.id = id 
            
            self.connections = {} # adjacent chamber: a single Edge object which points to linked list of components

            self.interactables = [] # interactable specific to a chamber, rather than an edge 

            self.action_probability_dist = None # probabilities are optional; must be added after all interacables and chamber connections have been added. can be added thru function 'add_action_probabilities'


        def __str__(self): 
            return 'Chamber: ' + str(self.id) + ', adjacent: ' + str([x for x in self.connections])
   
        def new_interactable(self, interactable): 
            # Adds interactable to chamber; these objects exist w/in a chamber, and not on an edge so have nothing to do with a vole's movement between chambers
            self.interactables.append(interactable)


        def remove_interactable(self, interactable_name): 
            interactableobj = self.get_chmbr_interactable(interactable_name)
            if interactableobj is None: 
                control_log(f'Chamber{self.id} does not contain {interactable_name}, so this interactable cannot be removed.')
                print(f'Chamber{self.id} does not contain {interactable_name}, so this interactable cannot be removed.')
            self.interactables.remove(interactableobj)

        def get_chmbr_interactable(self, interactable_name): 
            # search list of interactables and return the specified object 
            for i in self.interactables: 
                if i.name == interactable_name: return i 
            return None 
        


        #
        # (for Simulation Use Only) Probability Tracking: tracking probabilities of some Action-Object getting chosen by a Vole when a simulated vole is told to make random decisions
        #
        def add_action_probabilities( self, actionobj_probability_dict ): 
            
            ''' function for extensive error checking before assigning the probabilities to the possible actions from the current chamber '''

            # Check that probabilities have been set for every value (the +1 is for the time.sleep() option)
            if len(actionobj_probability_dict) != len(self.interactables) + len(self.connections) + 1: 
                raise Exception(f'must set the probability value for all action objects (the connecting chambers and the interactables) within the chamber, as well as the "sleep" option (even if this means setting their probability to 0) ')


            # check that the specified action-objects are accessible from the current chamber, and of type Chamber, Interactable, or 'sleep'
            p_sum = 0
            for (k,v) in actionobj_probability_dict.items():  
                if isinstance(k, type(self)): # type: Chamber 
                    if k.id not in self.connections.keys(): 
                        raise Exception(f'attempting to set the probability of moving to chamber{k.id}, which is not adjacent to chamber{self.id}, so cannot set its probability.') 
                elif isinstance(k, type(self.interactables[0])): # type: Interactable 
                    if k.id not in self.interactables: 
                        raise Exception(f'attempting to set the probability of choosing interactable {k.id} which does not exist in chamber {self.id}, so cannot set its probability.')
                elif k != 'sleep': # only remaining option is type=='sleep', throw error if it is not
                    raise Exception(f'{k} is an invalid object to set a probability for')
                else: 
                    p_sum += v


            # check that the probability values sum to 1
            if p_sum != 1: 
                raise Exception(f'the probabilities must sum to 1, but the given probabilities for chamber{self.id} summed to {p_sum}')
            

            self.action_probability_dist = actionobj_probability_dict

        

    #
    # Edges -- linked list for storing Components
    # 
    class Edge:    
        def __init__(self, id, chamber1, chamber2, type=None): 
            
            # Identifying Edge w/ id val and the chambers it connects 
            self.id = id 
            self.v1 = chamber1 
            self.v2 = chamber2
            self.type = type 

            # Component Makeup of the Edge 
            self.headval = None # will point to first instance of Component
        
        def __str__(self): 
            interactables = [c.interactable.name for c in self] # list of the interactable object's Names -- (concatenation of type+ID)
            if self.type=='shared': 
                return 'Edge ' + str(self.id) + f', connects: {self.v1} <--{interactables}--> {self.v2}'

            return 'Edge ' + str(self.id) + f', connects: {self.v1} --{interactables}---> {self.v2}'

        ''' Methods for Traversing and Locating Components on an Edge '''
        def __iter__(self): 
            component = self.headval
            while component is not None: 
                yield component
                print 
                component = component.nextval


        def component_exists(self, interactable): 
            # beginning at headval, traverses linked list to find component. Returns True if exists, False otherwise 
            if (self.headval.interactable == interactable): 
                return True
            c = self.headval
            while(c.nextval): 
                c = c.nextval 
                if c.interactable == interactable: 
                    return True
            return False

        def get_interactable_from_component(self, name): 
            '''traverses linked list and returns object with specified name'''
            if not (self.headval): 
                # Edge does not contain any components (i.e. no interactables) 
                return None 

            if (self.headval.interactable.name == name): 
                return self.headval.interactable
            
            c = self.headval
            while(c.nextval):
                c = c.nextval 
                if c.interactable.name == name: 
                    return c.interactable
            return None # a component with an interactable with name does not exist in linked list

        def get_component(self, interactable): 
            ## helper function for adding components into the linked list ## 
            '''beginning at headval, traverses linked list to find component. Returns None if it does not exist'''
            
            if not (self.headval): 
                # Edge does not contain any components 
                return None 

            if (self.headval.interactable == interactable): 
                return self.headval 

            c = self.headval
            while(c.nextval): 
                c = c.nextval 
                if c.interactable == interactable: 
                    return c 
            return None # c does not exist in linked list 


        ''' Adding and Removing Components from Edge '''
        def new_component(self, newinteractable): 
            # instantiates new Component and adds to end of linked list
            newComp = self.Component(newinteractable)

            if self.headval is None: 
                self.headval = newComp
                return newComp
            
            component = self.headval 
            while(component.nextval):
                component = component.nextval # list traversal to get last component in linked list 
                if component.interactable == newComp.interactable:                 
                    # check that component is not a repeat 
                    del newComp
                    raise Exception(f'component not added because this component has already been added to the edge')
            
            
            component.nextval = newComp # update list w/ new Component
            newComp.prevval = component # set new Component's previous component to allow for backwards traversal     
            return newComp
                

        def new_component_after(self, newinteractable, previnteractable): 
            '''instantiates and adds new component directly after the specified interactable (so can be in middle of linked list if desired)''' 

            if (self.component_exists(newinteractable)) is True: raise Exception(f'{newinteractable} already exists on this edge')
            if previnteractable is not None: 
                if (self.component_exists(previnteractable)) is False: raise Exception(f'{previnteractable} must already exist on this edge to add a component that follows it, so could not add {newinteractable}')

            newComp = self.Component(newinteractable) # Instantiate New Component object to get added into linked list

            # if previous component set to None, then make new component the new head of Linked List
            if previnteractable == None: 
                if self.headval is None: 
                    del newComp
                    # linked list is empty, use new_component() to add the first component
                    return self.new_component(newinteractable)
                else: 
                    # make newinteractable the new head of the linked list 
                    prevhead = self.headval 
                    self.headval = newComp
                    self.headval.nextval = prevhead
                    return self.headval
            
            else: 
                prevComp = self.get_component(previnteractable) # retrieve prevComp and check that it exists 
                nxtComp = prevComp.nextval

                # once prevcomponent is located, instantiate new component and update the vals of the previous component, current component, and next component
                newComp.prevval = prevComp 
                newComp.nextval = nxtComp

                # update the components on either side of newComp to reflect changes
                prevComp.nextval = newComp 
                nxtComp.prevval = newComp 
                return newComp
        
        def remove_component(self, interactable): 
            ''' updates linked list to remove specified interactable '''

            remComp = self.get_component(interactable)
            if remComp==None: raise Exception(f'{interactable} does not exist, so cannot remove it from linked list') 

            prevComp = remComp.prevval
            nxtComp = remComp.nextval

            if self.headval == remComp: 
                # update the head value of linked list 
                self.headval = nxtComp 
                nxtComp.prevval = None 
            elif nxtComp == None: 
                # remComp is the last element of the linked list
                prevComp.nextval = None 
            else: 
                prevComp.nextval = nxtComp 
                nxtComp.prevval = prevComp 

            del remComp 
            return 



        #
        # Component Object: Subclass of the Edge Class, used for implementing Linked List 
        #
        class Component: 
       
            def __init__(self, interactable): 
                self.interactable = interactable # access to the actual object that represents a hardware component
                self.nextval = None
                self.prevval = None

            
            def __str__(self): 
                return str(self.interactable.name)
            

            
            



                