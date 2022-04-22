import logging

from static import set_logging, get_configuration
from other import method1

def main():
    set_logging()                           #Set basic config and rotation handler

    conf = get_configuration()              #Get configuration dict
    
    log = logging.getLogger(__name__)       #Get logger for use in local function 

    log.info(f"logging from {__name__}")

    method1()

if __name__ == "__main__":
    main()
