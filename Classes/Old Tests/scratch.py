
      ''''
        class rfid:
            ## not sure what the normal code will look like ## 
            # Simulation Version! #  
            @threaded_fn
            def condition_for_threshold_to_get_set_to_true(): 
                # constantly looping and updating the rfid threshold val 
                if self.ping_queue gets new value: 
                    write val to output 
                    self.threshold = True 
                

        class Wheel: 
            @threaded_fn
            def condition_for_threshold_to_get_set_to_True(): 
                # constantly looping and updating the rfid threshold val 
                if self.moves is True: 
                    self.threshold = True 
                # simulation version of this function would look the same 
                # if the user specified to simulate the wheel, then the sim script will specify at what times the vole interacts with the wheel 
                # when vole interacts with the wheel, we will just directly set wheel.moves to True to "simulate" the movement. 
        class Lever: 
            @threaded_fn 
            def condition_for_threshold_to_get_set_to_true(): 
                if presses == self.required_presses: 
                    self.threshold = True 
            ## Simulation Version of this Function would look the same ##
            # if the user specified that we are simulating the lever (no physical hardware), then the user will directly specify in their simulation 
            # script that the vole should press the lever, by simply directly adding one to the self.pressed count 
            # ( or this will happen randomly if we are running a random_vole_moves() experiment ) 

        class Door: 
            @threaded_fn 
            def condition_for_threshold_to_get_set_to_true(open): 
                if open is True: # set threshold to True after successfully opening door 
                    self.open_door() 
                    self.threshold = True
                else: # set threshold to True after successfully closing door 
                    self.close_door() 
                    self.threshold = True

                    ~~~~~ simulation version of this funciton ~~~~    
                    ## If the user wants to abstract away from physical hardware, override the condition_for_threshold function ## 
                    ## ensures that we don't call any functions that interact with the rpi ## 
                    ## Simulation should Override the function condition_for_threshold_to_get_set_to_true(): 
                    def condition_for_threshold_to_get_set_to_true(open): 
                        if open is True: 
                            print('opening door')
                            self.threshold = True 
                        if open is False: 
                            print('closing door')
                            self.threshold = True 
            
            def isOpen(): 
                return state_switch # hardware! 
            def open_door(): 
                raspberry_pi_things.open # hardware
                if state_switch: # hardware! 
                    self.isOpen = True 
            def close_door(): 
                rpi.close # hardware! 
                if state_switch: #hardware!
                    self.isOpen = False         
        '''



        '''
        class rfid: 
            @threaded_fn 
            def condition_for_threshold_to_get_set_to_True(): 
                # constantly looping and updating the rfid threshold val
                if 3 items have been added to self.ping_queue: 
                    self.threshold = True 
        '''
        '''
            if self.box.rfid1.threshold is True: 
                self.box.door1.open() 
        '''



