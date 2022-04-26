import logging

from static import set_logging
from other import method1

set_logging()   #Set basic config and rotation handler
LOG = logging.getLogger(__name__)   #Get logger for use in local function 

def main():

    LOG.info("start")

    method1()

    LOG.info("stop")

if __name__ == "__main__":
    main()
