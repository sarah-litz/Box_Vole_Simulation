"""
Authors: Ryan Cameron
Date Created: 1/24/2022
Date Modified: 1/24/2022
Description: This is the class file for the mode classes which contain all the information for the control software of the Homecage project to move between different logic flows. Each mode of operation has a different flow of logic, and this file contains the base class and any extra classes that are necessary to manage that.

Property of Donaldson Lab at the University of Colorado at Boulder
"""

# Imports
from posixpath import split
import inspect
from Logging.logging_specs import control_log
import time
import threading
from ..Classes.Timer import countdown



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
        print(f'\nnew mode entered: {self}') # print to console 

        time.sleep(2) # pause before activating interactables 

        self.map.activate_interactables() # ensure that interactables are running for the new mode 

        self.setup() # prep for run() function call ( this is where calls to deactivate() specific interactables should be made )

        time.sleep(3) # Pause Before Starting

        self.startTime = time.time() 
        self.active = True # mark this mode as being active, triggering a simulation to start running, if a simulation exists

        self.inTimeout = True 
        mode_thread = threading.Thread(target = self.run, daemon = True) # start running the run() funciton in its own thread as a daemon thread
        mode_thread.start() 

        # countdown for the specified timeout interval 
        countdown( timeinterval = self.timeout, message = f"remaining in {self}'s timeout interval" )

        # exit when the timeout countdown finishes
        self.exit()   

        mode_thread.join() # ensure that mode thread finishes before returning 

     
    def exit(self): 
        """This function is run when the mode exits and another mode begins. It closes down all the necessary threads and makes sure the next mode is setup and ready to go. 
        """

        print(f"{self} finished its Timeout Period and is now Exiting")
        self.inTimeout = False
        self.active = False 

        self.map.deactivate_interactables(clear_threshold_queue = True) # empties the interactable's threshold event queue and sets active = False



    @threader
    def listen(self):
        """This method listens to the rfid queue and waits until something is added there.
        """
        pass


    def setup(self): 
        ''' any tasks for setting up box before run() gets called '''
        raise NameError('this funciton should be overriden')

    def run(self):
        """This is the main method that contains the logic for the specific mode. It should be overwritten for each specific mode class that inherits this one. Because of that, if this function is not overwritten it will raise an error on its default. 
        """

        # If not overwritten, this function will throw the following error
        raise NameError("This function must be overwritten with specific mode logic")


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

