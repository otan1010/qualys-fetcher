import logging
import json
from apscheduler.schedulers.blocking import BlockingScheduler

from set_logging import set_logging
from qualysfetcher import fetch

from configuration import Configuration

set_logging()   #Set basic config and rotation handler

LOG = logging.getLogger(__name__)   #Get logger for use locally

def main():
    #scheduler = BlockingScheduler()

    #scheduler.add_job(fetch, 'cron', ["activity_log"], minute="1", hour="*/1")

    #scheduler.add_job(fetch, 'cron', ["detections_fixed"], minute="1", hour="0", day="*/1")
    #scheduler.add_job(fetch, 'cron', ["detections"], minute="5", hour="0", day="*/1")
    #scheduler.add_job(fetch, 'cron', ["asset_group"], minute="30", hour="0", day="*/1")
    #scheduler.add_job(fetch, 'cron', ["asset"], minute="35", hour="0", day="*/1")
    #scheduler.add_job(fetch, 'cron', ["knowledgebase"], minute="40", hour="0", day="*/1")

    #scheduler.start()

    #fetch("detection")
    #fetch("knowledgebase")
    #fetch("activity_log")
    fetch("asset_group")

if __name__ == "__main__":
    main()