# next TODO: from Map.py, when creating the interactable or component from the info from map.json, 
# start reading in the new "threshold_condition" value so we can know what the 
# threshold attribute/value goal is for each component. Pass this info when creating 
# the interactable, and give interactables a new attribute to store this information.  
'''         _________________________________________________________________________________
            ## the simulation version reverses the order of a cause/effect reaction. 
            # Non-Simulation Version #
            # in the non-simulation version, the control software has the following cause/effect
                                            cause = some set of actions has met the threshold condition 
                                                (e.g. 2 lever presses in a row, where the threshold was defined as lever.required_presses == 2) 
                                                
                                                --> maybe in the function we can just say (if (condition) | if (simulation==True)&&(bypass==True)), go ahead and add to threshold_event_queue. 
                                                    if (simulation==True)&&(bypass==True): make sure to also wait a good num of seconds before adding to the event queue again to avoid adding an endless amount to the queue
                                            
                                            effect = add to threshold_event_queue 


                # so we are checking for if the condition has been met. 
            # Simulation Version # 
            # in the simulation version, the control software has the following cause/effect
                                        cause = something got added to the threshold_event_queue 
                                        effect = update attributes of the component to reflect the event 
                    for example, appending to an rfid queue, or changing the isOpen state of the door. 

            



            example for setting these values, with edge components (lever1, rfid1, door1, rfid2)

                # NON-SIM -- checks these attributes to see if their threshold_conditions have been met: 
                lever1.condition( lever1.required_presses == 6 )
                    def condition: 
                        if arg is True: lever1.signal_threshold() # adds to queue 
                
                class InteractableABC
                    def signal_threshold() 
                        # effect: add to queue 
                        self.threshold_event_queue.put() 
                    def threshold_attributes() 
                        # (NON-SIM) cause: check if attribute equals desired value --> set as dict of {attribute: value}
                        # (SIM) effect: set the attribute values
                        if self.condition_dict is True: self.signal_threshold() 
                class rfid1
                    ## Setting Values so it works for both Non-Sim and Sim Version 
                    self.condition_dict = { "rfidQ": True }
                class door1 
                    self.condition_dict = { "isOpen": True }
                class lever1
                    self.condition_dict = { "required_presses":6, "pressed":"required_presses" }
                class rfid2
                    self.condition_dict = { "rfidQ": True }






                door1.condition( door1.isOpen() == True ) 

                rfid1.condition( rfid1.rfidQ.added() ) 

                # SIM 
                
          _________________________________________________________________________________
'''
self = None 


