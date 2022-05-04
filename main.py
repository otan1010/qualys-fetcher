import logging

from set_logging import set_logging
from qualysfetcher import QualysFetcher

from configuration import Configuration

set_logging()   #Set basic config and rotation handler

LOG = logging.getLogger(__name__)   #Get logger for use locally

def main():

    got = QualysFetcher().get()

    print(got.text)
    print(got.headers)
    print(got.url)

if __name__ == "__main__":
    main()
