import logging
#import json
from os import replace

#import requests
from requests.auth import HTTPBasicAuth
#from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.util.retry import Retry

from configuration import Configuration
from parsers import Parser
from get_session import get_session

#from guppy import hpy

LOG = logging.getLogger(__name__)

def fetch(endpoint):
    conf = Configuration().get_endpoint(endpoint)
    session = get_session(endpoint)

    write_to = conf.get("options").get("write_to")
    item_tag = conf.get("options").get("item_tag")
    url = conf.get("url")
    headers = conf.get("headers")
    params = conf.get("params")
    username = conf.get("credentials").get("username")
    password = conf.get("credentials").get("password")

    out = "data/" + write_to
    prev = out + ".prev"

    try:
        replace(out, prev)
    except Exception as err:
        LOG.error(err)

    truncation = 1
    while truncation:
        response = session.get(url, headers=headers, params=params, auth=HTTPBasicAuth(username, password))

        content_type = response.headers.get("Content-Type")

        parsed = Parser(response.text, content_type, endpoint, item_tag)

        with open(out, 'a') as file:
            for item in parsed.get_items():
                file.write(item)
                file.write("\n")

        new_id = parsed.get_new_id()

        if new_id:
            params.update(new_id)
        else:
            truncation = 0