# Logic to change the num presses every time the wheel is run
while self.active:
    # If the wheel has been interacted with, increase the number of required presses
    if self.box.wheel_1.threshold_event_queue.get(block=False): # if an event was added to the queue to denote that the threshold's condition was met 
        self.box.chamber_lever.required_presses += 1
    
    # if lever was pressed required number of times, open door, reset the tracked num of lever presses to 0  
    if self.box.chamber_lever.threshold_event_queue.get(block=False): # if lever's threshold queue gets new value 
        self.box.chamber_lever.presses = 0 # reset tracked num of presses to 0
        self.door.open_door() # open door 
    
    # if rfid1 and rfid2 were pinged (meaning the vole moved to the next chamber), close door 
    if self.box.rfid1.threshold.threshold_event_queue.get(block=False) and self.box.rfid2.threshold_event_queue.get(block=False): 
        self.door.close_door() # close door 


        # LEAVING OFF HERE!!! 
        # simulate attribute has now been added to all of the interactable objects for use by the simulation 
        ''''
        class interactableABC: 
            self.event_queue # any event, even if it does not meet the defined threshold condition, will get added to this queue
            self.threshold_event_queue # if threshold condition is met, then we add to this queue 

            def sim_check(): 
                # decorator thread that should be called in any function that accesses hardware parts (the rpi)
                # this function should be overriden in each interactable, and specific simulation logic should sit in this function 


            def setup_watch_for_threshold_event(): 
                if hasattr(self.simulate): 

                    if self.simulate: 

                            #   .... OR? instead of overriding the normal function should we just 
                            # write a function that forces the threshold condition to be met?? 
                            # And then the watch_for_threshold_event function will still be running so will recognize that the threshold was met
                        
                        # override the normal functionality of so it waits for stuff 
                        # to get added to the threshold_event_queue, and if stuff gets added can manually update 
                        # attributes to reflect the threshold event. 

           
           
           
           
            def watch_for_threshold_event(): 



                # if not simulating, watch the condition and add to threshold_event_queue when condition is met 


                cause = some actions has met the threshold condition 
                    (e.g. 2 lever presses in a row, where the threshold was defined as lever.required_presses == 2) 
                effect = add to threshold_event_queue 


                # function that is unique to each interactable 
                # specifies the specific conditions required to meet the threshold
                # if that condition is met then an event is added to the threshold_event_queue 
                # continue to loop and check for if the threshold condition is met 

        class rfid:
            ## not sure what the normal code will look like ## 
            # Non-Simulation Version! #  
            def watch_for_threshold_event(): 
                # constantly looping to check if the defined condition has been met 
                # once condition gets met, then append to the threshold_event_queue 
                # this one is a little weird for the rfid readers because we are just taking things from one queue and placing it in another 
                # i.e. the threshold "condition" is if there is a ping, so if anything gets added to the rfid_q then we have met the threshold 
                new_ping = self.rfid_q.get(): 
                if new_ping: 
                    self.threshold_event_queue.put(new_ping)
            
          _________________________________________________________________________________
            ## the simulation version reverses the order of a cause/effect reaction. 
            # Non-Simulation Version #
            # in the non-simulation version, cause = some actions has met the threshold condition (e.g. 2 lever presses in a row, where the threshold was defined as lever.required_presses == 2) 
                                             effect = add to threshold_event_queue 
                # so we are checking for if the condition has been met. 
                # when condition is met, the control software appends to the th
            # Simulation Version # 
            # in the simulation version, cause = something added to the threshold_event_queue 
                                         effect = update attributes of the component to reflect the event 
                                                    for example, appending to an rfid queue, or changing the isOpen state of the door. 
          _________________________________________________________________________________

        class Door: 
            @threaded_fn
            def watch_for_threshold_event(): 
                # loops over the condition that gets defined here 
                # if condition is met at any point, then append to the threshold_event_queue 
                
                # door is watching for any state change in the door 
                prev_state = self.isOpen
                if self.isOpen != prev_state: 
                    # change in door state detected, write to threshold event queue
                    self.threshold_event_queue.put(self.isOpen)
            
            ## simulation functionality ## 
                # user will just directly change is isOpen value to force door to do what they want 
                # 
            
            def sim_check(): 
                if self.simulation == True: 
                     then we don't want to actually call open/close door
                     since this call is made directly from the experiment code, we need a way to prevent that function from fully executing
                     instead, just directly update the isOpen value to reflect the desired function 
                     the watch_for_threshold_event should see this state change and will append to the threshold_event_queue
                     then return from both functions, without ever having called the open/close door function. 

            @sim_check
            def open_door() 




        class Wheel: 
            
            def watch_for_threshold_event(): 
                # constantly looping on own thread to check if the defined condition has been met. 
                # once condition gets met, then append to the threshold_event_queue
                if self.moves is True: 
                    self.threshold_event_queue.put(True)
            
            
            ## simulation functionality ## 
                # user will just directly add self.moves to True 
                # or to skip this function all together, can directly append to the threshold_event_queue


        class Lever: 

            @threaded_fn 
            def watch_for_threshold_event(): 
                # constantly looping to check if the defined condition has been met. 
                # once condition gets met, then append to the threshold_event_queue

                if presses == self.required_presses: 
                    self.threshold_event.put(True) 

            ## simulation functionality ##
            # user will just directly add 1 to self.presses
            # or can skip this function all together by directly adding to the levers threshold_event_queue


        class Door: 
            @threaded_fn 
            def condition_for_threshold_event(open): 
                if open is True: # set threshold to True after successfully opening door 
                    self.open_door() 
                    self.threshold = True
                else: # set threshold to True after successfully closing door 
                    self.close_door() 
                    self.threshold = True

                    ~~~~~ simulation version of this funciton ~~~~    
                    ## If the user wants to abstract away from physical hardware, override the condition_for_threshold function ## 
                    ## ensures that we don't call any functions that interact with the rpi ## 
                    ## Simulation should Override the function condition_for_threshold_to_get_set_to_true(): 
                    def condition_for_threshold_event(open): 
                        if open is True: 
                            print('opening door')
                            self.threshold_event.put(True, 'door opened')
                        if open is False: 
                            print('closing door')
                            self.threshold_event.put(True, 'door closed') 
            
            def isOpen(): 
                return state_switch # hardware! 
            def open_door(): 
                raspberry_pi_things.open # hardware
                if state_switch: # hardware! 
                    self.isOpen = True 
            def close_door(): 
                rpi.close # hardware! 
                if state_switch: #hardware!
                    self.isOpen = False         
        '''



        '''
        class rfid: 
            @threaded_fn 
            def condition_for_threshold_event(): 
                # constantly looping and updating the rfid threshold val
                if 3 items have been added to self.ping_queue: 
                    self.threshold = True 
        '''
        '''
            if self.box.rfid1.threshold is True: 
                self.box.door1.open() 
        '''





            ''' ____________________________________________________________________________________________'''








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
        rfid_lst = []

        debug(f' traversing the edge: {edge} ')

        # traverse the linked list 
        for component in edge: 

            # check if component is an rfid --> if it is an rfid, then add to rfid queue
            # TODO: figure out how to handle diff. components! 
            #
            # LEAVING OFF HERE! 
            # abstract away from needing to reference specific hardware objects.
            # in particular, figure out how to avoid referencing the mode.rfid object. 
            #
            
            
            # if rfid, place in lst to iterate over later. Otherwise, check that the component's threshold is True. 
            if type(component) == mode.rfid: 
                rfid_lst.append(component) # add rfids to list so we can write to queue after checking all thresholds 

            # if not rfid, check that the threshold is True
            if component.interactable.threshold is False:
                print(f'{component.interactable} threshold is False, cannot complete the move.')
                return False  
            
        # if all interactables along the edge had true thresholds, then we are able to make the move, so we should ping the rfids to simulate the move
        ## Rfid Pings ##
        for component in rfid_lst: 

            component.to_queue(self.tag, component.id) # RFID ping: (vole tag, rfid num)


        ## Update Vole Location ## 
        self.current_loc = destination

        debug(f'Vole {self.tag} successfully moved into chamber {self.current_loc}')





            
            
            
            
            ''' ____________________________________________________________________________________________'''
            ''' This Class will actually be implemented by Control Software, so delete this after Integration '''
            ## TODO: Delete This Class once Control Software Interactable Objects have been Completed!
            class Interactable:
                def __init__(self, threshold_requirement_func = None): 
                    
                    self.ID = None
                    self.threshold = None

                    #self.initial_threshold = initial_threshold
                    #self.initial_threshold_requirement_func = threshold_requirement_func
                    #self.threshold = initial_threshold 
                    #self.threshold_requirement_func = threshold_requirement_func

                def set_threshold(self, bool): 
                    self.threshold = bool  
                def reset(self): 
                    self.__reset()
                    self.threshold = False 
                def __reset(self): 
                    raise NameError("Overwrite with unique logic")

            ''' ____________________________________________________________________________________________'''

            "rfid2":{
                "function": { 
                    "arguments": "self, vole_tag, rfid_id", 
                    "body":"self.rfidQ.append(vole_tag, rfid_id)"
                }
             }

            ''' ____________________________________________________________________________________________'''


            
