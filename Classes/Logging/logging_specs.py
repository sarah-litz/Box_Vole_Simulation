
# To Use These Specifications, place this import statement at top of file: 
# from Logging.logging_specs import debug


import logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


logging.basicConfig(filename='/Users/sarahlitz/Projects/Donaldson Lab/Vole Simulator Version 1/Box_Vole_Simulation/Classes/Logging/eventlogging.log', level=logging.DEBUG )

logging.basicConfig(filename='/Users/sarahlitz/Projects/Donaldson Lab/Vole Simulator Version 1/Box_Vole_Simulation/Classes/Logging/thresholdlogging.log', level=logging.INFO)

def debug(message): 
    logging.debug(message)


def debugthreshold(message): 
    logging.info(message)



