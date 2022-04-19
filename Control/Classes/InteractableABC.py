"""
Authors: Sarah Litz, Ryan Cameron
Date Created: 1/24/2022
Date Modified: 4/6/2022
Description: Class definition for interacting with hardware components. This module contains the abstract class definition, as well as the subclasses that are specific to a piece of hardware.

Property of Donaldson Lab at the University of Colorado at Boulder
"""

# Standard Lib Imports 
from cgitb import reset
import time
import threading
import queue

# Local Imports 
from Logging.logging_specs import control_log, sim_log


class interactableABC:

    def __init__(self, threshold_condition):
        self.ID = None
        self.active = False # must activate an interactable to startup threads for tracking any vole interactions with the interactable

        ## Threshold Tracking ## 
        self.threshold = False
        self.threshold_condition = threshold_condition  # {attribute, initial_value, goal_value} dict to specify what the attribute/value goal of the interactable is. 
        self.threshold_event_queue = queue.Queue() # queue for tracking anytime a threshold condition is met 
        self.new_threshold_count = 0 # boolean for how many new events have been added 

        self.dependents = [] # if an interactable is dependent on another one, then we can place those objects in this list. example, door's may have a dependent of 1 or more levers that control the door movements. 


    def activate(self):
        self.threshold = False # "resets" the interactable's threshold value so it'll check for a new threshold occurence
        self.active = True 
        self.watch_for_threshold_event() # begins continuous thread for monitoring for a threshold event

    def deactivate(self): 
        self.active = False 


    def isSimulation(self): 
        ''' checks if object is being simulated. 
        if it does, then it can avoid/shortcut certain functions that access hardware components. '''

        if hasattr(self, 'simulate'): 
            if self.simulate is True: 
                return True 
        return False


    def run_in_thread(func): 
        ''' decorator function to run function on its own daemon thread '''
        def run(*k, **kw): 
            t = threading.Thread(target = func, args = k, kwargs=kw, daemon=True)
            t.start() 
            return t
        return run 

    def add_new_threshold_event(self): 
        # appends to the threshold event queue 

        raise Exception(f'override add_new_threshold_event')
        self.threshold_event_queue.put()
        # NOTE: delete this 
        '''if hasattr(self, 'update_goal_after_threshold_event'):
            self.update_goal_after_threshold_event()'''

    @run_in_thread
    def watch_for_threshold_event(self, constant=None, reset_vals=False): 

        control_log(f"(InteractableABC.py, watch_for_threshold_event) {self.name} has been activated. starting contents of the threshold_event_queue are: {list(self.threshold_event_queue.queue)}")
        while self.active: 

            # using the attribute/value pairing specified by the threshold_condition dictionary
            # if at any time the given attribute == value, append to the threshold_event_queue.

            # if constant is True, then this is a threaded function that is running throughout the entire experiment execution 
            # if constant is False, then this function must be manually called by the control software whenever we need to watch for a threshold event occurrence for the interactable 

            # if reset_vals is True, value of the attribute will get reset to its starting state
            # if reset_vals is False, value of the attribute will remain the same

            threshold_attr_name = self.threshold_condition["attribute"]
            attribute = getattr(self, threshold_attr_name) # get object specified by the attribute name

            # control_log(f"(InteractableABC.py, watch_for_threshold_event) {self.name}: Threshold Name: {threshold_attr_name}, Threshold Attribute Obj: {attribute}")
            
            # check for attributes that may have been added dynamically 
            if hasattr(self, 'check_threshold_with_fn'): # the attribute check_threshold_with_fn is pointing to a function that we need to execute 
                attribute = attribute(self) # sets attribute value to reflect the value returned from the function call
            
            
                
            
            # Check for a Threshold Event by comparing the current threshold value with the goal value 
            if attribute == self.threshold_condition['goal_value']: # Threshold Event: interactable has met its threshold condition
                
                event_bool = True 


                #
                # Dependents Loop 
                #
                for dependent in self.dependents: 
                    # if dependents are present, then before we can add an event to current interactable, we must check if the dependents have met their threshold 
                    # loop thru all the dependents, and if any dependent has not already detected a threshold_event, then the current interactable has not met its threshold. 

                    if dependent.active is False: 
                        # dependent is not currently active, skip over this one 
                        break 

                    print(f'(InteractableABC.py, watch_for_threshold_event, dependents_loop) {self.name} event queue: {list(self.threshold_event_queue.queue)}')
                    print(f'(InteractableABC.py, watch_for_threshold_event, dependents_loop) dependent of {self.name} : {dependent.name} (event queue: {list(dependent.threshold_event_queue.queue)})')

                    time.sleep(3)      

                    # Threshold Not Reached
                    if not dependent.threshold:
                        # depedent did not reach its treshold, so neither does the current interactable
                        print(f"(InteractableABC.py, watch_for_threshold_event, dependents_loop) {self.name}'s dependent, {dependent.name} did not reach threshold")
                        event_bool = False 
                        break  # do not need to check any remaining interactables in the list
                

                    else: 
                        # Retrieve the Event of the Current Interactable's Dependent.  
                        control_log(f"(InteractableABC.py, watch_for_threshold_event, dependents loop) Threshold Event for {self.name}'s dependent, {dependent.name}.") 
                        print(f"(InteractableABC.py, watch_for_threshold_event, dependents_loop) Threshold Event for  {self.name}'s dependent, {dependent.name}.") 
                # End of Dependents Loop 
             


                #
                # Interactable Threshold Event Handling
                #             
                if event_bool: 
                    ## AN EVENT! ## 

                    # Reset the Threshold Values of the interactable's Dependents (ok to do so now that we have confirmed that there was a threshold event)
                    for dependent in self.dependents: 
                        dependent.threshold = False 

                    # Handle Event 
                    print(f"(InteractableABC.py, watch_for_threshold_event) Threshold Event for {self.name}")
                    self.add_new_threshold_event()
                    self.threshold = True 
                    
                    print(f'(InteractableABC.py, watch_for_threshold_event) {self.name} event queue: {list(self.threshold_event_queue.queue)}')


                    # Since an event occurred, check if we should reset the attribute value 
                    if 'reset_value' in self.threshold_condition.keys() and self.threshold_condition['reset_value']: 

                        setattr( self, self.threshold_condition['attribute'], self.threshold_condition['initial_value'] )

                        control_log( f' (InteractableABC,py, watch_for_threshold_event) resetting the threshold for {self.name}  ')

                else: 
                    # no threshold event 
                    # print(f'(InteractableABC.py, watch_for_threshold_event) no threshold event for {self.name}')
                    pass 
            
            
            else: 
                # no threshold event
                # print(f"(InteractableABC.py, watch_for_threshold_event) no threshold event for {self.name}.") # Attributes Value: {attribute}, Goal Value: {self.threshold_condition['value']}") 
                # control_log(f"(InteractableABC.py, watch_for_threshold_event) {self.name} has not reached its threshold value")
                # print(type(attribute), type(self.threshold_condition['value']))
                pass 
                
            
            time.sleep(0.75)

            if constant == False: 
                control_log(f"(InteractableABC.py, watch_for_threshold_event {self.name} was set to only check for a threshold once. Exiting function with contents of the threshold_event_queue as: {list(self.threshold_event_queue.queue)}")
                return 
            
        
        control_log(f"(InteractableABC.py, watch_for_threshold_event) {self.name} has been deactivated. Final contents of the threshold_event_queue are: {list(self.threshold_event_queue.queue)}")


    def reset(self):
      
        self.__reset()

      # called each time there is a new mode 

      # if the simulation was running for this interactable, then its threshold_event_queue should be empty 

      # if the simulation is not running, then this is where we empty out its threshold_event_queue
      

    def __reset(self):
      
      raise NameError("Overwrite with unique logic")
    
        