class Simulation 
     # old threading stuff; functions don't work yet, just was a rough layout 

    #
    # Running the Simulation 
    #
    def threader(self, isModeActive, func_to_run): 
        ''' decorator function that is called from the function we want to run '''

        pass 


    def run_sim(self, isModeActive, func_to_run): 

        ''' This function is called from the control software each time a simulation function should be executed '''
        # LEAVING OFF HERE! 
        # TODO -- probs needs fixing! 
        # creates thread with target function 'func_to_run' 
        # returns in case that either current_mode.active is set to False (either due to external interruption or because the mode.exit() function was reached
        
        # spawn thread, check that isModeActive is True, and start thread 
        sim_thread = threading.Thread(target=func_to_run, daemon=True)
        if isModeActive: sim_thread.start() 

        # let thread run while mode is Active 
        while isModeActive: 
            time.sleep(.05)
        
        # mode is exiting, return from function, effectively stopping the simulation
        return 




class Component: 
        # thinking i should move these into Simulation.py instead! 

        def simulate(self, vole): 
            ''' simulates a Vole's interaction with the interactable -- Called by the user script that specifies what actions the vole should make leading up to a move_chamber call '''
            if self.interactable.threshold_requirement_func: 
                # execute function to meet threshold 
                self.interactable.threshold_requirement_func() 
            else: 
                # simulate by directly setting the threshold to True 
                self.interactable.set_threshold(True)
        
        def set_threshold_requirement(self, func): 
            self.interactable.threshold_requirement_func = func

        def reset(self): 
            self.interactable.reset() 





