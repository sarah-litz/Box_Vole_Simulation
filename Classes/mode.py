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

# Classes
class modeABC:
    """This is the base class, each mode will be an obstantiation of this class.
    """

    def __init__(self, map = None, timeout = None, enterFuncs = None, exitFuncs = None, **kwargs):
        # Set the givens
        self.rfidQ   = None
        self.box     = map
        self.threads = None
        self.active  = False
        self.timeout = timeout
        self.optional = kwargs
        self.inTimeout = False 
        self.startTime = None

        # Set variables as the enter and exit strings
        self.enterStrings = enterFuncs
        self.exitStrings  = exitFuncs
        
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

    def __init__(self):
        self.ID = None
        self.threshold = None

    def activate(self):
        raise NameError("Needs to be overwritten")

    def __set_threshold(self, condition=True):
        """Override function to automatically bypass the logic of the object and set the threshhold value to whatever it needs to be. This can be accessed by either the safety software of the simulation software.

        Args:
            condition (bool, optional): [description]. Defaults to True.
        """

        self.threshold = condition

    def reset(self):
      
      self.__reset()
      self.threshold = False
      
    def __reset(self):
      
      raise NameError("Overwrite with unique logic")
    
    def threader(func):
        """This is a decorator function that runs the given function on its own thread in the system. It will create, start, and end the thread on the given function.

        Args:
                func (function object): The decorated function, auto passed in.
            """
        def inner(*args,**kwargs):
            """This the function that the decorator returns, actually runs the necessary things for the threader decorator.
                """
            # Create the thread
            print("Thread Created")
            tempThread = threading.Thread(target=func,args=args,kwargs=kwargs)

            # Start the thread and run the function
            print("Thread started")
            tempThread.start()

            while tempThread.isAlive():
                time.sleep(1)

            # End the thread
            print("Thread ended")

        return inner

    @threader
    def listen(self):
      # Listens to the object for when threshold is set to true
      
      while self.threshold == False:
        time.sleep(0.1)
        
class lever(interactableABC):
    def __init__(self, ID, signalPin, numPresses = 1):
        # Initialize the parent class
        super().__init__()

        # Initialize the given properties
        self.ID        = ID 
        self.signalPin = signalPin
        self.numPresses = numPresses

        # Initialize the retrieved variables
        self.angleExtend  = None
        self.angleRetract = None

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

    def __init__(self, ID, servoPin):
        # Initialize the abstract class stuff
        super().__init__()
        
        # Set the input variables
        self.ID       = ID 
        self.servoPin = servoPin

        # Set the state variable, default to False (closed). (open, closed) = (True, False)
        self.close() # Make sure doors are all closed first
        self.state = False

        # Set properties that will later be set
        self.currentAngle = None
        self.openAngle = None
        self.closeAngle = None

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

    def __init__(self, ID, rfidQ = None):
        # Initialize the parent 
        super().__init__()

        # Initialize the required properties
        self.ID = ID 

        # Init the found properties
        self.rfidQ = None
        self.specificQ = queue.LifoQueue()

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