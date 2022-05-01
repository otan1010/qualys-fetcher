import logging

from set_logging import set_logging
from api import get_from_api

from configuration import Configuration

set_logging()   #Set basic config and rotation handler

LOG = logging.getLogger(__name__)   #Get logger for use locally

def main():
    print(get_from_api("detection_fixed"))

    #conf = Configuration()

    #print(conf.get_endpoint("activity_log"))
    #print(conf.get_static_params())
    #print(conf.get_logging())

if __name__ == "__main__":
    main()
