import logging
import json

from set_logging import set_logging
from qualysfetcher import fetch

from configuration import Configuration

set_logging()   #Set basic config and rotation handler

LOG = logging.getLogger(__name__)   #Get logger for use locally

def main():

    fetch("detection")
    #fetch("knowledgebase")
    #fetch("asset_group")
    #QualysFetcher().fetch("knowledgebase")
    #got1 = QualysFetcher("detection_fixed")
    #got1 = QualysFetcher("activity_log")

    #print(json.dumps(got1.conf, indent=2, default=str))
    #print()

    #got2 = got1.run_endpoint()

    #print(got2.text)
    #print("status_code: ", got2.status_code)
    #print()
    #print("headers: ", got2.headers)
    #print()
    #print("url: ", got2.url)

if __name__ == "__main__":
    main()
