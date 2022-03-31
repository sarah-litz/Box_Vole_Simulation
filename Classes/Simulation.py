
# Local Imports 
from Logging.logging_specs import sim_log
from Vole import Vole
from Map import Map

# Standard Lib Imports 
import copy
import threading 
import time 
import json



class SimulationABC: 

    def __init__(self, modes, map, vole_dict={}): 
        
        # TODO: option for passing in voles dictionary, and we immediately initialize the voles as specified by the dictionary
        self.voles = []
        
        self.map = map

        self.configure_simulation(map.config_directory + '/simulation.json') # updates map features

        self.simulation_func = {} # dict for pairing a mode with a simulation function 

        self.modes = modes

        # TODO: either use a vole_dict argument option OR setup_voles option. Think it'll be confusing if both options are offered.
        # self.setup_voles()
        for (i,c) in vole_dict.items(): self.new_vole(i,c) # instantiate new voles 
    


    #
    # Threaded Simulation Runner 
    #
    def run_in_thread(func): 
        ''' decorator function to run function on its own thread '''
        def run(*k, **kw): 
            t = threading.Thread(target = func, args = k, kwargs=kw, daemon=True)
            t.start() 
            return t
        return run 
    
    @run_in_thread
    def run_sim(self): 

        sim_log('(Simulation.py, run_sim) Daemon Thread for getting the active mode, and running the specified simulation while active mode is in its timeout period.')

        ''' This Function Runs Continuously Until the Experiment Ends 
                    Runs on a separate thread 
                    Calls the function that is paired with the currently active mode '''

        # TODO: the function that we call should potentially also run on its own thread, so then all this function does is 
        # loop until the active mode is not in Timeout or the current mode is inactive. Basically will just allow for a more immediate 
        # stopage of the simulation when a mode gets out of timeout and/or stops running 

        while True: 
            ''' we can assume that this thread will get killed when the main thread running the modes finishes '''
            ''' so we can just keep looping and assume that we are in between modes, and that a mode will eventually become active again '''


            # Set the Currently Active Mode 
            current_mode = self.get_active_mode() # update the current mode 

            
            while current_mode is False: # if no mode is currently active 
                # wait for a mode to become active 
                time.sleep(0.5)
                current_mode = self.get_active_mode() # update the current mode when one becomes active 

            sim_log(f'\n\n  New Mode\n(Simulation.py, run_sim) Simulation Updating for Control Entering a New Mode: {(current_mode)}')


            # Loop Until Current Mode is Inactive
            while current_mode.active: # reruns simulation while the mode is still active

                #
                # Wait for Mode's Timeout Interval
                while not current_mode.inTimeout and current_mode.active: # active mode not in Timeout
                    # while not in timeout portion of mode, loop 
                    time.sleep(0.5)

                sim_log(f'(Simulation.py, run_sim) The current mode ({current_mode}) entered in timeout. Checking for if a simulation should be run. ')
                #
                # Check for if simulation function 
                if current_mode not in self.simulation_func.keys(): # no simulation function specified for this mode 
                    # do nothing loop until current mode is inactive 
                    sim_log(f'(Simulation.py, run_sim) No simulation function for {type(current_mode)}.')
                    while current_mode.active: 
                        time.sleep(0.5)

                
                sim_log(f'(Simulation.py, run_sim) {current_mode} is paired with the simulation function: {self.simulation_func[current_mode]}')
                #
                # Check if an iterator value was specified (num of times to call the sim function) 
                sim_iterator = None # specifies number of times to call the simulation function (optional)
                sim_fn = None # simulation function 
                
                if type(self.simulation_func[current_mode]) is tuple: # sim_iterator specified
                    # if the value is a tuple, then there is a specified number of times to run the function 
                    sim_iterator = self.simulation_func[current_mode][1]
                    sim_fn = self.simulation_func[current_mode][0]

                    # remove sim function from dictionary since we have a set num of times to run it, we don't want to retrieve it from dict again 
                    del self.simulation_func[current_mode]
                
                else: # no sim_iterator specified
                    # if the value is not a tuple, then the function should just rerun continuously until while loop can exit 
                    sim_fn = self.simulation_func[current_mode]
                        
                
                #
                # Run the Mode's Simulation Function
                # TODO: this needs testing! 
                while current_mode.inTimeout and current_mode.active:  # active mode is in timeout 
                    
                    if sim_iterator is None: 
                        
                        sim_log(f'(Simulation.py, run_sim) Simulaton is calling the function:{sim_fn}')

                        sim_fn()  # calling function continuously throught timeout interval 

                    elif sim_iterator > 0:  
                        
                        sim_log(f'(Simulation.py, run_sim) Simulaton is calling the function:{sim_fn}')

                        sim_fn() # function call for running the simulation 

                        sim_iterator -= 1 # decrement the iterator each run 
                    
                    time.sleep(2)
            



    def get_active_mode(self): 

        '''returns the mode object that is currently running ( assumes there is never more than one active mode at a given point in time ) '''
       
        for mode in self.modes: 
            if mode.active: 
                return mode 
        
        return False
    
    

    
    #
    # Vole Getters and Setters 
    #
    def setup_voles(self):  raise Exception('you need to add a setup_voles() method to your simulation! This is where you should add/initialize any voles that you want to Simulate.')

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
                i = i.name # reset i so we loop thru the names of the interactable objects
                if len(str(i)) > 8: 
                    i = i[:7] + '-'
                space = 8 - len(str(i)) 
                print(f'|I[{i}]' + f"{'':>{space}}" + '|')

            print(f'-------------')

    
    def draw_edges(self): 
        edges = self.map.edges
        for e in edges: 
            interactables = [c.interactable.name for c in e] # creates list of the interactable names 
            print(f'({e.v1}) <---{interactables}----> ({e.v2})')
    
    
    


    #
    # Add Simulation Features to Map 
    #
    def configure_simulation(self, config_filepath): 
        '''function to read/parse the simulation configuration file'''
        ''' Adds a simulation attribute to all of the interactables '''

        sim_log(f"(Simulation.py, configure_simulation) reading/parsing the file {config_filepath}")


        # opening JSON file 
        f = open(config_filepath)

        # returns json object as a dictionary 
        data = json.load(f) 

        # closing JSON file
        f.close() 


        ## add a simulation boolean attribute to each component that is on an edge in the map ## 
        # if an interactable doesn't exist in the json file, print message and set simulation attribute to be False 

        # copy list of interactables so we can ensure that every interactable gets an attribute 
        instantiated_interactables_copy = self.map.instantiated_interactables.copy() # shallow copy 
        

        for i in data['interactables']: 
            
            # check if interactable exists on edge or in chamber
            loc_type = instantiated_interactables_copy[i['name']][0] # string that takes value of "chamber" or "edge"
            loc_id = instantiated_interactables_copy[i['name']][1] # id of the chamber or edge 
            del instantiated_interactables_copy[i['name']] # delete val from the dict's copy 

            if loc_type == 'edge':
                # get object from edge 
                obj = self.map.get_edge(loc_id).get_interactable_from_component(i['name']) 
            
            else: 
                # get object from chamber 
                obj = self.map.graph[loc_id].get_interactable(i['name'])

            # give obj new attribute to represent if we should simulate the interactable or not  
            setattr(obj, 'simulate', i['simulate']) 

            # if provided, set the optional function to call for simulation process
            if 'simulate_with_fn'in i: 
                setattr(obj, 'simulate_with_fn', eval(i['simulate_with_fn']))                
        
        # set attribute for any interactables that were not specified 
        for name in instantiated_interactables_copy.keys(): 
            print(f'simulation.json did not contain the interactable {name}. sim defaults to False, so this interactable will not be simulated as the simulation runs.')
            sim_log(f'simulation.json did not contain the interactable {name}. sim defaults to False, so this interactable will not be simulated as the simulation runs.')

            loc_type = instantiated_interactables_copy[name][0] # chamber or edge 
            loc_id = instantiated_interactables_copy[name][1] # id of chamber or edge 

            if loc_type == 'edge': obj = self.map.get_edge(loc_id).get_interactable_from_component[name]
            else: obj = self.map.graph[loc_id].get_interactable(name)

            # assign new attribute to False 
            setattr(obj, 'simulate', False)


        # clear copied dictionary 
        instantiated_interactables_copy.clear() 
        return 




    #
    # Simulate Vole-Interactable Interactations
    #



if __name__ == '__main__': 
    
    print('SimulationABC is an Abstract Base Class, meaning you cannot run it directly. In order to run a Simulation, create a subclass of SimulationABC')