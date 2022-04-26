import logging

from static import set_logging
from other import get_from_api

set_logging()   #Set basic config and rotation handler
LOG = logging.getLogger(__name__)   #Get logger for use locally

def main():

    LOG.info("start")

    get_from_api()

    LOG.info("stop")

if __name__ == "__main__":
    main()
