import logging

from set_logging import set_logging
from api import get_from_api

from configuration import Configuration

set_logging()   #Set basic config and rotation handler

LOG = logging.getLogger(__name__)   #Get logger for use locally

def main():

    conf = Configuration("activity_log")

    conf.get_dynamic()

if __name__ == "__main__":
    main()
