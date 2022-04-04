"""
Authors: Ryan Cameron
Date Created: 1/24/2022
Date Modified: 1/24/2022
Description: This is the class file for the mode classes which contain all the information for the control software of the Homecage project to move between different logic flows. Each mode of operation has a different flow of logic, and this file contains the base class and any extra classes that are necessary to manage that.

Property of Donaldson Lab at the University of Colorado at Boulder
"""
# Imports
from posixpath import split
import time
import threading
import queue
import inspect

from Logging.logging_specs import control_log


# Classes
class modeABC:
    """This is the base class, each mode will be an obstantiation of this class.
    """

    def __init__(self, timeout = None, map = None, enterFuncs = None, exitFuncs = None, bypass = False, **kwargs):
        # Set the givens
        self.rfidQ   = None
        self.map     = map
        self.threads = None
        self.active  = False
        self.timeout = timeout
        self.optional = kwargs
        self.inTimeout = False 
        self.startTime = None

        # Set variables as the enter and exit strings
        self.enterStrings = enterFuncs
        self.exitStrings  = exitFuncs



    def __str__(self): 
        return __name__
    def threader(self):
        """This is a decorator function that will be added to any method here that needs to run on its own thread. It simply creates, starts, and logs a method to a thread. 
        """
        pass

    def enter(self):
        """This method runs when the mode is entered from another mode. Essentially it is the startup method. This differs from the __init__ method because it should not run when the object is created, rather it should run every time this mode of operation is started. 
        """
        pass

    @threader
    def listen(self):
        """This method listens to the rfid queue and waits until something is added there.
        """
        pass

    def run(self):
        """This is the main method that contains the logic for the specific mode. It should be overwritten for each specific mode class that inherits this one. Because of that, if this function is not overwritten it will raise an error on its default. 
        """

        # If not overwritten, this function will throw the following error
        raise NameError("This function must be overwritten with specific mode logic")

    @threader
    def exit(self):
        """This function is run when the mode exits and another mode begins. It closes down all the necessary threads and makes sure the next mode is setup and ready to go. 
        """
        pass

    def __find_func(self, functionName):
        """This function takes a given string and returns a function object that has the name of the given string. For example: If there was a class called "car" with a function called "get_miles" that returned the amount of miles the car has drive, this would look like __fund_func('car.get_miles'), and it would return the function object.

        Args:
            functionName (string): Name of subclass and method in form <objectName>.<methodName>

        Raises:
            NameError: Error is returned if no matching subclass and method is found

        Returns:
            object: actual function object of the subclass
        """
        # Find the object this function is from
        # Search for subclasses of modeABC
        subClasses = self.__find_subclasses(modeABC)

        # Break the functionName into subclass name and the function name
        nameList     = functionName.split('.')
        subClassName = nameList[0]
        methodName   = nameList[1]

        # Loop through the subclasses and find the right function
        for iSubClass in range(len(subClasses)):
            thisSub = subClasses[iSubClass]

            # Check to see if its the right subClass
            if thisSub.__name__ == "subClassName":
                # If its the right sublcass, return the function
                functionObject = getattr(thisSub, methodName)
                
                # Return the function once its found
                return functionObject
        
        # If its never found, rasie an error
        raise NameError("Error: subclass method not found")

    def __find_subclasses(self, module, classObj):
        """This searches through and finds all valid subclasses of the given class. This will include itself in the return.

        Args:
            module (python module): _description_
            classObj (class): _description_

        Returns:
            list: List of subclass objects
        """
        return [
            cls
                for name, cls in inspect.getmembers(module)
                    if inspect.isclass(cls) and issubclass(cls, classObj)
        ]

