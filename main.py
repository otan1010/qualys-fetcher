import logging

from set_logging import set_logging
from qualysfetcher import QualysFetcher

from configuration import Configuration

set_logging()   #Set basic config and rotation handler

LOG = logging.getLogger(__name__)   #Get logger for use locally

def main():
    #print(QualysFetcher().get("detection_fixed"))

    print(Configuration().credentials)
    print(Configuration().get_endpoint("activity_log"))

    #print(conf.get_endpoint("activity_log"))
    #print(conf.get_static_params())
    #print(conf.get_logging())

if __name__ == "__main__":
    main()