class lever(interactableABC):
    def __init__(self, ID, signalPin, threshold_condition):
        # Initialize the parent class
        super().__init__(threshold_condition)

        # Initialize the given properties
        self.name = 'lever'+str(ID) 
        self.ID        = ID 
        self.signalPin = signalPin

        
        ## Threshold Condition Tracking ## 
        self.pressed = self.threshold_condition["initial_value"] # counts current num of presses 
        #self.required_presses = self.threshold_condition["goal_value"] # Threshold Goal Value specifies the threshold goal, i.e. required_presses to meet the threshold
        #self.threshold_attribute = self.threshold_condition["attribute"] # points to the attribute we should check to see if we have reached goal. For lever, this is simply a pointer to the self.pressed attribute. 

        # Initialize the retrieved variables
        self.angleExtend  = None
        self.angleRetract = None

        # Note: do not call self.activate() from here, as the "check_for_threshold_fn", if present, gets dynamically added, and we need to ensure that this happens before we call watch_for_threshold_event()  

    def add_new_threshold_event(self): 

        # appends to the lever's threshold event queue 
        self.threshold_event_queue.put(f'lever{self.ID} pressed {self.pressed} times!')
        # self.threshold_condition['goal_value'] = self.update_goal_after_threshold_event(self)
        print('(lever(InteractableABC), add_new_threshold_event) updated threshold: ', self.threshold_condition['goal_value'])


        # (NOTE) if you don't want this component to be checking for a threhsold value the entire time, then deactivate here and re-activate when a new mode starts 
        #self.deactivate()


    #@threader
    def extend(self):
        """Extends the lever to the correct value
        """
        pass

    #@threader
    def retract(self):
        """Retracts lever to the property value
        """

    def __move(self, angle):
        """This moves the lever to the specified angle. This can be any angle in the correct range, and the function will produce an error if the angle is out of range of the motor. 

        Args:
            angle (int): Servo angle to move to. This should be between 0 and 180 degrees
        """
        pass

    def __check_state(self):
        """Instantaneously returns the state of the lever
        """
        pass