class interactableABC:

    def __init__(self, threshold_condition):
        self.ID = None
        self.active = False # must activate an interactable to startup threads for tracking any vole interactions with the interactable

        ## Threshold Tracking ## 
        self.threshold_condition = threshold_condition  # {attribute, value} dict to specify what the attribute/value goal of the interactable is. 
        self.threshold_event_queue = queue.Queue() # queue for tracking anytime a threshold condition is met 

        self.dependents = [] # if an interactable is dependent on another one, then we can place those objects in this list. example, door's may have a dependent of 1 or more levers that control the door movements. 

    def activate(self):
        self.active = True 
        self.watch_for_threshold_event() # begins continuous thread for monitoring for a threshold event

    def deactivate(self): 
        self.active = False 


    def run_in_thread(func): 
        ''' decorator function to run function on its own daemon thread '''
        def run(*k, **kw): 
            t = threading.Thread(target = func, args = k, kwargs=kw, daemon=True)
            t.start() 
            return t
        return run 

    @run_in_thread
    def watch_for_threshold_event(self, constant=None, reset_vals=None): 

        control_log(f"(mode.py, watch_for_threshold_event) {self.name} has been activated. starting contents of the threshold_event_queue are: {list(self.threshold_event_queue.queue)}")
        while self.active: 

            # using the attribute/value pairing specified by the threshold_condition dictionary
            # if at any time the given attribute == value, append to the threshold_event_queue.

            # if constant is True, then this is a threaded function that is running throughout the entire experiment execution 
            # if constant is False, then this function must be manually called by the control software whenever we need to watch for a threshold event occurrence for the interactable 

            # if reset_vals is True, value of the attribute will get reset to its starting state
            # if reset_vals is False, value of the attribute will remain the same

            threshold_attr_name = self.threshold_condition["attribute"]
            attribute = getattr(self, threshold_attr_name) # get object specified by the attribute name

            # control_log(f"(mode.py, watch_for_threshold_event) {self.name}: Threshold Name: {threshold_attr_name}, Threshold Attribute Obj: {attribute}")
            
            # check for attributes that may have been added dynamically 
            if hasattr(self, 'check_threshold_with_fn'): # the attribute check_threshold_with_fn is pointing to a function that we need to execute 
                attribute = attribute(self) # sets attribute value to reflect the value returned from the function call
            
            
                
                
            # Check for a Threshold Event by comparing the current threshold value with the goal value 
            if attribute == self.threshold_condition['value']: # Threshold Event: interactable has met its threshold condition

                # check if dependent interactable exists
                if hasattr(self, 'dependent'):  # if the interactable has a dependent interactable, then that interactable must have already detected a threshold_event in order for the current interactable to also be considered true.

                    if self.dependent.threshold_event_queue.empty(): 
                        # depedent did not reach its treshold, so neither does the current interactable
                        pass
                    else: 
                        self.threshold_event_queue.put('An Event!')

                # print(f"(mode.py, watch_for_threshold_event) {self.name} threshold event detected!")
                # control_log(f"(mode.py, watch_for_threshold_event) {self.name} threshold event detected!")
                else: 
                    self.threshold_event_queue.put('An Event!')
            
            else: 
                # no threshold event
                # print(f"watch_for_threshold_event: no threshold event for {self.name}. Attributes Value: {attribute}, Goal Value: {self.threshold_condition['value']}") 
                # control_log(f"(mode.py, watch_for_threshold_event) {self.name} has not reached its threshold value")
                # print(type(attribute), type(self.threshold_condition['value']))
                pass 
                
            time.sleep(0.75)
        
        control_log(f"(mode.py, watch_for_threshold_event) {self.name} has been deactivated. Final contents of the threshold_event_queue are: {list(self.threshold_event_queue.queue)}")


    def reset(self):
      
      self.__reset()
      
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
        self.pressed = 0 # counts current num of presses 
        self.required_presses = self.threshold_condition["value"] # Threshold Goal Value specifies the threshold goal, i.e. required_presses to meet the threshold
        #self.threshold_attribute = self.threshold_condition["attribute"] # points to the attribute we should check to see if we have reached goal. For lever, this is simply a pointer to the self.pressed attribute. 

        # Initialize the retrieved variables
        self.angleExtend  = None
        self.angleRetract = None

        # Note: do not call self.activate() from here, as the "check_for_threshold_fn", if present, gets dynamically added, and we need to ensure that this happens before we call watch_for_threshold_event()  

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
        self.close() # Make sure doors are all closed first
        self.state = False

        # Set properties that will later be set
        self.currentAngle = None
        self.openAngle = None
        self.closeAngle = None

        # Note: do not call self.activate() from here, as the "check_for_threshold_fn", if present, gets dynamically added, and we need to ensure that this happens before we call watch_for_threshold_event()  


    #@threader
    def close(self):
        """This function closes the doors fully
        """
        pass

    #@threader
    def open(self):
        """This function opens the doors fully
        """
        pass

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