def set_action_probability( self, actionobj_probability_lst):

            # actionobj_probability_lst: list of (actionobject, new_p) 

            for a in self.action_objects: 
                if a not in actionobj_probability_lst: 
                    raise Exception(f'must set the probability value for all action objects within the chamber ({self.action_objects}). Did not find a value for {a}. ')
            

            newsum = sum(a for (a,p) in actionobj_probability_lst) 
            if newsum != 1: 
                raise Exception(f'probabilities must sum to 1, but the given probabilities added to {newsum}')
            

            for (a,p) in actionobj_probability_lst: 
                self.actionobject_probability[a] = p

            #ISSUE: what if there are only 2 action objects in a chamber and both of their isDefaults are False. Then would be impossible to adjust the probability since could never change a diff value to ensure that total probability is 100%
            # to solve this issue, for now am ridding of the use of .isDefault, and no matter what, we will adjust all the other action-objects. 

            # updates the objects probability of getting chosen, and adjusts the other probabilities to ensure that they add up to 100% 
            # if an object's isDefault==False, then it does not get adjusted. Only the objects that have isDefault==True will be updated. 
            # if probability does not sum to 100 and there are no objects that are able to be adjusted to reach 100%, throw an error


            '''adjustable_actionobjects = [ a for (a,p) in self.action_objects if a not in actionobj_probability_lst ] # put any remaining actionobject in lst 
            # total_diff = 
            for actionobj in actionobjectlst: 

                old_p = self.actionobject_probability[actionobj]
                p_diff = new_p - old_p
                # adjustable_actionobjects = [ a for a in self.action_objects if (self.actionobject_probability[a].isDefault and a != actionobj) ] # new list of adjustable objects, discluding the object of the current action-object we are trying to change the probability of 
                

                # increase/decrease the probabilities of adjustable_actionobjects such that in total the change in probability is equal to that of p_diff 
                
                num_adjustables = len(self.actionobject_probability) - len(actionobjectlst)   
                if num_adjustables < 1: raise Exception(f'cannot adjust the probability of {actionobj} to a value not equal to 100%, because it is the only action-object accessible from chamber {self.id}')
                
                adjusted_p = p_diff/num_adjustables # divide the total change in p equally amongst all of the other action_objects
                for a in self.actionobject_probability: # loop thru the action-objects that we want to adjust, and change probability value accordingly
                    self.actionobject_probability[a] = self.actionobject_probability[a] + adjusted_p
                
                self.actionobject_probability[actionobj] = new_p # update with new probability value
                new_sum = sum(v for (k,v) in self.actionobject_probability.items()) # double check that new sum is 100%
                if new_sum != 1: 
                    raise Exception(f'something went wrong in adjusting the probabilities (def set_action_probability in Map Class). the sum after changing the probability is now {new_sum}')
                

           '''
                

        class ActionObjectProbability:
            def __init__( self ): 
                
                distribution = Table().domain()
                #self.probability = probability # updated probability 
                #self.initial_p = probability # initial default probability 
                #self.isDefault = True # Boolean to represent if probability has changes from default or not 
            
            def update_probability( self, new_p ): 
                self.probability = new_p 
                self.isDefault = False 
    __________________________________________________________________________________________________________________________________________________________________________________


    Remove Chamber Note--> decided i don't need this because it makes sense that throughout experient user will want to add/remove different components, but doesn't make sense that they would want to remove an entire chamber. 
    Plus, if I do need this function, then i have to deal with ensuring that I am not removing a chamber with a vole currently in it. 
    For the same reasoning of I don't see why people would need to do this task mid-experiment, I also am not creating a remove_edge function

    def remove_chamber(self, id): 
        ''' remove Chamber object '''
        if self.get_chamber(id) is None: 
            raise Exception(f'chamber {id} does not exist, so cannot remove it from map')
        
        if self.graph[id].connections: 
            # connections dictionary is not empty; deal with edges 
            edges = self.graph[id].connections.values()
            raise Exception(f'You are trying to remove chamber {id} which is an endpoint in the following Edge objects that need to be removed first:' + str([f'{e}'for e in edges]))
        
        if self.graph[id].interactables: 
            # interactables list is not empty; deal with chamber's interactables 
            raise Exception(f'You are trying to remove chamber {id} which contains the following Interactables that need to be removed first:' + str([f'{i}'for i in self.graph[id].interactables]))

        del self.graph[id]
   
   
   def draw_map_helper(self, vertex_ids, edges): 

        # Base Case 
        if ( len(vertex_ids) == 0): return 
        else: 
            vertexid = vertex_ids.pop(0)
            chmbr = self.map.graph[vertexid]
            
            drawvoles = [] 
            drawedges = []

            for vole in self.voles: 
                if vole.current_loc == chmbr.id: drawvoles.append(vole.tag)

            for e in edges: 
                if ((e.v1 == vertexid) or (e.v1== vertexid)): 
                    # Current Chmbr has an undrawn edge; follow/draw this edge first 
                    drawedges.append(edges.remove(e)) # remove and add to edges to draw


            print(f'_____________\n|   (C{chmbr.id})    |')

            if len(drawvoles) > len(drawedges): 
                max = len(drawvoles)
            else: max = len(drawedges)

            for x in range(0,max): 
                if len(drawvoles)>0: 
                    v = drawvoles.pop() 
                space = 8 - len(str(v)) 
                if len(drawedges)>0: 
                    e = f' -------E{drawedges.pop().id}--------'
                print(f'|V[{v}]' + f"{'':>{space}}" + '|' + f'{e}')
            print(f'-------------')
    def draw_map(self): 
        ''' Recursively Prints Map and Voles '''

        edges = copy.deepcopy(self.map.edges)
        v_ids = self.map.graph.keys() 

        self.draw_map_helper(v_ids, edges)

        '''for cid in self.map.graph.keys(): 
            chmbr = self.map.graph[cid]
            cvoles = [] 
            for v in self.voles: 
                if v.current_loc == chmbr.id: cvoles.append(v.tag)
            print(f'_____________\n|   (C{chmbr.id})    |')

            for v in cvoles: 
                space = 8 - len(str(v)) 
                print(f'|V[{v}]' + f"{'':>{space}}" + '|')
            print(f'-------------')

            # Base Case: if vertices list is empty, return '''