class door(interactableABC):
    """This class is the unique door type class for interactable objects to be added to the Map configuration.

    Args:
        interactableABC ([type]): [description]
    """

    def __init__(self, ID, servoPin, threshold_condition, dependent=None):
        # Initialize the abstract class stuff
        super().__init__(threshold_condition)
        
        # Set the input variables
        self.name = 'door'+str(ID)
        self.ID       = ID 
        self.servoPin = servoPin

        self.lever = dependent # lever that controls the door
        # in order for a threshold event to occur, there must have also been a threshold_event for its dependent interactable
        
        # Set the state variable, default to False (closed). (open, closed) = (True, False)
        self.state = threshold_condition['initial_value'] # assumes that config file reflects the current state of the physical door


        # Set properties that will later be set
        self.currentAngle = None
        self.openAngle = None
        self.closeAngle = None

        # Note: do not call self.activate() from here, as the "check_for_threshold_fn", if present, gets dynamically added, and we need to ensure that this happens before we call watch_for_threshold_event()  

    def activate(self): 
        self.active = True 
        self.watch_for_threshold_event()
        # watch_for_threshold_event is called directly from open() and close() functions

    def add_new_threshold_event(self): 
        # appends to the threshold event queue 
        self.threshold_event_queue.put(f'{self.name} isOpen:{self.state}')
        print(f'(Door(InteractableABC.py, add_new_threshold_event) {self.name} event queue: {list(self.threshold_event_queue.queue)}')
        #NOTE: self.threshold_condition['goal_value'] = self.update_goal_after_threshold_event(self)
        print('(Door(InteracbleABC.py), add_new_threshold_event) updated threshold: ', self.threshold_condition['goal_value'])
        
        
        # (NOTE) if you don't want this component to be checking for a threhsold value the entire time, then deactivate here and re-activate when a new mode starts 
        self.deactivate()

    #@threader
    def close(self):
        """This function closes the doors fully"""

        # check if the door is already closed 
        if self.state is False: 

            # door is already closed 
            control_log('(Door(InteractableABC)) {self.name} is Closed')
            print(f'(Door(InteractableABC)) {self.name} is Closed')
            return 


        # if in simulation, the simulate_vole_interactable_interaction should be manually setting the new state value 


        time.sleep(6) # time for door to close 

        #
        # LEAVING OFF HERE!!!!! 
        # 
        print(f'(Door(InteractableABC), close() ) Hardware Accessed Stuff Here to Close {self.name}')





        
        

        


    #@threader
    def open(self):
        """This function opens the doors fully
        """
        # set the threshold_condition to reflect the desired goal
        self.threshold_condition['goal_value'] = True  


        # check if the door is getting simulated (i.e. hardware is present or not)
        if hasattr(self, 'simulate'): 
            if self.simulate == True: 
                # if simulating door, manually set the state val 
                self.state = True 
                return 


        time.sleep(3) 

        #
        # LEAVING OFF HERE! 
        #
        if self.state == True: 

            # door is already closed 
            control_log('(Door(InteractableABC)) {self.name} is Open')
            print(f'(Door(InteractableABC)) {self.name} is Open')
            return 
        
        else: 

            raise Exception(f'(Door(InteractableABC), open() ) Hardware Accessed Stuff Here to Open {self.name}')


    def check_state(self):
        """This returns the state of whether the doors are open or closed, and also sets the state variable to the returned value
        """
        pass

    #@threader
    def __set_door(self, angle):
        """This sets the door value to any given input value.

        Args:
            angle (int): Servo angle to set the door value to.
        """
        pass

class rfid(interactableABC):
    """This class is the unique class for rfid readers that is an interactable object. Note that this does not control the rfid readers like the other unique classes, it only deals with the handling of rfid data and its postion in the decision flow.

    Args:
        interactableABC ([type]): [description]
    """

    def __init__(self, ID, threshold_condition, rfidQ = queue.Queue()):
        # Initialize the parent 
        super().__init__(threshold_condition)

        # Initialize the required properties
        self.name = 'rfid'+str(ID)
        self.ID = ID 

        # Init the found properties
        self.rfidQ = queue.Queue()
        self.rfidQisEmpty = self.rfidQ.empty() # returns True if queue is Empty
        self.specificQ = queue.LifoQueue()

        # Note: do not call self.activate() from here, as the "check_for_threshold_fn", if present, gets dynamically added, and we need to ensure that this happens before we call watch_for_threshold_event()  

    def add_new_threshold_event(self): 
        # appends to the threshold event queue 
        # set isNewEvent to True 

        ping = self.rfidQ.get_nowait()
        self.threshold_event_queue.put(ping)

        # do not deactivate the rfids. always monitoring for pings. 



    def from_queue(self, numEntries = 1):
        """Pulls the given number of entries from the shared rfidQ with the hardware or simulation.

        Args:
            numEntries (int, optional): Number of queue entries to pull. Defaults to 1.
        """
        pass

    def to_queue(self, data):
        """Puts the given data into the object specific queue that is initialized.

        Args:
            data (any): Data to be added to the specificQ property
        """
        pass

    def is_empty(self, queue):
        """Determines if a queue is empty or if there is information to grab. Returns a boolean

        Args:
            queue (queue): queue to query and check for emptiness.
        """
        pass

#if __name__ == "__main__":