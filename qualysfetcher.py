import logging

import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from configuration import Configuration
from api import get_session

LOG = logging.getLogger(__name__)

def fetch(endpoint):
    conf = Configuration().get_endpoint(endpoint)
    session = get_session(endpoint)

    write_to = conf.get("options").get("write_to")
    batch_by = conf.get("options").get("batch_by")
    list_field = conf.get("options").get("list_field")
    list_param = conf.get("options").get("list_param")
    list_from = conf.get("options").get("list_from")

    truncation = 1

    while truncation:
        response = session.get(url, headers=headers, params=params, auth=HTTPBasicAuth(username, password))
        content = response.content

        for item in parse_data(content, 'detections'):
            log_data.critical(item)

        new_id = get_truncation_id(content, 'detections')

        if new_id:
            params['id_min'] = new_id
        else:
            truncation = 0

#    for req in get_next(session, batch_by):
#        data = parse_output(req)
#        write_data(data)
#
#def get_next(session, batch_by):
#
#    if batch_by == "truncation":
#        truncation = 1
#
#        while truncation:
#            #response = session.get()
#            #content = response.content
#            truncation = 0
#
##            for item in parse_data(content, 'detections'):
##                log_data.critical(item)
##
##            new_id = get_truncation_id(content, 'detections')
##
##            if new_id:
##                params['id_min'] = new_id
##            else:
##                truncation = 0
#
#    elif batch_by == "list":
#        pass