{ 
    "chambers": [ 
        {
            "id": 1, 
            "descriptive_name": "Main Chamber", 
            "interactables": [
                {"interactable_name":"lever1", "type":"lever"},
                {"interactable_name":"water1", "type":"interactableABC"}, 
                {"interactable_name":"food1", "type":"food"}
            ] 
        }, 

        {
            "id": 2, 
            "descriptive_name": "Chamber 2", 
            "interactables": []
        }, 

        {
            "id": 3, 
            "descriptive_name": "Chamber 3",
            "interactables": [
                { "interactable_name":"wheel1", "type":"wheel" }
            ]
        }
    
    ], 

    "edges": [
        {
            "start_chamber_id":1, 
            "target_chamber_id":2, 
            "id":12, 
            "type":"shared", 
            "components":[
                { "interactable_name":"rfid1", "type":"rfid" }, 
                { "interactable_name":"door1", "type":"door" }, 
                { "interactable_name":"rfid2", "type":"rfid" }
            ]
        }, 

        { 
            "start_chamber_id":1, 
            "target_chamber_id":3, 
            "id": 13, 
            "type":"shared", 
            "components":[
                { "interactable_name":"rfid3", "type": "rfid" }, 
                { "interactable": "door2", "type": "door" }, 
                { "interactable": "rfid4", "type": "rfid" }
            ]
        }
    ]
}