import logging
import json
from apscheduler.schedulers.blocking import BlockingScheduler

from set_logging import set_logging
from qualysfetcher import fetch

from configuration import Configuration

set_logging()   #Set basic config and rotation handler

LOG = logging.getLogger(__name__)   #Get logger for use locally

def main():
    scheduler = BlockingScheduler()
        
    schedules = Configuration().get_schedules()

    for key, value in schedules.items():
        scheduler.add_job(fetch, 'cron', [key], **value)

    #scheduler.start()

    fetch("asset_group")
    #fetch("activity_log")

if __name__ == "__main__":
    main()
