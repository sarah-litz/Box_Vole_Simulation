
# To Use These Specifications, place this import statement at top of file: 
# from Logging.logging_specs import debug


import logging
logging.basicConfig(filename='/Users/sarahlitz/Projects/Donaldson Lab/Vole Simulator Version 1/Box_Vole_Simulation/Classes/Logging/eventlogging.log', level=logging.DEBUG )


def debug(message): 
    logging.debug(message)